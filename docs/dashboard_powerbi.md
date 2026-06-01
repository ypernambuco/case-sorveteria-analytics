# Dashboard Power BI

## Objetivo

O dashboard Power BI do projeto `case-sorveteria-analytics` consolida a leitura executiva e operacional das vendas da sorveteria. O objetivo e apoiar tomada de decisao com foco em receita, volume vendido, canais, tipos de sorvete, comportamento por dia da semana e demanda por faixa horaria.

O arquivo `.pbix` foi ajustado manualmente no Power BI. Este documento registra as decisoes finais de layout, visuais e narrativa, sem reconstruir ou modificar automaticamente o dashboard.

## Estrutura Das Paginas

O relatorio esta organizado em duas paginas principais:

1. `Visao Executiva`
2. `Visao Operacional`

A separacao busca manter a primeira pagina focada em leitura rapida para lideranca e a segunda pagina focada em analises de rotina operacional.

## Pagina 1 - Visao Executiva

### Filtros Superiores

Foram mantidos os filtros superiores em formato compacto para preservar area util e facilitar a leitura executiva:

- Mes
- Canal de Venda
- Tipo de Sorvete

### KPIs Principais

Foram mantidos os cinco indicadores principais:

- Receita Total
- Total de Vendas
- Ticket Medio
- Clientes Unicos
- Volume Vendido

Esses KPIs funcionam como abertura da narrativa, permitindo uma leitura imediata do tamanho da operacao, intensidade de vendas, valor medio por transacao, alcance de clientes e demanda fisica.

### Visual Principal

- Evolucao da Receita

O grafico principal permanece dedicado a evolucao da receita, pois e a leitura temporal mais relevante para apresentacao executiva.

### Graficos De Apoio

- Receita por Canal
- Receita por Tipo de Sorvete
- Vendas por Dia da Semana

Esses graficos complementam a leitura principal ao responder quais canais geram receita, quais tipos de sorvete sustentam o faturamento e quais dias concentram maior volume de vendas.

### Decisao De Layout

O layout final foi organizado com foco executivo, priorizando leitura rapida dos principais indicadores e evitando excesso de elementos visuais. A pagina preserva a estrutura aprovada, com filtros no topo, KPIs em destaque, grafico principal em area central e graficos de apoio na parte inferior.

## Pagina 2 - Visao Operacional

### Conjunto Final De Graficos

A pagina operacional foi ajustada manualmente para conter os seguintes visuais:

- Vendas por Faixa Horaria
- Receita por Faixa Horaria
- Receita por Trimestre
- Volume por Tipo de Sorvete
- Receita por Dia da Semana
- Evolucao do Volume Vendido

### Alteracoes Manuais Realizadas

- O grafico anterior de `Ticket Medio por Faixa Horaria` foi substituido por `Receita por Faixa Horaria`.
- O grafico anterior de `Vendas por Canal` foi substituido por `Receita por Dia da Semana`.
- A ordenacao do grafico `Receita por Trimestre` foi ajustada usando a coluna auxiliar `trimestre_num`, garantindo a ordem correta `T1`, `T2`, `T3`, `T4`.

### Decisao Analitica

A pagina operacional prioriza perguntas de rotina:

- em quais faixas horarias ocorrem mais vendas;
- quais faixas horarias geram mais receita;
- como a receita se distribui por trimestre;
- quais tipos de sorvete concentram maior volume;
- quais dias da semana concentram receita;
- como o volume vendido evolui ao longo do tempo.

Essa composicao reduz redundancia e distribui melhor as analises entre demanda, receita, sazonalidade e volume.

## Metricas Exibidas

As principais metricas exibidas no dashboard sao:

- Receita Total
- Total de Vendas
- Ticket Medio
- Clientes Unicos
- Volume Vendido
- Receita por periodo
- Receita por canal
- Receita por tipo de sorvete
- Receita por faixa horaria
- Receita por trimestre
- Receita por dia da semana
- Volume por tipo de sorvete
- Volume vendido ao longo do tempo

## Decisoes De Cores

A identidade visual foi mantida com cores consistentes e associadas ao tipo de leitura:

- azul petroleo para vendas e volume operacional;
- verde para volume e produto;
- laranja para receita operacional;
- roxo e cores de destaque para analise por tipo de sorvete na visao executiva.

As cores foram usadas com criterio para reforcar a leitura sem poluir a tela, preservando uma aparencia corporativa e adequada para apresentacao.

## Decisoes De Layout E UX

- Manutencao dos filtros superiores na pagina executiva.
- Manutencao dos KPIs principais em destaque.
- Separacao clara entre visao executiva e visao operacional.
- Priorizacao de graficos sem rolagem interna.
- Uso de titulos objetivos e orientados a leitura de negocio.
- Preservacao da estrutura geral ja aprovada.
- Evitar excesso de cores, icones e elementos decorativos sem funcao analitica.

## Limitacao Identificada na Base de Dados

Durante a analise exploratoria e a validacao dos indicadores do dashboard, foi identificada uma reducao abrupta no volume de registros a partir de 22/08/2025.

A investigacao foi realizada comparando:

- o dataset tratado (`data/processed/vendas_sorvetes_tratado.csv`);
- o dataset bruto original (`data/raw/vendas_sorvetes.csv`).

A analise confirmou que a reducao de registros ja estava presente na fonte original dos dados e nao foi causada pelo processo de limpeza, transformacao ou modelagem realizado neste projeto.

### Evidencias observadas

Nos dias anteriores a 22/08/2025, o dataset apresentava aproximadamente 250 registros por dia. A partir dessa data, o volume passou para cerca de 10 a 30 registros diarios, representando uma reducao superior a 90%.

Na validacao, o dataset bruto apresentou 251 registros em 21/08/2025 e 26 registros em 22/08/2025. O dataset tratado apresentou o mesmo comportamento, com 243 registros em 21/08/2025 e 25 registros em 22/08/2025.

Como consequencia, indicadores temporais como:

- Receita;
- Volume Vendido;
- Quantidade de Vendas;

apresentam queda significativa apos essa data.

### Decisao adotada

Nenhum valor foi corrigido, estimado ou imputado artificialmente.

Como nao existe informacao suficiente para reconstruir os registros ausentes de forma confiavel, optou-se por preservar os dados originais e documentar a limitacao identificada.

### Impacto na analise

Os resultados referentes ao periodo posterior a 22/08/2025 devem ser interpretados com cautela, pois podem nao representar o comportamento real da operacao.

Essa decisao foi tomada para manter a integridade analitica do projeto e evitar a introducao de vieses decorrentes de preenchimentos artificiais dos dados.

## Observacao Sobre O Arquivo Power BI

O arquivo `.pbix` foi ajustado manualmente no Power BI. Nenhuma alteracao automatica no arquivo Power BI deve ser inferida a partir deste documento.

Este registro existe para documentar o estado final aprovado do dashboard e orientar manutencoes futuras sem alterar o arquivo `.pbix`.
