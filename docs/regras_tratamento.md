# Regras De Tratamento E Governança Dos Dados

Projeto: Case Sorveteria Analytics
Fonte bruta: `data/raw/vendas_sorvetes.csv`
Script responsável: `scripts/data_cleaning.py`
Notebook de apoio: `notebooks/02_tratamento_dados.ipynb`
Base final: `data/processed/vendas_sorvetes_tratado.csv`

## Sumário Executivo

A etapa de tratamento transformou a base bruta de vendas em uma base analítica confiável para uso em análises, KPIs e Power BI, preservando rastreabilidade dos registros descartados e das decisões aplicadas.

O processamento manteve 48.491 registros válidos de um total original de 50.000, o que representa 96,98% da base bruta. Os 1.509 registros removidos da base final permanecem auditaveis em `data/interim/vendas_sorvetes_registros_excluidos.csv`.

## Principio De Governança

Os arquivos em `data/raw` não são alterados. Toda transformação gera arquivos derivados em `data/interim` ou `data/processed`, garantindo reprodutibilidade, rastreabilidade e separacao clara entre fonte original, auditoria e base de consumo.

## Arquitetura Do Pipeline

```text
Raw -> Interim -> Processed -> Power BI
```

| Camada | Papel | Arquivos principais |
|---|---|---|
| Raw | Camada imutável com os dados originais recebidos. Deve ser usada apenas como leitura. | `data/raw/vendas_sorvetes.csv` |
| Interim | Camada de auditoria e transicao. Contem padronizacoes, flags de qualidade, registros excluidos e relatório de impacto. | `data/interim/vendas_sorvetes_interim.csv`, `data/interim/vendas_sorvetes_registros_excluidos.csv`, `data/interim/relatorio_qualidade_tratamento.csv` |
| Processed | Camada analítica final, limpa e pronta para consumo em análises e Power BI. | `data/processed/vendas_sorvetes_tratado.csv` |
| Power BI | Camada de consumo executivo. Deve usar preferencialmente a base processed e medidas DAX documentadas. | `powerbi/` |

## Premissas Analíticas

- Valores negativos ou iguais a zero no valor monetario da venda não foram considerados vendas válidas para a base final. Na camada processada, a coluna final correspondente e `receita_transacao`.
- Valores negativos ou iguais a zero em quantidade vendida foram removidos da base final pelo mesmo critério de confiabilidade operacional. Na camada processada, a coluna final correspondente e `quantidade_vendida`.
- `Valor_Total` nulo na origem foi tratado como impeditivo para análise financeira, pois afeta receita, ticket médio e ranking de produtos.
- Nulos em `sabor` e `cidade` foram preenchidos com `Nao Informado`, acompanhados de flags, pois a venda continua financeiramente válida mesmo sem detalhamento completo de produto ou geografia.
- Outliers de receita foram mantidos e apenas sinalizados em `flag_outlier_valor_total`. A decisão evita descartar vendas potencialmente reais sem evidencia objetiva de erro.
- O horário informado no case usa GMT-3. A coluna `hora_venda` preserva esse contexto, e as faixas horarias foram derivadas com base nessa premissa.
- `valor_transacao` representa o valor total da venda. A coluna `valor_unitario_medio` foi derivada como `receita_transacao / quantidade_vendida`, funcionando como valor médio unitário estimado da transação. Para KPI executivo de ticket médio, a recomendacao e calcular uma medida no Power BI como `SUM(receita_transacao) / DISTINCTCOUNT(id_transacao)`.
- A base processada está preparada para Power BI, mas recomendações finais devem considerar validação de negócio antes de qualquer storytelling executivo.

## Métricas De Qualidade Dos Dados

| Dimensão | Definição | Resultado | Leitura executiva |
|---|---|---:|---|
| Completude | Ausencia de nulos na base processada. | 100,00% | A base final não possui campos nulos. |
| Unicidade | Ausencia de duplicidade em `id_transacao`. | 100,00% | Cada transação aparece uma unica vez na base final. |
| Consistência | Ausencia de categorias invalidas, datas invalidas e horários invalidos. | 100,00% | Campos criticos passaram nas validacoes implementadas. |
| Validade | Percentual da base bruta mantido como válido para Power BI. | 96,98% | 3,02% dos registros foram removidos por problemas que afetam confiabilidade analítica. |

## Data Quality Score

O Data Quality Score foi definido como uma média simples das quatro dimensões acima:

```text
Data Quality Score = (Completude + Unicidade + Consistencia + Validade) / 4
```

Aplicando os resultados do tratamento:

```text
Data Quality Score = (100,00 + 100,00 + 100,00 + 96,98) / 4 = 99,25
```

Classificação sugerida:

- 95 a 100: Alta confiabilidade para análise executiva.
- 85 a 94,99: Confiabilidade boa, com pontos de atenção.
- 70 a 84,99: Requer saneamento adicional antes de uso executivo.
- Abaixo de 70: Não recomendado para tomada de decisão.

Resultado atual: 99,25, indicando alta confiabilidade para análises e dashboard, desde que as premissas documentadas sejam respeitadas.

## Resumo Do Impacto

- Linhas na base bruta: 50.000
- Linhas na base processada: 48.491
- Linhas removidas da base processada: 1.509, equivalentes a 3,02%
- Celulas de texto padronizadas: 22.822
- Nulos preenchidos em `sabor`: 500, equivalentes a 1,00%
- Nulos preenchidos em `cidade`: 500, equivalentes a 1,00%
- Nulos finais na base processada: 0
- Duplicidade final de `id_transacao`: 0
- Registros finais com `quantidade_vendida <= 0`: 0
- Registros finais com `receita_transacao <= 0`: 0
- Categorias invalidas finais: 0
- Outliers de receita mantidos e sinalizados: 101, equivalentes a 0,21% da base processada

## Decisões De Tratamento

| Problema encontrado | Regra aplicada | Justificativa executiva | Impacto estimado |
|---|---|---|---|
| Nomes de colunas em formato original misto, como `ID_Transacao` e `Valor_Total`. | Renomear para nomes analíticos em `snake_case`: `id_transacao`, `receita_transacao`, `canal_venda` etc. | Aumenta padronização técnica e reduz fricção para uso em Python, Power BI e DAX. | 12 colunas de origem padronizadas e nomes finais refinados na camada processed. |
| Espacos extras e inconsistencias textuais. | Remover espacos extras, aplicar capitalizacao em categorias/cidades, e manter `estado` e `id_cliente` em maiusculas. | Evita filtros duplicados e melhora experiência de navegacao no dashboard. | 22.822 celulas de texto padronizadas. |
| `Data` lida como texto. | Converter para `data_venda`. | Permite calendário, cortes por mês, trimestre, dia da semana e análises temporais confiaveis. | 0 datas invalidas. |
| `Hora` lida como texto. | Validar formato `HH:MM`, criar `hora_venda`, extrair `hora` e classificar `faixa_horaria`. | Viabiliza análise de comportamento de compra por horário, respeitando GMT-3. | 0 horários invalidos. |
| `Sabor` nulo. | Preencher com `Nao Informado` e criar `flag_sabor_nao_informado`. | Preserva receita válida sem inventar atributo de produto. | 500 registros preenchidos, 1,00% da base. |
| `Cidade` nula. | Preencher com `Nao Informado` e criar `flag_cidade_nao_informada`. | Mantém vendas válidas para receita, mas sinaliza limitação geográfica. | 500 registros preenchidos, 1,00% da base. |
| `Valor_Total` nulo. | Remover da base processada e preservar em auditoria. | Registro sem valor financeiro não sustenta KPI executivo de receita ou ticket médio. | 500 registros afetados, 1,00% da base. |
| `Quantidade <= 0`. | Remover da base processada e preservar em auditoria. | Sem regra confirmada de devolucao/cancelamento, o registro pode distorcer volume, ticket e produtividade. | 1.016 registros marcados, 2,03% da base. |
| `Valor_Total <= 0`. | Remover da base processada e preservar em auditoria. | Valores não positivos não representam venda positiva confiável para dashboard executivo. | 1.509 registros marcados, 3,02% da base. |
| Duplicidade de `id_transacao`. | Manter somente a primeira ocorrencia na base processada e sinalizar duplicatas. | Evita dupla contagem de vendas e preserva a chave primaria indicada no briefing. | 0 duplicatas encontradas. |
| Linhas totalmente duplicadas. | Remover da base processada quando existirem e preservar em auditoria. | Evita inflar receita, volume e contagem de transações. | 0 linhas duplicadas encontradas. |
| Categorias de `tipo_sorvete`, `sabor`, `canal_venda` e `estado`. | Validar contra dominios esperados observados na EDA e no briefing. | Garante filtros consistentes e reduz risco de segmentação incorreta no Power BI. | 0 categorias invalidas. |
| Outliers de receita. | Sinalizar em `flag_outlier_valor_total`, sem remover. | Mantém potencial venda real e permite análise específica sem perda de informação. | 101 registros sinalizados, 0,21% da base processada. |

## Colunas Auxiliares Criadas

| Coluna | Uso analítico |
|---|---|
| `ano`, `mes`, `nome_mes`, `ano_mes`, `trimestre` | Análise temporal e ordenacao no Power BI. |
| `dia_semana`, `dia_mes` | Análise de comportamento por calendário. |
| `hora_venda`, `hora`, `faixa_horaria` | Análise por período do dia. |
| `valor_transacao` | Valor total da venda por transação. |
| `valor_unitario_medio`, `valor_unitario_estimado` | Valor médio unitário estimado da transação. |
| `status_promocao` | Rotulo executivo para segmentar vendas com/sem promoção. |
| `cliente_recorrente`, `quantidade_transacoes_cliente` | Sinais iniciais de recompra e recorrência. |
| `flag_sabor_nao_informado`, `flag_cidade_nao_informada` | Transparencia sobre preenchimentos de dados ausentes. |
| `flag_outlier_valor_total` | Auditoria de valores monetarios extremos mantidos. |
| `flag_registro_valido_powerbi` | Indicador de prontidao para consumo analítico. |

## Riscos E Validacoes Futuras Com O Negócio

- Confirmar se registros com valor monetario não positivo ou quantidade não positiva representam erro, devolucao, cancelamento, cortesia, ajuste financeiro ou outra regra operacional.
- Confirmar se outliers de receita representam compras reais, eventos especiais, venda corporativa ou erro de carga.
- Validar consistência geográfica entre `cidade` e `estado`, especialmente antes de recomendações de expansão regional.
- Confirmar regras de negócio para promoção, incluindo se `promocao = True` representa qualquer desconto, campanha específica ou outra condicao comercial.
- Definir calendário de negócio para Power BI, incluindo feriados, sazonalidade e eventuais campanhas.
- Criar medidas DAX oficiais para KPIs executivos, evitando calculos divergentes entre notebooks e dashboard.

## Recomendacao Para Power BI

Usar `data/processed/vendas_sorvetes_tratado.csv` como fonte principal do modelo. A camada `data/interim` deve ser mantida como auditoria, mas não precisa ser carregada no dashboard executivo, exceto se houver uma pagina técnica de qualidade de dados.
