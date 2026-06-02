# Dicionário De Dados Processado

Fonte: `data/processed/vendas_sorvetes_tratado.csv`  
Origem bruta: `data/raw/vendas_sorvetes.csv`  
Status: base analítica estável para análises, KPIs e Power BI.

## Resumo

- Linhas: 48.491
- Colunas: 31
- Nulos finais: 0
- Duplicidade em `id_transacao`: 0
- Registros com `quantidade_vendida <= 0`: 0
- Registros com `receita_transacao <= 0`: 0

## Colunas

| Coluna | Tipo esperado | Descrição | Observacoes |
|---|---|---|---|
| `id_transacao` | inteiro | Identificador único da transação. | Chave de venda; sem duplicidade na base final. |
| `data_venda` | data | Data da venda. | Formato `YYYY-MM-DD`, pronta para relacionamento com calendário. |
| `ano` | inteiro | Ano da venda. | Mantido para filtros e agrupamentos simples. |
| `mes` | inteiro | Numero do mês da venda. | Nome aprovado; usado para ordenacao de `nome_mes`. |
| `nome_mes` | texto | Nome do mês da venda. | Campo amigavel para visuais. |
| `ano_mes` | texto | Combinacao ano-mês da venda. | Util para eixo temporal mensal. |
| `trimestre` | texto | Trimestre da venda. | Valores como `T1`, `T2`, `T3`. |
| `dia_semana` | texto | Dia da semana da venda. | Campo amigavel para análise semanal. |
| `dia_mes` | inteiro | Dia do mês da venda. | Apoia análises de calendário. |
| `hora_venda` | texto | Hora original da venda. | Formato `HH:MM`, em GMT-3 conforme briefing. |
| `hora` | inteiro | Hora inteira da venda. | Nome aprovado; usado para agrupamentos horários. |
| `faixa_horaria` | texto | Faixa do dia da venda. | Madrugada, Manha, Tarde ou Noite. |
| `tipo_sorvete` | texto | Categoria do sorvete vendido. | Dimensão de produto. |
| `sabor` | texto | Sabor do item vendido. | Nulos da origem foram preenchidos como `Nao Informado`. |
| `quantidade_vendida` | inteiro | Quantidade vendida na transação. | Apenas valores positivos na base final. |
| `receita_transacao` | decimal | Receita válida da transação. | Apenas valores positivos na base final. |
| `valor_transacao` | decimal | Valor monetario total da transação. | Mantido como coluna semântica de valor da venda. |
| `valor_unitario_medio` | decimal | Receita média por unidade vendida. | Calculado como `receita_transacao / quantidade_vendida`. |
| `valor_unitario_estimado` | decimal | Valor unitário estimado. | Mesmo conceito de `valor_unitario_medio`; mantido por rastreabilidade da etapa anterior. |
| `cidade` | texto | Cidade da venda. | Nulos da origem foram preenchidos como `Nao Informado`. |
| `estado` | texto | UF da venda. | Sigla da unidade federativa. |
| `canal_venda` | texto | Canal comercial da venda. | App, Parceiro ou Loja Física. |
| `promocao` | booleano | Indica se houve promoção. | Campo booleano técnico. |
| `status_promocao` | texto | Rotulo de promoção. | `Com Promocao` ou `Sem Promocao`. |
| `id_cliente` | texto | Identificador do cliente. | Permite recorrência e contagem distinta. |
| `cliente_recorrente` | booleano | Indica cliente com mais de uma transação. | Derivado da contagem de transações por cliente. |
| `quantidade_transacoes_cliente` | inteiro | Numero de transações do cliente na base final. | Apoia segmentação de recorrência. |
| `flag_sabor_nao_informado` | booleano | Indica sabor ausente na origem. | Mantém rastreabilidade do preenchimento. |
| `flag_cidade_nao_informada` | booleano | Indica cidade ausente na origem. | Mantém rastreabilidade do preenchimento. |
| `flag_outlier_valor_total` | booleano | Indica outlier financeiro mantido. | Outliers foram sinalizados, não removidos. |
| `flag_registro_valido_powerbi` | booleano | Indica registro válido para Power BI. | Todos os registros da base processed estão marcados como válidos. |

## Medidas DAX Recomendadas

```DAX
Receita Total = SUM(vendas_sorvetes_tratado[receita_transacao])

Quantidade Vendida = SUM(vendas_sorvetes_tratado[quantidade_vendida])

Transacoes = DISTINCTCOUNT(vendas_sorvetes_tratado[id_transacao])

Ticket Medio = DIVIDE([Receita Total], [Transacoes])
```

## Observacoes

- `mes` e `hora` foram mantidos por decisão do projeto.
- `valor_unitario_medio` não deve ser confundido com o KPI executivo de ticket médio.
- A base final não substitui a auditoria: registros removidos seguem em `data/interim/vendas_sorvetes_registros_excluidos.csv`.
