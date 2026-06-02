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

# Contexto do Negocio

A sorveteria precisava transformar uma base transacional em informacao gerencial para apoiar decisoes de crescimento.

Pergunta central:

**Como aumentar receita a partir do comportamento de vendas de 2025?**

Dimensoes analisadas:

- produtos e mix de vendas
- canais comerciais
- sazonalidade e horarios
- comportamento de clientes
- limitacoes da fonte de dados

---

# Objetivo da Analise

Criar uma base confiavel e indicadores executivos para entender desempenho comercial, eficiencia operacional e oportunidades de crescimento.

Entregas analiticas:

- entender a qualidade dos dados
- preparar uma base confiavel
- criar KPIs executivos
- modelar dados para Power BI
- construir dashboards executivo e operacional
- documentar descobertas, decisoes e limitacoes

---

# Dataset

- Base bruta: **50.000 registros**
- Base tratada: **48.491 registros validos**
- Registros removidos: **1.509**
- Taxa de aproveitamento: **96,98%**
- Periodo da base: **20/02/2025 a 20/09/2025**
- Granularidade: **uma linha por transacao de venda**

Fonte bruta: `data/raw/vendas_sorvetes.csv`  
Base tratada: `data/processed/vendas_sorvetes_tratado.csv`

---

# Problemas Encontrados Nos Dados

A base original tinha problemas que poderiam distorcer receita, volume, ticket medio, filtros e leitura operacional.

Principais pontos tratados:

- nulos em campos como `sabor`, `cidade` e `Valor_Total`
- valores monetarios nao positivos
- quantidade vendida nao positiva
- inconsistencias textuais e espacos extras
- nomes de colunas pouco adequados para Power BI e DAX
- outliers financeiros que exigiam rastreabilidade

---

# Processo de Tratamento

O tratamento preservou a fonte original e separou as camadas de trabalho.

```text
Raw -> Interim -> Processed -> Power BI
```

Decisoes aplicadas:

- arquivos em `data/raw` mantidos como fonte imutavel
- registros removidos preservados em `data/interim`
- nulos em `sabor` e `cidade` preenchidos como `Nao Informado`
- flags criadas para manter rastreabilidade
- valores e quantidades nao positivos removidos da base processada

---

# Qualidade dos Dados Apos Tratamento

A base processada ficou consistente e pronta para analises, KPIs e Power BI.

Resultados finais:

- **48.491 registros validos** mantidos
- **31 colunas** na base processada
- **0 nulos finais**
- **0 duplicidades em `id_transacao`**
- **0 registros com `quantidade_vendida <= 0`**
- **0 registros com `receita_transacao <= 0`**
- **Data Quality Score: 99,25**

---

# Modelagem Dimensional

O modelo foi organizado em estrela para reduzir ambiguidade e facilitar filtros, medidas e dashboards.

Modelo recomendado:

- `fato_vendas`
- `dim_tempo`
- `dim_produtos`
- `dim_clientes`
- `dim_canais`

Relacionamentos:

- dimensoes em relacao **1 para muitos** com `fato_vendas`
- direcao de filtro simples
- sem muitos-para-muitos nesta versao

---

# Dashboard Executivo

Pagina voltada para leitura rapida da saude do negocio.

Elementos principais:

- filtros superiores: mes, canal de venda e tipo de sorvete
- KPIs: Receita Total, Total de Vendas, Ticket Medio, Clientes Unicos e Volume Vendido
- visual principal: **Evolucao da Receita**
- graficos de apoio: Receita por Canal, Receita por Tipo de Sorvete e Vendas por Dia da Semana

A pagina prioriza leitura executiva, clareza e poucos elementos visuais.

---

# Dashboard Operacional

Pagina voltada para rotina de operacao, demanda e sazonalidade.

Visuais finais:

- Vendas por Faixa Horaria
- Receita por Faixa Horaria
- Receita por Trimestre
- Volume por Tipo de Sorvete
- Receita por Dia da Semana
- Evolucao do Volume Vendido

O objetivo e responder perguntas operacionais sem repetir a mesma historia da visao executiva.

---

# Principais Descobertas

- Receita total: **R$ 1.366.105,34**
- Vendas validas: **48.491**
- Volume vendido: **149.400 unidades**
- Ticket medio: **R$ 28,17**
- Clientes unicos: **8.970**

Insights documentados:

- Milkshake lidera com **25,9%** da receita
- canais Parceiro, App e Loja Fisica ficam equilibrados em torno de um terco da receita
- clientes recorrentes representam **97,6%** da base analisada
- Tarde concentra **39,9%** das vendas
- promocoes representam **50,1%** das vendas, mas apenas **45,4%** da receita

---

# Investigacao da Anomalia pos-22/08/2025

Durante a validacao do dashboard, foi identificada queda brusca de registros apos **22/08/2025**.

Evidencias:

- Bruto: **251 registros em 21/08/2025** e **26 em 22/08/2025**
- Tratado: **243 registros em 21/08/2025** e **25 em 22/08/2025**

Conclusao:

A anomalia ja existia na fonte original e nao foi causada por limpeza, transformacao, modelagem ou dashboard.

Decisao: nenhum valor foi imputado, estimado ou reconstruido artificialmente.

---

# Recomendacoes de Negocio

As oportunidades mais claras estao em aumentar ticket, revisar promocoes, proteger a categoria Milkshake, explorar CRM e ajustar operacao por horario.

Recomendacoes:

- revisar promocoes: ticket com promocao de **R$ 25,55** contra **R$ 30,80** sem promocao
- trocar desconto amplo por combos, beneficios progressivos e ofertas condicionadas a quantidade minima
- tratar Milkshake como categoria ancora, pois responde por **25,9%** da receita
- usar o intervalo mediano de **20 dias** entre compras para campanhas de CRM
- diferenciar operacao por horario: tarde como janela de volume e noite como janela de valor
- fortalecer gestao omnicanal, ja que os canais apresentam participacao equilibrada

---

# Conclusao

O projeto transformou uma base transacional em um ativo analitico confiavel para tomada de decisao.

Resultados do case:

- fonte bruta preservada
- transformacoes rastreaveis
- base final pronta para analises, KPIs e Power BI
- modelo dimensional organizado
- dashboards separados entre leitura executiva e operacional
- anomalia pos-22/08/2025 investigada na origem
- recomendacoes de negocio baseadas em evidencias documentadas

---

# Obrigado

## Case Sorveteria Analytics

Projeto de Analytics e Business Intelligence para portfolio.
