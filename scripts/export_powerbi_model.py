from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
INPUT_PATH = ROOT / "data" / "processed" / "vendas_sorvetes_tratado.csv"
OUTPUT_DIR = ROOT / "data" / "powerbi"


def mode_or_first(series: pd.Series):
    modes = series.dropna().mode()
    if not modes.empty:
        return modes.iloc[0]
    values = series.dropna()
    return values.iloc[0] if not values.empty else None


def build_dim_tempo(df: pd.DataFrame) -> pd.DataFrame:
    nomes_meses = {
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
    dias_semana = {
        1: "Segunda",
        2: "Terca",
        3: "Quarta",
        4: "Quinta",
        5: "Sexta",
        6: "Sabado",
        7: "Domingo",
    }

    datas = pd.date_range(df["data_venda"].min(), df["data_venda"].max(), freq="D")
    dim = pd.DataFrame({"data_venda": datas})
    dim["ano"] = dim["data_venda"].dt.year
    dim["mes"] = dim["data_venda"].dt.month
    dim["nome_mes"] = dim["mes"].map(nomes_meses)
    dim["ano_mes"] = dim["data_venda"].dt.strftime("%Y-%m")
    dim["ordem_ano_mes"] = dim["ano"] * 100 + dim["mes"]
    dim["trimestre_numero"] = dim["data_venda"].dt.quarter
    dim["trimestre"] = "T" + dim["trimestre_numero"].astype(str)
    dim["dia_mes"] = dim["data_venda"].dt.day
    dim["numero_dia_semana"] = dim["data_venda"].dt.weekday + 1
    dim["dia_semana"] = dim["numero_dia_semana"].map(dias_semana)
    dim["fim_de_semana"] = dim["numero_dia_semana"].isin([6, 7])
    dim["data_venda"] = dim["data_venda"].dt.strftime("%Y-%m-%d")
    return dim


def build_model() -> dict[str, pd.DataFrame]:
    df = pd.read_csv(INPUT_PATH)
    df["data_venda"] = pd.to_datetime(df["data_venda"])

    produtos = (
        df[["tipo_sorvete", "sabor", "flag_sabor_nao_informado"]]
        .drop_duplicates()
        .sort_values(["tipo_sorvete", "sabor"])
        .reset_index(drop=True)
    )
    produtos.insert(0, "id_produto", range(1, len(produtos) + 1))
    produtos["produto"] = produtos["tipo_sorvete"] + " - " + produtos["sabor"]

    canais = (
        df[["canal_venda"]]
        .drop_duplicates()
        .sort_values("canal_venda")
        .reset_index(drop=True)
    )
    canais.insert(0, "id_canal", range(1, len(canais) + 1))
    canais["tipo_canal"] = canais["canal_venda"].map(
        {
            "App": "Digital proprio",
            "Parceiro": "Digital parceiro",
            "Loja Física": "Presencial",
        }
    ).fillna("Nao classificado")

    fato = df.merge(produtos[["id_produto", "tipo_sorvete", "sabor"]], on=["tipo_sorvete", "sabor"], how="left")
    fato = fato.merge(canais[["id_canal", "canal_venda"]], on="canal_venda", how="left")

    fato_vendas = fato[
        [
            "id_transacao",
            "data_venda",
            "id_produto",
            "id_cliente",
            "id_canal",
            "quantidade_vendida",
            "receita_transacao",
            "valor_transacao",
            "valor_unitario_medio",
            "promocao",
            "status_promocao",
            "hora_venda",
            "hora",
            "faixa_horaria",
            "flag_outlier_valor_total",
            "flag_registro_valido_powerbi",
        ]
    ].copy()
    fato_vendas["data_venda"] = fato_vendas["data_venda"].dt.strftime("%Y-%m-%d")

    cliente_base = (
        df.groupby("id_cliente", as_index=False)
        .agg(
            quantidade_transacoes_cliente=("id_transacao", "count"),
            primeira_data_compra=("data_venda", "min"),
            ultima_data_compra=("data_venda", "max"),
            receita_total_cliente=("receita_transacao", "sum"),
            volume_total_cliente=("quantidade_vendida", "sum"),
            cidade_principal=("cidade", mode_or_first),
            estado_principal=("estado", mode_or_first),
            canal_preferencial=("canal_venda", mode_or_first),
            categoria_preferencial=("tipo_sorvete", mode_or_first),
        )
    )
    cliente_base["cliente_recorrente"] = cliente_base["quantidade_transacoes_cliente"] > 1
    cliente_base["dias_entre_primeira_ultima_compra"] = (
        cliente_base["ultima_data_compra"] - cliente_base["primeira_data_compra"]
    ).dt.days
    cliente_base["ticket_medio_cliente"] = (
        cliente_base["receita_total_cliente"] / cliente_base["quantidade_transacoes_cliente"]
    ).round(2)

    cliente_base["faixa_frequencia_cliente"] = pd.cut(
        cliente_base["quantidade_transacoes_cliente"],
        bins=[0, 1, 3, 6, 10, float("inf")],
        labels=["1 compra", "2 a 3 compras", "4 a 6 compras", "7 a 10 compras", "Mais de 10 compras"],
        right=True,
    )
    cliente_base["segmento_valor_cliente"] = pd.qcut(
        cliente_base["receita_total_cliente"],
        q=3,
        labels=["Baixo valor", "Medio valor", "Alto valor"],
        duplicates="drop",
    )

    dim_clientes = cliente_base[
        [
            "id_cliente",
            "cliente_recorrente",
            "quantidade_transacoes_cliente",
            "faixa_frequencia_cliente",
            "segmento_valor_cliente",
            "primeira_data_compra",
            "ultima_data_compra",
            "dias_entre_primeira_ultima_compra",
            "receita_total_cliente",
            "volume_total_cliente",
            "ticket_medio_cliente",
            "cidade_principal",
            "estado_principal",
            "canal_preferencial",
            "categoria_preferencial",
        ]
    ].copy()
    dim_clientes["primeira_data_compra"] = dim_clientes["primeira_data_compra"].dt.strftime("%Y-%m-%d")
    dim_clientes["ultima_data_compra"] = dim_clientes["ultima_data_compra"].dt.strftime("%Y-%m-%d")

    dim_produtos = produtos[
        ["id_produto", "produto", "tipo_sorvete", "sabor", "flag_sabor_nao_informado"]
    ].copy()
    dim_canais = canais[["id_canal", "canal_venda", "tipo_canal"]].copy()
    dim_tempo = build_dim_tempo(df)

    return {
        "fato_vendas": fato_vendas,
        "dim_produtos": dim_produtos,
        "dim_clientes": dim_clientes,
        "dim_canais": dim_canais,
        "dim_tempo": dim_tempo,
    }


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    tables = build_model()
    for name, table in tables.items():
        table.to_csv(OUTPUT_DIR / f"{name}.csv", index=False, encoding="utf-8-sig")

    print(f"Arquivos gerados em: {OUTPUT_DIR}")
    for name, table in tables.items():
        print(f"{name}: {len(table):,} linhas | {len(table.columns)} colunas")


if __name__ == "__main__":
    main()
