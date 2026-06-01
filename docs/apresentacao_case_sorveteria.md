---
marp: true
title: Case Sorveteria Analytics
description: Projeto de Analytics e Business Intelligence
paginate: true
theme: default
---

# Case Sorveteria Analytics

## Projeto de Analytics e Business Intelligence

**Autor:** Yuri Pernambuco  
**Tecnologias:** Python, Pandas, Power BI, Git, GitHub

---

# Objetivo do Projeto

Transformar uma base transacional de vendas em uma solucao analitica para tomada de decisao.

- Entender a qualidade dos dados
- Preparar uma base confiavel
- Criar KPIs executivos
- Modelar dados para Power BI
- Construir dashboards executivo e operacional
- Documentar descobertas e limitacoes

---

# Arquitetura do Projeto

```text
CSV bruto
  -> EDA
  -> Data Cleaning
  -> CSV tratado
  -> Modelagem Estrela
  -> Power BI
  -> Dashboards
```

O fluxo preserva a fonte original e gera camadas derivadas para auditoria, analise e consumo em BI.

---

# Dataset

- Base bruta: **50.000 registros**
- Base tratada: **48.491 registros validos**
- Registros removidos: **1.509**
- Taxa de aproveitamento: **96,98%**
- Periodo da base: **20/02/2025 a 20/09/2025**

Os registros removidos permanecem auditaveis em `data/interim`.

---

# Qualidade dos Dados

Problemas tratados:

- Valores nulos em campos relevantes
- Valores monetarios nao positivos
- Quantidade vendida nao positiva
- Tipos de dados inadequados para analise
- Padronizacao textual de categorias e localidades
- Necessidade de flags de auditoria

Resultado: base processada com **0 nulos finais** e **0 duplicidades em `id_transacao`**.

---

# Tratamento e Enriquecimento

Colunas e informacoes criadas:

- `ano`, `mes`, `nome_mes`, `ano_mes`
- `trimestre`
- `dia_semana`, `dia_mes`
- `hora`, `faixa_horaria`
- `valor_unitario_medio`
- `status_promocao`
- `cliente_recorrente`
- flags de qualidade e auditoria

Essas variaveis viabilizam filtros, cortes temporais e leitura operacional no Power BI.

---

# Modelagem Dimensional

Modelo recomendado em estrela:

- `fato_vendas`
- `dim_tempo`
- `dim_produtos`
- `dim_clientes`
- `dim_canais`

Beneficios:

- Separacao clara entre fatos e dimensoes
- Melhor organizacao para Power BI
- Relacionamentos simples
- Menor risco de ambiguidade nas analises

---

# Dashboard Executivo

Pagina voltada para leitura rapida da saude do negocio.

KPIs principais:

- Receita Total
- Total de Vendas
- Ticket Medio
- Clientes Unicos
- Volume Vendido

Visual principal: **Evolucao da Receita**.

---

# Dashboard Operacional

Pagina voltada para rotina de operacao e demanda.

Visuais finais:

- Vendas por Faixa Horaria
- Receita por Faixa Horaria
- Receita por Trimestre
- Volume por Tipo de Sorvete
- Receita por Dia da Semana
- Evolucao do Volume Vendido

O objetivo e responder perguntas diferentes sem repetir a mesma historia.

---

# Principais Descobertas

- Receita total: **R$ 1.366.105,34**
- Vendas validas: **48.491**
- Volume vendido: **149.400 unidades**
- Ticket medio: **R$ 28,17**
- Clientes unicos: **8.970**

Insights documentados:

- Categoria lider: **Milkshake**, com **25,9%** da receita
- Melhor trimestre: **T2**, com **49,3%** da receita
- Melhor dia: **Quinta-feira**, com **R$ 203,5 mil** e **7.215 vendas**
- Faixa de maior volume: **Tarde**, com **39,9%** das vendas

---

# Anomalia Identificada

Durante a validacao do dashboard, foi identificada queda brusca apos **22/08/2025**.

Impacto observado em:

- Receita
- Volume Vendido
- Quantidade de Vendas

Evidencias:

- Bruto: **251 registros em 21/08/2025** e **26 em 22/08/2025**
- Tratado: **243 registros em 21/08/2025** e **25 em 22/08/2025**

---

# Investigacao da Anomalia

Raciocinio de validacao:

```text
Dashboard
  -> dataset tratado
  -> dataset bruto
  -> comparacao por dia
  -> conclusao
```

Conclusao:

A anomalia ja existia na fonte original e nao foi causada por limpeza, transformacao, modelagem ou dashboard.

---

# Decisao Analitica

Decisao adotada:

- Nenhum valor foi imputado
- Nenhum dado foi estimado artificialmente
- Nenhum registro foi reconstruido sem evidencia
- A limitacao foi documentada
- O periodo posterior a 22/08/2025 deve ser interpretado com cautela

Essa decisao preserva a integridade analitica e evita vieses artificiais.

---

# Tecnologias Utilizadas

- Python
- Pandas
- Power BI
- DAX
- Git
- GitHub
- CSV
- Markdown

O projeto combina tratamento de dados, modelagem, BI e documentacao tecnica.

---

# Entregas do Projeto

- Analise exploratoria dos dados
- Regras de tratamento e governanca
- Dataset tratado
- Auditoria dos registros removidos
- Modelagem dimensional
- Dashboard executivo
- Dashboard operacional
- Documentacao tecnica
- Investigacao da anomalia da fonte

---

# Proximos Passos

Evolucoes possiveis:

- Carregar dados em banco SQL
- Automatizar atualizacao da base
- Criar monitoramento de qualidade dos dados
- Evoluir KPIs de performance
- Adicionar alertas para quedas anormais de registros
- Criar analises preditivas de demanda

---

# Encerramento

Principais aprendizados:

- ETL com rastreabilidade
- Qualidade e governanca de dados
- Modelagem dimensional
- Construcao de dashboard Power BI
- Storytelling executivo
- Investigacao analitica de anomalias
- Documentacao para manutencao e portfolio

---

# Obrigado

## Case Sorveteria Analytics

Projeto de Analytics e Business Intelligence para portfolio.
