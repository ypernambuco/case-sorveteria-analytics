# Case Sorveteria Analytics

Projeto profissional de analise de dados para uma sorveteria, com foco em vendas de 2025, aumento de receita, geracao de KPIs, dashboard executivo em Power BI e storytelling de negocio.

> Status: camada analitica tratada e documentada, pronta para consumo em analises, KPIs e Power BI.

## Objetivo

Organizar uma base de vendas de sorvetes ainda nao tratada para apoiar uma jornada completa de analytics:

- entendimento do problema de negocio;
- analise exploratoria dos dados;
- tratamento e validacao da base;
- construcao de indicadores de desempenho;
- desenvolvimento de dashboard executivo;
- criacao de apresentacao com recomendacoes de negocio.

## Pergunta De Negocio

Como a sorveteria pode aumentar receita a partir do comportamento de vendas de 2025, considerando produtos, sazonalidade, canais, regioes, mix de vendas e oportunidades operacionais?

## Estrutura Do Projeto

```text
case-sorveteria-analytics/
|-- assets/
|-- data/
|   |-- raw/
|   |-- interim/
|   `-- processed/
|-- docs/
|-- exports/
|   |-- figures/
|   |-- tables/
|   `-- powerbi/
|-- notebooks/
|-- powerbi/
|-- presentation/
|-- scripts/
|-- .gitignore
|-- requirements.txt
`-- README.md
```

## Descricao Das Pastas

- `data/raw`: dados originais, sem alteracao. Arquivos desta pasta devem ser tratados como fonte imutavel.
- `data/interim`: dados intermediarios gerados durante limpeza, padronizacao e validacao.
- `data/processed`: bases finais tratadas, prontas para analise, KPIs e Power BI.
- `notebooks`: exploracao, investigacao de qualidade dos dados e prototipos analiticos.
- `scripts`: rotinas reutilizaveis para ingestao, limpeza, transformacao e validacao.
- `powerbi`: arquivos do dashboard, modelo semantico, medidas DAX e documentacao visual.
- `presentation`: materiais da apresentacao executiva e storytelling final.
- `docs`: briefing, premissas, dicionario de dados, regras de negocio e documentos de referencia.
- `exports`: tabelas, graficos e artefatos finais exportados.
- `assets`: imagens, logos, icones e recursos visuais.

## Dados De Entrada

Arquivo principal:

- `data/raw/vendas_sorvetes.csv`

Documento de referencia:

- `docs/case_sorveteria.pptx`

Os arquivos originais nao devem ser alterados. Qualquer transformacao deve gerar novos arquivos em `data/interim` ou `data/processed`.

## Base Analitica Atual

Arquivo principal para analises e Power BI:

- `data/processed/vendas_sorvetes_tratado.csv`

Resumo da camada processada:

- 48.491 registros validos;
- 31 colunas;
- 0 nulos finais;
- 0 duplicidades em `id_transacao`;
- `mes` e `hora` mantidos como nomes aprovados;
- principais campos de metricas: `receita_transacao`, `quantidade_vendida`, `valor_transacao` e `valor_unitario_medio`.

## Ambiente

Criar e ativar o ambiente virtual no Windows:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Neste workspace, a `.venv` ja foi criada e as bibliotecas principais foram instaladas.

Bibliotecas iniciais:

- `pandas`
- `numpy`
- `matplotlib`
- `jupyter`
- `openpyxl`

## Fluxo De Trabalho Sugerido

1. Registrar premissas e contexto do case em `docs/`.
2. Criar uma exploracao inicial em `notebooks/`, lendo apenas `data/raw/vendas_sorvetes.csv`.
3. Avaliar estrutura, tipos de dados, nulos, duplicidades e consistencia dos campos.
4. Salvar bases intermediarias em `data/interim`.
5. Gerar base tratada final em `data/processed`.
6. Definir KPIs e regras de negocio em `docs/`.
7. Construir dashboard executivo em `powerbi`.
8. Exportar graficos e tabelas relevantes em `exports`.
9. Consolidar storytelling e recomendacoes em `presentation`.

## KPIs Planejados

Os KPIs serao definidos apos a exploracao e validacao dos dados. Possiveis indicadores:

- receita total;
- ticket medio;
- quantidade vendida;
- margem ou lucro, se houver dados disponiveis;
- receita por produto;
- receita por canal;
- sazonalidade mensal;
- ranking de sabores/produtos;
- desempenho por loja, regiao ou vendedor, se houver esses campos.

## Regras De Governanca

- Nao editar arquivos em `data/raw`.
- Documentar premissas antes de aplicar transformacoes relevantes.
- Separar dados brutos, intermediarios e processados.
- Manter notebooks numerados por etapa.
- Transformacoes recorrentes devem migrar de notebooks para `scripts`.
- Exportacoes finais devem ficar em `exports`.

## Proximas Etapas

- Criar notebook de exploracao inicial.
- Levantar dicionario de dados.
- Identificar problemas de qualidade da base.
- Planejar KPIs executivos.
- Desenhar wireframe do dashboard em Power BI.
