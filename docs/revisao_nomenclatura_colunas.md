# Revisao De Nomenclatura Da Base Processada

Base avaliada: `data/processed/vendas_sorvetes_tratado.csv`  
Escopo: revisao semantica dos nomes finais para Power BI e DAX.  
Status: mudancas aprovadas aplicadas na camada processed. A base raw permanece inalterada.

## Mudancas Aprovadas Aplicadas

| Nome anterior | Nome atual aplicado | Justificativa |
|---|---|---|
| `faixa_horario` | `faixa_horaria` | Forma nominal mais natural em portugues analitico. |
| `quantidade` | `quantidade_vendida` | Explicita que a metrica representa volume vendido. |
| `valor_total` | `receita_transacao` | Explicita que o valor monetario representa receita valida da transacao. |
| `ticket_transacao` | `valor_transacao` | Reduz ambiguidade com o KPI executivo de ticket medio. |
| `ticket_medio` | `valor_unitario_medio` | Evita conflito com a medida DAX de ticket medio. |
| `promocao_label` | `status_promocao` | Troca termo tecnico por rotulo mais claro para visuais. |
| `qtd_transacoes_cliente` | `quantidade_transacoes_cliente` | Remove abreviacao e melhora leitura para usuarios de negocio. |
| `registro_valido_powerbi` | `flag_registro_valido_powerbi` | Padroniza indicador booleano com prefixo `flag_`. |

## Nomes Mantidos Por Decisao Analitica

| Coluna | Decisao | Justificativa |
|---|---|---|
| `mes` | Manter | Nome curto, claro e usual para representar o numero do mes em bases analiticas. |
| `hora` | Manter | Nome curto, claro e suficiente para representar a hora inteira da venda. |

## Analise Coluna A Coluna

| Nome atual | Nome sugerido | Status | Justificativa | Impacto positivo no Power BI/DAX |
|---|---|---|---|---|
| `id_transacao` | `id_transacao` | Manter | Nome claro para chave transacional. | Facilita relacionamentos, contagem distinta e medidas como `Qtd Transacoes`. |
| `data_venda` | `data_venda` | Manter | Nome explicita que a data se refere a venda. | Facilita relacionamento com calendario e medidas time intelligence. |
| `ano` | `ano` | Manter | Nome simples e suficiente para o ano da venda. | Mantem o modelo enxuto e legivel. |
| `mes` | `mes` | Manter | Nome aprovado pelo projeto; representa o numero do mes. | Facilita ordenacao de `nome_mes` sem deixar o modelo verboso. |
| `nome_mes` | `nome_mes` | Manter | Nome claro e adequado para visualizacao. | Facilita exibicao em graficos e segmentadores. |
| `ano_mes` | `ano_mes` | Manter | Campo util para agrupamento temporal mensal. | Facilita eixo mensal e ordenacao cronologica simples. |
| `trimestre` | `trimestre` | Manter | Nome claro para agrupamento trimestral. | Bom para segmentacao executiva. |
| `dia_semana` | `dia_semana` | Manter | Nome compreensivel para o nome do dia da semana. | Facilita leitura em visuais de comportamento semanal. |
| `dia_mes` | `dia_mes` | Manter | Nome ja compreensivel dentro do calendario. | Mantem consistencia com `mes` e `hora`. |
| `hora_venda` | `hora_venda` | Manter | Preserva o horario original da venda em `HH:MM`. | Util para detalhamento horario sem depender de transformacao visual. |
| `hora` | `hora` | Manter | Nome aprovado pelo projeto; representa a hora inteira da venda. | Facilita agrupamentos por hora no Power BI. |
| `faixa_horaria` | `faixa_horaria` | Aplicado | Nome natural para segmentar manha, tarde, noite e madrugada. | Melhora legibilidade em slicers, filtros e graficos executivos. |
| `tipo_sorvete` | `tipo_sorvete` | Manter | Fiel ao dado original e claro para o dominio do case. | Facilita ranking e comparacao por categoria de sorvete. |
| `sabor` | `sabor` | Manter | Nome direto e compreensivel. | Bom para ranking e segmentacao de produto. |
| `quantidade_vendida` | `quantidade_vendida` | Aplicado | Explicita que a coluna representa volume vendido. | Facilita medidas como `Total Quantidade Vendida`. |
| `receita_transacao` | `receita_transacao` | Aplicado | Nome financeiro claro para receita da venda. | Melhora clareza de medidas como `Receita Total = SUM(receita_transacao)`. |
| `valor_transacao` | `valor_transacao` | Aplicado | Deixa claro que e o valor monetario total da transacao. | Evita conflito com KPI de ticket medio. |
| `valor_unitario_medio` | `valor_unitario_medio` | Aplicado | Representa `receita_transacao / quantidade_vendida`. | Evita confusao com medida DAX de ticket medio executivo. |
| `valor_unitario_estimado` | `valor_unitario_estimado` | Manter por ora | Duplicidade conceitual com `valor_unitario_medio`, mas nome e claro. | Pode apoiar comparacoes enquanto o modelo ainda amadurece. |
| `cidade` | `cidade` | Manter | Nome claro para dimensao geografica. | Facilita mapas, filtros e analise regional. |
| `estado` | `estado` | Manter | Embora contenha UF, o termo e compreensivel para usuarios de negocio. | Evita renomeacao desnecessaria nesta etapa. |
| `canal_venda` | `canal_venda` | Manter | Nome claro e alinhado ao negocio. | Facilita medidas por canal e comparacao App, Parceiro e Loja Fisica. |
| `promocao` | `promocao` | Manter | Booleano simples e compreensivel. | Pode ser usado diretamente em filtros tecnicos. |
| `status_promocao` | `status_promocao` | Aplicado | Nome amigavel para rotulos `Com Promocao` e `Sem Promocao`. | Melhora legibilidade em filtros e legendas do Power BI. |
| `id_cliente` | `id_cliente` | Manter | Nome claro para identificador do cliente. | Facilita contagem distinta e analises de recorrencia. |
| `cliente_recorrente` | `cliente_recorrente` | Manter | Booleano sem prefixo, mas legivel para negocio. | Bom para segmentacao simples de clientes. |
| `quantidade_transacoes_cliente` | `quantidade_transacoes_cliente` | Aplicado | Remove abreviacao `qtd`. | Facilita segmentacoes de recorrencia e documentacao DAX. |
| `flag_sabor_nao_informado` | `flag_sabor_nao_informado` | Manter | Nome claro e rastreavel. | Ajuda a filtrar impactos de preenchimento sem esconder qualidade dos dados. |
| `flag_cidade_nao_informada` | `flag_cidade_nao_informada` | Manter | Nome claro e rastreavel. | Ajuda a controlar impacto de geografia incompleta. |
| `flag_outlier_valor_total` | `flag_outlier_valor_total` | Manter por ora | Mantido para evitar renomeacao nao aprovada; indica outliers financeiros. | Permite auditoria tecnica dos valores extremos. |
| `flag_registro_valido_powerbi` | `flag_registro_valido_powerbi` | Aplicado | Prefixo `flag_` explicita indicador booleano. | Padroniza filtros tecnicos e paginas de qualidade. |

## Observacao Sobre Ticket Medio

A coluna fisica `valor_unitario_medio` representa o valor medio por unidade vendida:

```text
valor_unitario_medio = receita_transacao / quantidade_vendida
```

O KPI executivo de ticket medio deve ser criado como medida no Power BI:

```text
Ticket Medio = SUM(receita_transacao) / DISTINCTCOUNT(id_transacao)
```

Essa separacao evita ambiguidade entre preco unitario medio e ticket medio por transacao.

## Recomendacao Final

A base processed agora possui nomes mais claros para Power BI e DAX, preservando `mes` e `hora` conforme decisao do projeto. Mudancas futuras devem ser avaliadas somente se houver necessidade real no modelo semantico ou no dashboard executivo.
