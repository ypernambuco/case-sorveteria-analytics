# Dashboard Power BI

## Objetivo

O dashboard Power BI do projeto `case-sorveteria-analytics` consolida a leitura executiva e operacional das vendas da sorveteria. O objetivo e apoiar tomada de decisão com foco em receita, volume vendido, canais, tipos de sorvete, comportamento por dia da semana e demanda por faixa horária.

O arquivo `.pbix` foi ajustado manualmente no Power BI. Este documento registra as decisões finais de layout, visuais e narrativa, sem reconstruir ou modificar automaticamente o dashboard.

## Estrutura Das Páginas

O relatório está organizado em duas páginas principais:

1. `Visao Executiva`
2. `Visao Operacional`

A separacao busca manter a primeira pagina focada em leitura rápida para lideranca e a segunda pagina focada em análises de rotina operacional.

## Pagina 1 - Visão Executiva

### Filtros Superiores

Foram mantidos os filtros superiores em formato compacto para preservar area útil e facilitar a leitura executiva:

- Mês
- Canal de Venda
- Tipo de Sorvete

### KPIs Principais

Foram mantidos os cinco indicadores principais:

- Receita Total
- Total de Vendas
- Ticket Médio
- Clientes Únicos
- Volume Vendido

Esses KPIs funcionam como abertura da narrativa, permitindo uma leitura imediata do tamanho da operação, intensidade de vendas, valor médio por transação, alcance de clientes e demanda física.

### Visual Principal

- Evolução da Receita

O grafico principal permanece dedicado a evolução da receita, pois e a leitura temporal mais relevante para apresentação executiva.

### Gráficos De Apoio

- Receita por Canal
- Receita por Tipo de Sorvete
- Vendas por Dia da Semana

Esses gráficos complementam a leitura principal ao responder quais canais geram receita, quais tipos de sorvete sustentam o faturamento e quais dias concentram maior volume de vendas.

### Decisão De Layout

O layout final foi organizado com foco executivo, priorizando leitura rápida dos principais indicadores e evitando excesso de elementos visuais. A pagina preserva a estrutura aprovada, com filtros no topo, KPIs em destaque, grafico principal em area central e gráficos de apoio na parte inferior.

## Pagina 2 - Visão Operacional

### Conjunto Final De Gráficos

A pagina operacional foi ajustada manualmente para conter os seguintes visuais:

- Vendas por Faixa Horária
- Receita por Faixa Horária
- Receita por Trimestre
- Volume por Tipo de Sorvete
- Receita por Dia da Semana
- Evolução do Volume Vendido

### Alteracoes Manuais Realizadas

- O grafico anterior de `Ticket Medio por Faixa Horaria` foi substituido por `Receita por Faixa Horaria`.
- O grafico anterior de `Vendas por Canal` foi substituido por `Receita por Dia da Semana`.
- A ordenacao do grafico `Receita por Trimestre` foi ajustada usando a coluna auxiliar `trimestre_num`, garantindo a ordem correta `T1`, `T2`, `T3`, `T4`.

### Decisão Analítica

A pagina operacional prioriza perguntas de rotina:

- em quais faixas horarias ocorrem mais vendas;
- quais faixas horarias geram mais receita;
- como a receita se distribui por trimestre;
- quais tipos de sorvete concentram maior volume;
- quais dias da semana concentram receita;
- como o volume vendido evolui ao longo do tempo.

Essa composição reduz redundancia e distribui melhor as análises entre demanda, receita, sazonalidade e volume.

## Métricas Exibidas

As principais métricas exibidas no dashboard são:

- Receita Total
- Total de Vendas
- Ticket Médio
- Clientes Únicos
- Volume Vendido
- Receita por período
- Receita por canal
- Receita por tipo de sorvete
- Receita por faixa horária
- Receita por trimestre
- Receita por dia da semana
- Volume por tipo de sorvete
- Volume vendido ao longo do tempo

## Decisões De Cores

A identidade visual foi mantida com cores consistentes e associadas ao tipo de leitura:

- azul petroleo para vendas e volume operacional;
- verde para volume e produto;
- laranja para receita operacional;
- roxo e cores de destaque para análise por tipo de sorvete na visão executiva.

As cores foram usadas com critério para reforcar a leitura sem poluir a tela, preservando uma aparencia corporativa e adequada para apresentação.

## Decisões De Layout E UX

- Manutenção dos filtros superiores na pagina executiva.
- Manutenção dos KPIs principais em destaque.
- Separacao clara entre visão executiva e visão operacional.
- Priorizacao de gráficos sem rolagem interna.
- Uso de titulos objetivos e orientados a leitura de negócio.
- Preservacao da estrutura geral já aprovada.
- Evitar excesso de cores, ícones e elementos decorativos sem funcao analítica.

## Limitação Identificada na Base de Dados

Durante a análise exploratória e a validação dos indicadores do dashboard, foi identificada uma redução abrupta no volume de registros a partir de 22/08/2025.

A investigação foi realizada comparando:

- o dataset tratado (`data/processed/vendas_sorvetes_tratado.csv`);
- o dataset bruto original (`data/raw/vendas_sorvetes.csv`).

A análise confirmou que a redução de registros já estava presente na fonte original dos dados e não foi causada pelo processo de limpeza, transformação ou modelagem realizado neste projeto.

### Evidencias observadas

Nos dias anteriores a 22/08/2025, o dataset apresentava aproximadamente 250 registros por dia. A partir dessa data, o volume passou para cerca de 10 a 30 registros diarios, representando uma redução superior a 90%.

Na validação, o dataset bruto apresentou 251 registros em 21/08/2025 e 26 registros em 22/08/2025. O dataset tratado apresentou o mesmo comportamento, com 243 registros em 21/08/2025 e 25 registros em 22/08/2025.

Como consequencia, indicadores temporais como:

- Receita;
- Volume Vendido;
- Quantidade de Vendas;

apresentam queda significativa após essa data.

### Decisão adotada

Nenhum valor foi corrigido, estimado ou imputado artificialmente.

Como não existe informação suficiente para reconstruir os registros ausentes de forma confiável, optou-se por preservar os dados originais e documentar a limitação identificada.

### Impacto na análise

Os resultados referentes ao período posterior a 22/08/2025 devem ser interpretados com cautela, pois podem não representar o comportamento real da operação.

Essa decisão foi tomada para manter a integridade analítica do projeto e evitar a introducao de vieses decorrentes de preenchimentos artificiais dos dados.

## Observacao Sobre O Arquivo Power BI

O arquivo `.pbix` foi ajustado manualmente no Power BI. Nenhuma alteração automatica no arquivo Power BI deve ser inferida a partir deste documento.

Este registro existe para documentar o estado final aprovado do dashboard e orientar manutencoes futuras sem alterar o arquivo `.pbix`.
