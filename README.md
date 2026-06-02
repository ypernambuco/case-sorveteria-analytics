# Case Sorveteria Analytics

Case completo de BI com 50.000 registros, tratamento com Python, modelagem para Power BI, dashboard executivo/operacional e investigacao de anomalia real na fonte de dados.

> Status: projeto finalizado, com base tratada, KPIs documentados, modelo dimensional, dashboard Power BI, apresentacao do case e documentacao tecnica.

## Prévia do Dashboard

Os screenshots reais do dashboard Power BI serao adicionados futuramente, assim que as capturas finais estiverem disponiveis no repositorio.

## Objetivo

Organizar uma base de vendas de sorvetes para apoiar uma jornada completa de analytics:

- entendimento do problema de negocio;
- analise exploratoria dos dados;
- tratamento e validacao da base;
- construcao de indicadores de desempenho;
- modelagem dimensional para Power BI;
- desenvolvimento de dashboards executivo e operacional;
- documentacao das descobertas, decisoes tecnicas e limitacoes dos dados.

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

## Dashboard Power BI

O dashboard Power BI final foi ajustado manualmente no Power BI e esta organizado em duas paginas: `Visao Executiva` e `Visao Operacional`. A documentacao dos visuais, metricas, decisoes de layout, cores e alteracoes manuais esta em [`docs/dashboard_powerbi.md`](docs/dashboard_powerbi.md).

Durante a validacao foi identificada uma reducao abrupta de registros a partir de 22/08/2025. A investigacao confirmou que a queda ja existia no dataset bruto original e nao foi causada por limpeza, transformacao, modelagem ou construcao do dashboard. Por isso, nenhum valor foi imputado artificialmente; a limitacao e seu impacto nos indicadores temporais estao documentados em [`docs/dashboard_powerbi.md`](docs/dashboard_powerbi.md#limitacao-identificada-na-base-de-dados).

## Apresentacao Do Case

A apresentacao em formato Markdown/Marp para portfolio e entrevistas esta disponivel em [`docs/apresentacao_case_sorveteria.md`](docs/apresentacao_case_sorveteria.md).

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

## Fluxo De Trabalho Executado

1. Registro de premissas e contexto do case em `docs/`.
2. Exploracao inicial da base bruta em `notebooks/`.
3. Avaliacao de estrutura, tipos de dados, nulos, duplicidades e consistencia.
4. Tratamento e auditoria de registros em `data/interim`.
5. Geracao da base tratada em `data/processed`.
6. Criacao da camada dimensional em `data/powerbi`.
7. Definicao e documentacao dos KPIs executivos.
8. Construcao do dashboard Power BI com visao executiva e operacional.
9. Investigacao e documentacao da anomalia de registros apos 22/08/2025.
10. Criacao da apresentacao do case para portfolio e entrevistas.

## KPIs Entregues

Os principais indicadores entregues no dashboard e na documentacao sao:

- receita total;
- total de vendas;
- ticket medio;
- clientes unicos;
- volume vendido;
- receita por canal;
- receita por tipo de sorvete;
- vendas por dia da semana;
- receita por faixa horaria;
- receita por trimestre;
- evolucao do volume vendido.

## Regras De Governanca

- Nao editar arquivos em `data/raw`.
- Documentar premissas antes de aplicar transformacoes relevantes.
- Separar dados brutos, intermediarios e processados.
- Manter notebooks numerados por etapa.
- Transformacoes recorrentes devem migrar de notebooks para `scripts`.
- Exportacoes finais devem ficar em `exports`.

## Evolucoes Futuras

- Carregar a base tratada em um banco SQL.
- Automatizar o pipeline de atualizacao.
- Criar testes automatizados de qualidade dos dados.
- Publicar o relatorio no Power BI Service.
- Adicionar alertas para anomalias de volume de registros.
- Evoluir analises preditivas de demanda.
