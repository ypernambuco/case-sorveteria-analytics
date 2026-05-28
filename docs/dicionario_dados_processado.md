# Dicionario De Dados Processado

Fonte: `data/processed/vendas_sorvetes_tratado.csv`  
Origem bruta: `data/raw/vendas_sorvetes.csv`  
Status: base analitica estavel para analises, KPIs e Power BI.

## Resumo

- Linhas: 48.491
- Colunas: 31
- Nulos finais: 0
- Duplicidade em `id_transacao`: 0
- Registros com `quantidade_vendida <= 0`: 0
- Registros com `receita_transacao <= 0`: 0

## Colunas

| Coluna | Tipo esperado | Descricao | Observacoes |
|---|---|---|---|
| `id_transacao` | inteiro | Identificador unico da transacao. | Chave de venda; sem duplicidade na base final. |
| `data_venda` | data | Data da venda. | Formato `YYYY-MM-DD`, pronta para relacionamento com calendario. |
| `ano` | inteiro | Ano da venda. | Mantido para filtros e agrupamentos simples. |
| `mes` | inteiro | Numero do mes da venda. | Nome aprovado; usado para ordenacao de `nome_mes`. |
| `nome_mes` | texto | Nome do mes da venda. | Campo amigavel para visuais. |
| `ano_mes` | texto | Combinacao ano-mes da venda. | Util para eixo temporal mensal. |
| `trimestre` | texto | Trimestre da venda. | Valores como `T1`, `T2`, `T3`. |
| `dia_semana` | texto | Dia da semana da venda. | Campo amigavel para analise semanal. |
| `dia_mes` | inteiro | Dia do mes da venda. | Apoia analises de calendario. |
| `hora_venda` | texto | Hora original da venda. | Formato `HH:MM`, em GMT-3 conforme briefing. |
| `hora` | inteiro | Hora inteira da venda. | Nome aprovado; usado para agrupamentos horarios. |
| `faixa_horaria` | texto | Faixa do dia da venda. | Madrugada, Manha, Tarde ou Noite. |
| `tipo_sorvete` | texto | Categoria do sorvete vendido. | Dimensao de produto. |
| `sabor` | texto | Sabor do item vendido. | Nulos da origem foram preenchidos como `Nao Informado`. |
| `quantidade_vendida` | inteiro | Quantidade vendida na transacao. | Apenas valores positivos na base final. |
| `receita_transacao` | decimal | Receita valida da transacao. | Apenas valores positivos na base final. |
| `valor_transacao` | decimal | Valor monetario total da transacao. | Mantido como coluna semantica de valor da venda. |
| `valor_unitario_medio` | decimal | Receita media por unidade vendida. | Calculado como `receita_transacao / quantidade_vendida`. |
| `valor_unitario_estimado` | decimal | Valor unitario estimado. | Mesmo conceito de `valor_unitario_medio`; mantido por rastreabilidade da etapa anterior. |
| `cidade` | texto | Cidade da venda. | Nulos da origem foram preenchidos como `Nao Informado`. |
| `estado` | texto | UF da venda. | Sigla da unidade federativa. |
| `canal_venda` | texto | Canal comercial da venda. | App, Parceiro ou Loja Fisica. |
| `promocao` | booleano | Indica se houve promocao. | Campo booleano tecnico. |
| `status_promocao` | texto | Rotulo de promocao. | `Com Promocao` ou `Sem Promocao`. |
| `id_cliente` | texto | Identificador do cliente. | Permite recorrencia e contagem distinta. |
| `cliente_recorrente` | booleano | Indica cliente com mais de uma transacao. | Derivado da contagem de transacoes por cliente. |
| `quantidade_transacoes_cliente` | inteiro | Numero de transacoes do cliente na base final. | Apoia segmentacao de recorrencia. |
| `flag_sabor_nao_informado` | booleano | Indica sabor ausente na origem. | Mantem rastreabilidade do preenchimento. |
| `flag_cidade_nao_informada` | booleano | Indica cidade ausente na origem. | Mantem rastreabilidade do preenchimento. |
| `flag_outlier_valor_total` | booleano | Indica outlier financeiro mantido. | Outliers foram sinalizados, nao removidos. |
| `flag_registro_valido_powerbi` | booleano | Indica registro valido para Power BI. | Todos os registros da base processed estao marcados como validos. |

## Medidas DAX Recomendadas

```DAX
Receita Total = SUM(vendas_sorvetes_tratado[receita_transacao])

Quantidade Vendida = SUM(vendas_sorvetes_tratado[quantidade_vendida])

Transacoes = DISTINCTCOUNT(vendas_sorvetes_tratado[id_transacao])

Ticket Medio = DIVIDE([Receita Total], [Transacoes])
```

## Observacoes

- `mes` e `hora` foram mantidos por decisao do projeto.
- `valor_unitario_medio` nao deve ser confundido com o KPI executivo de ticket medio.
- A base final nao substitui a auditoria: registros removidos seguem em `data/interim/vendas_sorvetes_registros_excluidos.csv`.
