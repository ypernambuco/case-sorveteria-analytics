"""Data cleaning pipeline for the Case Sorveteria Analytics project.

The pipeline keeps raw data immutable, creates auditable interim outputs,
and writes a processed CSV ready for analysis and Power BI consumption.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any
import unicodedata

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw" / "vendas_sorvetes.csv"
INTERIM_DIR = PROJECT_ROOT / "data" / "interim"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

INTERIM_OUTPUT_PATH = INTERIM_DIR / "vendas_sorvetes_interim.csv"
REJECTED_OUTPUT_PATH = INTERIM_DIR / "vendas_sorvetes_registros_excluidos.csv"
QUALITY_REPORT_PATH = INTERIM_DIR / "relatorio_qualidade_tratamento.csv"
PROCESSED_OUTPUT_PATH = PROCESSED_DIR / "vendas_sorvetes_tratado.csv"


COLUMN_MAP = {
    "ID_Transacao": "id_transacao",
    "Data": "data",
    "Hora": "hora",
    "Tipo_Sorvete": "tipo_sorvete",
    "Sabor": "sabor",
    "Quantidade": "quantidade",
    "Valor_Total": "valor_total",
    "Cidade": "cidade",
    "Estado": "estado",
    "Canal_Venda": "canal_venda",
    "Promocao": "promocao",
    "ID_Cliente": "id_cliente",
}

TEXT_COLUMNS = ["tipo_sorvete", "sabor", "cidade", "estado", "canal_venda", "id_cliente"]
MONTH_NAMES = {
    1: "Janeiro",
    2: "Fevereiro",
    3: "Marco",
    4: "Abril",
    5: "Maio",
    6: "Junho",
    7: "Julho",
    8: "Agosto",
    9: "Setembro",
    10: "Outubro",
    11: "Novembro",
    12: "Dezembro",
}
WEEKDAY_NAMES = {
    0: "Segunda",
    1: "Terca",
    2: "Quarta",
    3: "Quinta",
    4: "Sexta",
    5: "Sabado",
    6: "Domingo",
}
EXPECTED_CATEGORY_KEYS = {
    "tipo_sorvete": {"milkshake", "sundae", "picole", "pote", "casquinha"},
    "sabor": {"acai", "cookies", "caramelo", "morango", "menta", "limao", "baunilha", "chocolate", "nao informado"},
    "canal_venda": {"parceiro", "app", "loja fisica"},
    "estado": {
        "ac", "al", "ap", "am", "ba", "ce", "df", "es", "go", "ma", "mt", "ms", "mg",
        "pa", "pb", "pr", "pe", "pi", "rj", "rn", "rs", "ro", "rr", "sc", "sp", "se", "to",
    },
}


@dataclass(frozen=True)
class CleaningResult:
    """Container for pipeline outputs."""

    raw: pd.DataFrame
    interim: pd.DataFrame
    processed: pd.DataFrame
    rejected: pd.DataFrame
    quality_report: pd.DataFrame


def load_raw_data(path: Path = RAW_DATA_PATH) -> pd.DataFrame:
    """Load the immutable raw CSV."""
    return pd.read_csv(path)


def standardize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """Rename columns to snake_case names for analytical use."""
    missing_columns = set(COLUMN_MAP) - set(df.columns)
    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"Missing expected columns in raw data: {missing}")

    return df.rename(columns=COLUMN_MAP)


def normalize_text(value: Any) -> Any:
    """Trim repeated spaces while preserving nulls and accents."""
    if pd.isna(value):
        return value
    return " ".join(str(value).strip().split())


def category_key(value: Any) -> str:
    """Return an accent-insensitive key for category validation."""
    if pd.isna(value):
        return ""
    normalized = unicodedata.normalize("NFKD", str(value))
    ascii_text = "".join(char for char in normalized if not unicodedata.combining(char))
    return ascii_text.strip().lower()


def standardize_text_columns(df: pd.DataFrame) -> tuple[pd.DataFrame, int]:
    """Normalize text fields and return the number of changed cells."""
    clean = df.copy()
    changed_cells = 0

    for column in TEXT_COLUMNS:
        before = clean[column].copy()
        clean[column] = clean[column].map(normalize_text)

        if column in {"tipo_sorvete", "sabor", "cidade", "canal_venda"}:
            clean[column] = clean[column].where(clean[column].isna(), clean[column].astype(str).str.title())
        elif column in {"estado", "id_cliente"}:
            clean[column] = clean[column].where(clean[column].isna(), clean[column].astype(str).str.upper())

        changed_cells += int((before.fillna("<NA>") != clean[column].fillna("<NA>")).sum())

    return clean, changed_cells


def convert_types(df: pd.DataFrame) -> pd.DataFrame:
    """Convert core fields to analytical types."""
    typed = df.copy()
    typed["data_venda"] = pd.to_datetime(typed["data"], errors="coerce")
    typed["hora_parse"] = pd.to_datetime(typed["hora"], format="%H:%M", errors="coerce")
    typed["hora_venda"] = typed["hora_parse"].dt.strftime("%H:%M")
    typed["quantidade"] = pd.to_numeric(typed["quantidade"], errors="coerce").astype("Int64")
    typed["valor_total"] = pd.to_numeric(typed["valor_total"], errors="coerce")
    typed["promocao"] = typed["promocao"].astype("boolean")
    return typed


def fill_dimension_nulls(df: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, int]]:
    """Fill non-critical dimension nulls and keep explicit quality flags."""
    clean = df.copy()
    counts = {
        "sabor_nulo_preenchido": int(clean["sabor"].isna().sum()),
        "cidade_nula_preenchida": int(clean["cidade"].isna().sum()),
    }

    clean["flag_sabor_nao_informado"] = clean["sabor"].isna()
    clean["flag_cidade_nao_informada"] = clean["cidade"].isna()
    clean["sabor"] = clean["sabor"].fillna("Nao Informado")
    clean["cidade"] = clean["cidade"].fillna("Nao Informado")

    return clean, counts


def add_quality_flags(df: pd.DataFrame) -> pd.DataFrame:
    """Add validation flags and rejection reasons."""
    flagged = df.copy()

    flagged["flag_data_invalida"] = flagged["data_venda"].isna()
    flagged["flag_hora_invalida"] = flagged["hora_parse"].isna()
    flagged["flag_quantidade_invalida"] = flagged["quantidade"].isna() | (flagged["quantidade"] <= 0)
    flagged["flag_valor_total_nulo"] = flagged["valor_total"].isna()
    flagged["flag_valor_total_invalido"] = flagged["valor_total"].isna() | (flagged["valor_total"] <= 0)
    flagged["flag_id_transacao_duplicado"] = flagged["id_transacao"].duplicated(keep="first")
    flagged["flag_linha_duplicada"] = flagged.duplicated(subset=list(COLUMN_MAP.values()), keep="first")
    flagged["flag_tipo_sorvete_invalido"] = ~flagged["tipo_sorvete"].map(category_key).isin(EXPECTED_CATEGORY_KEYS["tipo_sorvete"])
    flagged["flag_sabor_invalido"] = ~flagged["sabor"].map(category_key).isin(EXPECTED_CATEGORY_KEYS["sabor"])
    flagged["flag_canal_venda_invalido"] = ~flagged["canal_venda"].map(category_key).isin(EXPECTED_CATEGORY_KEYS["canal_venda"])
    flagged["flag_estado_invalido"] = ~flagged["estado"].map(category_key).isin(EXPECTED_CATEGORY_KEYS["estado"])

    reasons = []
    for _, row in flagged.iterrows():
        row_reasons = []
        if row["flag_data_invalida"]:
            row_reasons.append("data_invalida")
        if row["flag_hora_invalida"]:
            row_reasons.append("hora_invalida")
        if row["flag_quantidade_invalida"]:
            row_reasons.append("quantidade_nao_positiva_ou_nula")
        if row["flag_valor_total_nulo"]:
            row_reasons.append("valor_total_nulo")
        elif row["flag_valor_total_invalido"]:
            row_reasons.append("valor_total_nao_positivo")
        if row["flag_id_transacao_duplicado"]:
            row_reasons.append("id_transacao_duplicado")
        if row["flag_linha_duplicada"]:
            row_reasons.append("linha_duplicada")
        if row["flag_tipo_sorvete_invalido"]:
            row_reasons.append("tipo_sorvete_invalido")
        if row["flag_sabor_invalido"]:
            row_reasons.append("sabor_invalido")
        if row["flag_canal_venda_invalido"]:
            row_reasons.append("canal_venda_invalido")
        if row["flag_estado_invalido"]:
            row_reasons.append("estado_invalido")
        reasons.append(";".join(row_reasons))

    flagged["motivo_exclusao"] = reasons
    flagged["registro_valido_powerbi"] = flagged["motivo_exclusao"].eq("")
    return flagged


def add_outlier_flags(df: pd.DataFrame) -> pd.DataFrame:
    """Flag relevant numeric outliers without removing them."""
    flagged = df.copy()

    valid_amounts = flagged.loc[flagged["valor_total"].gt(0), "valor_total"]
    q1 = valid_amounts.quantile(0.25)
    q3 = valid_amounts.quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr

    flagged["flag_outlier_valor_total"] = flagged["valor_total"].lt(lower_bound) | flagged["valor_total"].gt(upper_bound)
    return flagged


def add_analytical_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Create Power BI-friendly derived columns."""
    enriched = df.copy()

    enriched["ano"] = enriched["data_venda"].dt.year.astype("Int64")
    enriched["mes"] = enriched["data_venda"].dt.month.astype("Int64")
    enriched["nome_mes"] = enriched["mes"].map(MONTH_NAMES)
    enriched["ano_mes"] = enriched["data_venda"].dt.strftime("%Y-%m")
    enriched["trimestre"] = "T" + enriched["data_venda"].dt.quarter.astype("Int64").astype(str)
    enriched["dia_semana"] = enriched["data_venda"].dt.weekday.map(WEEKDAY_NAMES)
    enriched["dia_mes"] = enriched["data_venda"].dt.day.astype("Int64")
    enriched["hora"] = enriched["hora_parse"].dt.hour.astype("Int64")

    enriched["faixa_horario"] = pd.cut(
        enriched["hora"].astype(float),
        bins=[-1, 5, 11, 17, 23],
        labels=["Madrugada", "Manha", "Tarde", "Noite"],
    ).astype("string")

    enriched["ticket_transacao"] = enriched["valor_total"]
    enriched["ticket_medio"] = (enriched["valor_total"] / enriched["quantidade"].astype(float)).round(2)
    enriched["valor_unitario_estimado"] = enriched["ticket_medio"]
    enriched["promocao_label"] = enriched["promocao"].map({True: "Com Promocao", False: "Sem Promocao"})
    enriched["cliente_recorrente"] = enriched.groupby("id_cliente")["id_transacao"].transform("count").gt(1)
    enriched["qtd_transacoes_cliente"] = enriched.groupby("id_cliente")["id_transacao"].transform("count")

    return enriched


def prepare_processed_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """Select and order final analytical columns."""
    processed_columns = [
        "id_transacao",
        "data_venda",
        "ano",
        "mes",
        "nome_mes",
        "ano_mes",
        "trimestre",
        "dia_semana",
        "dia_mes",
        "hora_venda",
        "hora",
        "faixa_horario",
        "tipo_sorvete",
        "sabor",
        "quantidade",
        "valor_total",
        "ticket_transacao",
        "ticket_medio",
        "valor_unitario_estimado",
        "cidade",
        "estado",
        "canal_venda",
        "promocao",
        "promocao_label",
        "id_cliente",
        "cliente_recorrente",
        "qtd_transacoes_cliente",
        "flag_sabor_nao_informado",
        "flag_cidade_nao_informada",
        "flag_outlier_valor_total",
        "registro_valido_powerbi",
    ]

    processed = df.loc[df["registro_valido_powerbi"], processed_columns].copy()
    processed["data_venda"] = processed["data_venda"].dt.strftime("%Y-%m-%d")
    processed["quantidade"] = processed["quantidade"].astype(int)
    processed["hora"] = processed["hora"].astype(int)
    processed["ano"] = processed["ano"].astype(int)
    processed["mes"] = processed["mes"].astype(int)
    processed["dia_mes"] = processed["dia_mes"].astype(int)
    processed["qtd_transacoes_cliente"] = processed["qtd_transacoes_cliente"].astype(int)
    return processed


def build_quality_report(raw: pd.DataFrame, interim: pd.DataFrame, processed: pd.DataFrame, text_changes: int, fill_counts: dict[str, int]) -> pd.DataFrame:
    """Create a compact quality and impact report."""
    total_rows = len(raw)
    rejected = interim.loc[~interim["registro_valido_powerbi"]].copy()

    rows = [
        {"metrica": "linhas_base_bruta", "valor": total_rows, "percentual_base": 100.0},
        {"metrica": "linhas_base_processada", "valor": len(processed), "percentual_base": round(len(processed) / total_rows * 100, 2)},
        {"metrica": "linhas_removidas_base_processada", "valor": len(rejected), "percentual_base": round(len(rejected) / total_rows * 100, 2)},
        {"metrica": "celulas_texto_padronizadas", "valor": text_changes, "percentual_base": None},
        {"metrica": "sabor_nulo_preenchido", "valor": fill_counts["sabor_nulo_preenchido"], "percentual_base": round(fill_counts["sabor_nulo_preenchido"] / total_rows * 100, 2)},
        {"metrica": "cidade_nula_preenchida", "valor": fill_counts["cidade_nula_preenchida"], "percentual_base": round(fill_counts["cidade_nula_preenchida"] / total_rows * 100, 2)},
        {"metrica": "valor_total_nulo", "valor": int(interim["flag_valor_total_nulo"].sum()), "percentual_base": round(interim["flag_valor_total_nulo"].mean() * 100, 2)},
        {"metrica": "quantidade_invalida", "valor": int(interim["flag_quantidade_invalida"].sum()), "percentual_base": round(interim["flag_quantidade_invalida"].mean() * 100, 2)},
        {"metrica": "valor_total_invalido", "valor": int(interim["flag_valor_total_invalido"].sum()), "percentual_base": round(interim["flag_valor_total_invalido"].mean() * 100, 2)},
        {"metrica": "data_invalida", "valor": int(interim["flag_data_invalida"].sum()), "percentual_base": round(interim["flag_data_invalida"].mean() * 100, 2)},
        {"metrica": "hora_invalida", "valor": int(interim["flag_hora_invalida"].sum()), "percentual_base": round(interim["flag_hora_invalida"].mean() * 100, 2)},
        {"metrica": "id_transacao_duplicado", "valor": int(interim["flag_id_transacao_duplicado"].sum()), "percentual_base": round(interim["flag_id_transacao_duplicado"].mean() * 100, 2)},
        {"metrica": "tipo_sorvete_invalido", "valor": int(interim["flag_tipo_sorvete_invalido"].sum()), "percentual_base": round(interim["flag_tipo_sorvete_invalido"].mean() * 100, 2)},
        {"metrica": "sabor_invalido", "valor": int(interim["flag_sabor_invalido"].sum()), "percentual_base": round(interim["flag_sabor_invalido"].mean() * 100, 2)},
        {"metrica": "canal_venda_invalido", "valor": int(interim["flag_canal_venda_invalido"].sum()), "percentual_base": round(interim["flag_canal_venda_invalido"].mean() * 100, 2)},
        {"metrica": "estado_invalido", "valor": int(interim["flag_estado_invalido"].sum()), "percentual_base": round(interim["flag_estado_invalido"].mean() * 100, 2)},
        {"metrica": "outliers_valor_total_mantidos", "valor": int(processed["flag_outlier_valor_total"].sum()), "percentual_base": round(processed["flag_outlier_valor_total"].mean() * 100, 2) if len(processed) else 0.0},
        {"metrica": "nulos_base_processada", "valor": int(processed.isna().sum().sum()), "percentual_base": None},
    ]
    return pd.DataFrame(rows)


def clean_data(raw: pd.DataFrame) -> CleaningResult:
    """Execute all cleaning and validation steps in memory."""
    standardized = standardize_column_names(raw)
    standardized, text_changes = standardize_text_columns(standardized)
    typed = convert_types(standardized)
    filled, fill_counts = fill_dimension_nulls(typed)
    flagged = add_quality_flags(filled)
    interim = add_outlier_flags(flagged)
    enriched = add_analytical_columns(interim)
    processed = prepare_processed_dataset(enriched)
    rejected = enriched.loc[~enriched["registro_valido_powerbi"]].copy()
    quality_report = build_quality_report(raw, interim, processed, text_changes, fill_counts)

    return CleaningResult(
        raw=raw,
        interim=enriched,
        processed=processed,
        rejected=rejected,
        quality_report=quality_report,
    )


def save_outputs(result: CleaningResult) -> None:
    """Save interim, rejected, report, and processed outputs."""
    INTERIM_DIR.mkdir(parents=True, exist_ok=True)
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    result.interim.to_csv(INTERIM_OUTPUT_PATH, index=False, encoding="utf-8-sig")
    result.rejected.to_csv(REJECTED_OUTPUT_PATH, index=False, encoding="utf-8-sig")
    result.quality_report.to_csv(QUALITY_REPORT_PATH, index=False, encoding="utf-8-sig")
    result.processed.to_csv(PROCESSED_OUTPUT_PATH, index=False, encoding="utf-8-sig")


def run_pipeline(write_outputs: bool = True) -> CleaningResult:
    """Run the full cleaning pipeline."""
    raw = load_raw_data()
    result = clean_data(raw)
    if write_outputs:
        save_outputs(result)
    return result


def main() -> None:
    """Run the pipeline and print the quality report."""
    result = run_pipeline(write_outputs=True)
    print("=== Relatorio de qualidade ===")
    print(result.quality_report.to_string(index=False))
    print(f"\nBase processada: {PROCESSED_OUTPUT_PATH}")
    print(f"Registros excluidos auditaveis: {REJECTED_OUTPUT_PATH}")


if __name__ == "__main__":
    main()
