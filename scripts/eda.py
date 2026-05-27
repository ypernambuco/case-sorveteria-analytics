"""Exploratory data analysis helpers for the ice cream sales case.

This module reads the immutable raw CSV and produces quality checks,
descriptive summaries, initial patterns, and business suggestions without
modifying source data.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw" / "vendas_sorvetes.csv"


EXPECTED_COLUMNS = [
    "ID_Transacao",
    "Data",
    "Hora",
    "Tipo_Sorvete",
    "Sabor",
    "Quantidade",
    "Valor_Total",
    "Cidade",
    "Estado",
    "Canal_Venda",
    "Promocao",
    "ID_Cliente",
]


def load_raw_data(path: Path = RAW_DATA_PATH) -> pd.DataFrame:
    """Load the raw sales CSV without changing the source file."""
    return pd.read_csv(path)


def summarize_structure(df: pd.DataFrame) -> dict[str, Any]:
    """Return high-level structure and memory information."""
    return {
        "linhas": int(df.shape[0]),
        "colunas": int(df.shape[1]),
        "memoria_mb": float(round(df.memory_usage(deep=True).sum() / 1024**2, 2)),
        "colunas_esperadas_presentes": EXPECTED_COLUMNS == list(df.columns),
    }


def summarize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Summarize detected types, nulls, uniqueness, and example values."""
    summary = pd.DataFrame(
        {
            "coluna": df.columns,
            "tipo_identificado": [str(dtype) for dtype in df.dtypes],
            "nulos": df.isna().sum().values,
            "percentual_nulos": (df.isna().mean().values * 100).round(2),
            "valores_unicos": df.nunique(dropna=True).values,
            "exemplo": [df[col].dropna().iloc[0] if df[col].notna().any() else None for col in df.columns],
        }
    )
    return summary


def check_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """Check duplicate rows and duplicate key-like identifiers."""
    checks = [
        {
            "checagem": "linhas totalmente duplicadas",
            "quantidade": int(df.duplicated().sum()),
            "observacao": "Duplicidade exata de todos os campos.",
        },
        {
            "checagem": "ID_Transacao duplicado",
            "quantidade": int(df["ID_Transacao"].duplicated().sum()),
            "observacao": "ID_Transacao e indicado como chave primaria no briefing.",
        },
        {
            "checagem": "ID_Cliente distintos",
            "quantidade": int(df["ID_Cliente"].nunique(dropna=True)),
            "observacao": "Clientes podem aparecer em multiplas compras.",
        },
    ]
    return pd.DataFrame(checks)


def validate_formats(df: pd.DataFrame) -> pd.DataFrame:
    """Validate basic date, time, ID, and state formats."""
    parsed_dates = pd.to_datetime(df["Data"], errors="coerce")
    parsed_times = pd.to_datetime(df["Hora"], format="%H:%M", errors="coerce")

    checks = [
        {
            "campo": "Data",
            "validacao": "parse yyyy-mm-dd",
            "registros_invalidos": int(parsed_dates.isna().sum()),
            "observacao": f"{parsed_dates.min().date()} a {parsed_dates.max().date()}",
        },
        {
            "campo": "Hora",
            "validacao": "parse HH:MM",
            "registros_invalidos": int(parsed_times.isna().sum()),
            "observacao": "Formato horario valido para todos os registros.",
        },
        {
            "campo": "Estado",
            "validacao": "UF com 2 letras maiusculas",
            "registros_invalidos": int((~df["Estado"].astype(str).str.match(r"^[A-Z]{2}$")).sum()),
            "observacao": f"{df['Estado'].nunique(dropna=True)} UFs distintas.",
        },
        {
            "campo": "ID_Cliente",
            "validacao": "padrao CLI + digitos",
            "registros_invalidos": int((~df["ID_Cliente"].astype(str).str.match(r"^CLI\d+$")).sum()),
            "observacao": "Formato esperado para identificador de cliente.",
        },
        {
            "campo": "ID_Transacao",
            "validacao": "inteiro positivo",
            "registros_invalidos": int((df["ID_Transacao"] <= 0).sum()),
            "observacao": "Chave transacional numerica.",
        },
    ]
    return pd.DataFrame(checks)


def identify_inconsistencies(df: pd.DataFrame) -> pd.DataFrame:
    """Identify records requiring business-rule validation before KPI use."""
    checks = [
        {
            "inconsistencia": "Sabor nulo",
            "quantidade": int(df["Sabor"].isna().sum()),
            "impacto_potencial": "Afeta analises de mix de sabores e ranking de produtos.",
        },
        {
            "inconsistencia": "Valor_Total nulo",
            "quantidade": int(df["Valor_Total"].isna().sum()),
            "impacto_potencial": "Afeta receita, ticket medio e analises financeiras.",
        },
        {
            "inconsistencia": "Cidade nula",
            "quantidade": int(df["Cidade"].isna().sum()),
            "impacto_potencial": "Afeta leitura geografica e desempenho regional.",
        },
        {
            "inconsistencia": "Quantidade <= 0",
            "quantidade": int((df["Quantidade"] <= 0).sum()),
            "impacto_potencial": "Pode representar devolucao, cancelamento, ajuste ou erro.",
        },
        {
            "inconsistencia": "Valor_Total <= 0",
            "quantidade": int((df["Valor_Total"] <= 0).sum()),
            "impacto_potencial": "Pode distorcer receita e margem de oportunidade.",
        },
        {
            "inconsistencia": "Valor_Total nulo com Quantidade positiva",
            "quantidade": int((df["Valor_Total"].isna() & (df["Quantidade"] > 0)).sum()),
            "impacto_potencial": "Indica venda operacional sem valor financeiro registrado.",
        },
        {
            "inconsistencia": "Quantidade positiva e Valor_Total negativo",
            "quantidade": int(((df["Quantidade"] > 0) & (df["Valor_Total"] < 0)).sum()),
            "impacto_potencial": "Pode indicar erro de sinal ou regra financeira nao documentada.",
        },
    ]
    return pd.DataFrame(checks)


def descriptive_statistics(df: pd.DataFrame) -> pd.DataFrame:
    """Generate descriptive statistics for all columns."""
    return df.describe(include="all").T


def initial_patterns(df: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """Return lightweight initial business patterns without complex charts."""
    df_dates = df.copy()
    df_dates["Data"] = pd.to_datetime(df_dates["Data"], errors="coerce")
    df_dates["Mes"] = df_dates["Data"].dt.to_period("M").astype(str)

    valid_revenue = df_dates[df_dates["Valor_Total"].notna()]

    return {
        "top_tipos_sorvete_por_registros": df["Tipo_Sorvete"].value_counts(dropna=False).head(10).to_frame("registros"),
        "top_sabores_por_registros": df["Sabor"].value_counts(dropna=False).head(10).to_frame("registros"),
        "canais_por_registros": df["Canal_Venda"].value_counts(dropna=False).to_frame("registros"),
        "promocao_por_registros": df["Promocao"].value_counts(dropna=False).to_frame("registros"),
        "receita_por_canal": valid_revenue.groupby("Canal_Venda", dropna=False)["Valor_Total"].sum().sort_values(ascending=False).to_frame("valor_total"),
        "receita_por_tipo_sorvete": valid_revenue.groupby("Tipo_Sorvete", dropna=False)["Valor_Total"].sum().sort_values(ascending=False).head(10).to_frame("valor_total"),
        "receita_por_mes": valid_revenue.groupby("Mes", dropna=False)["Valor_Total"].sum().sort_index().to_frame("valor_total"),
    }


def map_analytical_fields() -> pd.DataFrame:
    """Map columns to likely analytical roles."""
    rows = [
        {"papel_analitico": "data", "campos_provaveis": "Data, Hora"},
        {"papel_analitico": "produto", "campos_provaveis": "Tipo_Sorvete, Sabor"},
        {"papel_analitico": "canal", "campos_provaveis": "Canal_Venda"},
        {"papel_analitico": "receita", "campos_provaveis": "Valor_Total"},
        {"papel_analitico": "quantidade", "campos_provaveis": "Quantidade"},
        {"papel_analitico": "loja", "campos_provaveis": "nao identificado explicitamente"},
        {"papel_analitico": "regiao", "campos_provaveis": "Cidade, Estado"},
        {"papel_analitico": "vendedor", "campos_provaveis": "nao identificado explicitamente"},
        {"papel_analitico": "cliente", "campos_provaveis": "ID_Cliente"},
        {"papel_analitico": "promocao", "campos_provaveis": "Promocao"},
    ]
    return pd.DataFrame(rows)


def suggest_executive_kpis() -> pd.DataFrame:
    """Suggest executive KPIs for later validated analysis."""
    rows = [
        {
            "kpi": "Receita Total",
            "formula_sugerida": "soma de Valor_Total validado",
            "uso_executivo": "Medir tamanho do negocio e evolucao geral.",
        },
        {
            "kpi": "Ticket Medio",
            "formula_sugerida": "receita valida / numero de transacoes validas",
            "uso_executivo": "Avaliar monetizacao media por venda.",
        },
        {
            "kpi": "Quantidade Vendida",
            "formula_sugerida": "soma de Quantidade validada",
            "uso_executivo": "Medir volume e demanda operacional.",
        },
        {
            "kpi": "Receita Por Canal",
            "formula_sugerida": "soma de Valor_Total por Canal_Venda",
            "uso_executivo": "Priorizar canais com maior retorno.",
        },
        {
            "kpi": "Receita Por Produto/Sabor",
            "formula_sugerida": "soma de Valor_Total por Tipo_Sorvete e Sabor",
            "uso_executivo": "Identificar mix de produtos mais relevante.",
        },
        {
            "kpi": "Impacto De Promocao",
            "formula_sugerida": "comparar receita e ticket medio entre Promocao=True/False",
            "uso_executivo": "Avaliar se promocoes geram incremento real.",
        },
        {
            "kpi": "Receita Por Regiao",
            "formula_sugerida": "soma de Valor_Total por Estado/Cidade",
            "uso_executivo": "Mapear mercados prioritarios.",
        },
        {
            "kpi": "Clientes Recorrentes",
            "formula_sugerida": "clientes com mais de uma transacao / clientes totais",
            "uso_executivo": "Entender recompra e fidelizacao.",
        },
    ]
    return pd.DataFrame(rows)


def suggest_revenue_insights(df: pd.DataFrame) -> pd.DataFrame:
    """Suggest early revenue-oriented hypotheses based on raw patterns."""
    valid_revenue = df[df["Valor_Total"].notna()]
    top_channel = valid_revenue.groupby("Canal_Venda")["Valor_Total"].sum().idxmax()
    top_product = valid_revenue.groupby("Tipo_Sorvete")["Valor_Total"].sum().idxmax()
    promo_revenue = {
        str(key): round(value, 2)
        for key, value in valid_revenue.groupby("Promocao")["Valor_Total"].mean().to_dict().items()
    }

    rows = [
        {
            "tema": "Canal de venda",
            "hipotese": f"O canal {top_channel} aparece como candidato a alavanca de receita.",
            "proxima_validacao": "Comparar receita, volume, ticket medio e recorrencia por canal apos tratar dados invalidos.",
        },
        {
            "tema": "Mix de produtos",
            "hipotese": f"{top_product} aparece como categoria candidata a destaque comercial.",
            "proxima_validacao": "Avaliar receita e quantidade por tipo e sabor, separando promocoes e sazonalidade.",
        },
        {
            "tema": "Promocoes",
            "hipotese": f"Ticket medio bruto por promocao: {promo_revenue}.",
            "proxima_validacao": "Medir se promocao aumenta receita incremental ou apenas desloca margem/ticket.",
        },
        {
            "tema": "Qualidade de dados",
            "hipotese": "Valores nulos e nao positivos podem distorcer a leitura de receita.",
            "proxima_validacao": "Definir regra de negocio para cancelamentos, devolucoes, erros e vendas sem valor.",
        },
        {
            "tema": "Geografia",
            "hipotese": "Cidade e Estado permitem priorizar mercados, mas Cidade possui nulos e alta cardinalidade.",
            "proxima_validacao": "Validar consistencia geografica antes de recomendar expansao regional.",
        },
    ]
    return pd.DataFrame(rows)


def run_eda(path: Path = RAW_DATA_PATH) -> dict[str, Any]:
    """Run the complete initial EDA and return all outputs."""
    df = load_raw_data(path)
    return {
        "dataframe": df,
        "estrutura": summarize_structure(df),
        "colunas": summarize_columns(df),
        "duplicidades": check_duplicates(df),
        "formatos": validate_formats(df),
        "inconsistencias": identify_inconsistencies(df),
        "estatisticas": descriptive_statistics(df),
        "padroes": initial_patterns(df),
        "campos_analiticos": map_analytical_fields(),
        "kpis_sugeridos": suggest_executive_kpis(),
        "insights_receita": suggest_revenue_insights(df),
    }


def main() -> None:
    """Print a concise console version of the initial EDA."""
    results = run_eda()

    print("=== Estrutura ===")
    print(results["estrutura"])

    print("\n=== Colunas ===")
    print(results["colunas"].to_string(index=False))

    print("\n=== Duplicidades ===")
    print(results["duplicidades"].to_string(index=False))

    print("\n=== Validacao De Formatos ===")
    print(results["formatos"].to_string(index=False))

    print("\n=== Inconsistencias ===")
    print(results["inconsistencias"].to_string(index=False))

    print("\n=== KPIs Executivos Sugeridos ===")
    print(results["kpis_sugeridos"].to_string(index=False))

    print("\n=== Possiveis Insights De Receita ===")
    print(results["insights_receita"].to_string(index=False))


if __name__ == "__main__":
    main()
