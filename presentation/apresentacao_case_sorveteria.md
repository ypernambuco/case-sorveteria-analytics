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

# Contexto do Negócio

A sorveteria precisava transformar uma base transacional em informação gerencial para apoiar decisões de crescimento.

Pergunta central:

**Como aumentar receita a partir do comportamento de vendas de 2025?**

Dimensões analisadas:

- produtos e mix de vendas
- canais comerciais
- sazonalidade e horários
- comportamento de clientes
- limitações da fonte de dados

---

# Objetivo da Análise

Criar uma base confiável e indicadores executivos para entender desempenho comercial, eficiência operacional e oportunidades de crescimento.

Entregas analíticas:

- entender a qualidade dos dados
- preparar uma base confiável
- criar KPIs executivos
- modelar dados para Power BI
- construir dashboards executivo e operacional
- documentar descobertas, decisões e limitações

---

# Dataset

- Base bruta: **50.000 registros**
- Base tratada: **48.491 registros válidos**
- Registros removidos: **1.509**
- Taxa de aproveitamento: **96,98%**
- Período da base: **20/02/2025 a 20/09/2025**
- Granularidade: **uma linha por transação de venda**

Fonte bruta: `data/raw/vendas_sorvetes.csv`  
Base tratada: `data/processed/vendas_sorvetes_tratado.csv`

---

# Problemas Encontrados Nos Dados

A base original tinha problemas que poderiam distorcer receita, volume, ticket médio, filtros e leitura operacional.

Principais pontos tratados:

- nulos em campos como `sabor`, `cidade` e `Valor_Total`
- valores monetarios não positivos
- quantidade vendida não positiva
- inconsistencias textuais e espacos extras
- nomes de colunas pouco adequados para Power BI e DAX
- outliers financeiros que exigiam rastreabilidade

---

# Processo de Tratamento

O tratamento preservou a fonte original e separou as camadas de trabalho.

```text
Raw -> Interim -> Processed -> Power BI
```

Decisões aplicadas:

- arquivos em `data/raw` mantidos como fonte imutável
- registros removidos preservados em `data/interim`
- nulos em `sabor` e `cidade` preenchidos como `Nao Informado`
- flags criadas para manter rastreabilidade
- valores e quantidades não positivos removidos da base processada

---

# Qualidade dos Dados Após Tratamento

A base processada ficou consistente e pronta para análises, KPIs e Power BI.

Resultados finais:

- **48.491 registros válidos** mantidos
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

- dimensões em relacao **1 para muitos** com `fato_vendas`
- direcao de filtro simples
- sem muitos-para-muitos nesta versão

---

# Dashboard Executivo

Pagina voltada para leitura rápida da saúde do negócio.

![Dashboard Executivo](assets/dashboard_executivo.png)

Elementos principais:

- filtros superiores: mês, canal de venda e tipo de sorvete
- KPIs: Receita Total, Total de Vendas, Ticket Médio, Clientes Únicos e Volume Vendido
- visual principal: **Evolução da Receita**
- gráficos de apoio: Receita por Canal, Receita por Tipo de Sorvete e Vendas por Dia da Semana

A pagina prioriza leitura executiva, clareza e poucos elementos visuais.

---

# Dashboard Operacional

Pagina voltada para rotina de operação, demanda e sazonalidade.

![Dashboard Operacional](assets/dashboard_operacional.png)

Visuais finais:

- Vendas por Faixa Horária
- Receita por Faixa Horária
- Receita por Trimestre
- Volume por Tipo de Sorvete
- Receita por Dia da Semana
- Evolução do Volume Vendido

O objetivo e responder perguntas operacionais sem repetir a mesma história da visão executiva.

---

# Principais Descobertas

![Top Produtos](assets/top_produtos.png)

- Receita total: **R$ 1.366.105,34**
- Vendas válidas: **48.491**
- Volume vendido: **149.400 unidades**
- Ticket médio: **R$ 28,17**
- Clientes únicos: **8.970**

Insights documentados:

- Milkshake lidera com **25,9%** da receita
- canais Parceiro, App e Loja Física ficam equilibrados em torno de um terço da receita
- clientes recorrentes representam **97,6%** da base analisada
- Tarde concentra **39,9%** das vendas
- promoções representam **50,1%** das vendas, mas apenas **45,4%** da receita

---

# Investigação da Anomalia pos-22/08/2025

Durante a validação do dashboard, foi identificada queda brusca de registros após **22/08/2025**.

![Receita ao Longo do Tempo](assets/receita_temporal.png)

Evidencias:

- Bruto: **251 registros em 21/08/2025** e **26 em 22/08/2025**
- Tratado: **243 registros em 21/08/2025** e **25 em 22/08/2025**

Conclusão:

A anomalia já existia na fonte original e não foi causada por limpeza, transformação, modelagem ou dashboard.

Decisão: nenhum valor foi imputado, estimado ou reconstruído artificialmente.

---

# Recomendacoes de Negócio

As oportunidades mais claras estão em aumentar ticket, revisar promoções, proteger a categoria Milkshake, explorar CRM e ajustar operação por horário.

Recomendacoes:

- revisar promoções: ticket com promoção de **R$ 25,55** contra **R$ 30,80** sem promoção
- trocar desconto amplo por combos, benefícios progressivos e ofertas condicionadas a quantidade minima
- tratar Milkshake como categoria âncora, pois responde por **25,9%** da receita
- usar o intervalo mediano de **20 dias** entre compras para campanhas de CRM
- diferenciar operação por horário: tarde como janela de volume e noite como janela de valor
- fortalecer gestão omnicanal, já que os canais apresentam participação equilibrada

---

# Conclusão

O projeto transformou uma base transacional em um ativo analítico confiável para tomada de decisão.

Resultados do case:

- fonte bruta preservada
- transformações rastreaveis
- base final pronta para análises, KPIs e Power BI
- modelo dimensional organizado
- dashboards separados entre leitura executiva e operacional
- anomalia pos-22/08/2025 investigada na origem
- recomendações de negócio baseadas em evidências documentadas

---

# Obrigado

## Case Sorveteria Analytics

Projeto de Analytics e Business Intelligence para portfólio.
