# Regras De Tratamento E Governanca Dos Dados

Projeto: Case Sorveteria Analytics  
Fonte bruta: `data/raw/vendas_sorvetes.csv`  
Script responsavel: `scripts/data_cleaning.py`  
Notebook de apoio: `notebooks/02_tratamento_dados.ipynb`  
Base final: `data/processed/vendas_sorvetes_tratado.csv`

## Sumario Executivo

A etapa de tratamento transformou a base bruta de vendas em uma base analitica confiavel para uso em analises, KPIs e Power BI, preservando rastreabilidade dos registros descartados e das decisoes aplicadas.

O processamento manteve 48.491 registros validos de um total original de 50.000, o que representa 96,98% da base bruta. Os 1.509 registros removidos da base final permanecem auditaveis em `data/interim/vendas_sorvetes_registros_excluidos.csv`.

## Principio De Governanca

Os arquivos em `data/raw` nao sao alterados. Toda transformacao gera arquivos derivados em `data/interim` ou `data/processed`, garantindo reprodutibilidade, rastreabilidade e separacao clara entre fonte original, auditoria e base de consumo.

## Arquitetura Do Pipeline

```text
Raw -> Interim -> Processed -> Power BI
```

| Camada | Papel | Arquivos principais |
|---|---|---|
| Raw | Camada imutavel com os dados originais recebidos. Deve ser usada apenas como leitura. | `data/raw/vendas_sorvetes.csv` |
| Interim | Camada de auditoria e transicao. Contem padronizacoes, flags de qualidade, registros excluidos e relatorio de impacto. | `data/interim/vendas_sorvetes_interim.csv`, `data/interim/vendas_sorvetes_registros_excluidos.csv`, `data/interim/relatorio_qualidade_tratamento.csv` |
| Processed | Camada analitica final, limpa e pronta para consumo em analises e Power BI. | `data/processed/vendas_sorvetes_tratado.csv` |
| Power BI | Camada de consumo executivo. Deve usar preferencialmente a base processed e medidas DAX documentadas. | `powerbi/` |

## Premissas Analiticas

- Valores negativos ou iguais a zero no valor monetario da venda nao foram considerados vendas validas para a base final. Na camada processada, a coluna final correspondente e `receita_transacao`.
- Valores negativos ou iguais a zero em quantidade vendida foram removidos da base final pelo mesmo criterio de confiabilidade operacional. Na camada processada, a coluna final correspondente e `quantidade_vendida`.
- `Valor_Total` nulo na origem foi tratado como impeditivo para analise financeira, pois afeta receita, ticket medio e ranking de produtos.
- Nulos em `sabor` e `cidade` foram preenchidos com `Nao Informado`, acompanhados de flags, pois a venda continua financeiramente valida mesmo sem detalhamento completo de produto ou geografia.
- Outliers de receita foram mantidos e apenas sinalizados em `flag_outlier_valor_total`. A decisao evita descartar vendas potencialmente reais sem evidencia objetiva de erro.
- O horario informado no case usa GMT-3. A coluna `hora_venda` preserva esse contexto, e as faixas horarias foram derivadas com base nessa premissa.
- `valor_transacao` representa o valor total da venda. A coluna `valor_unitario_medio` foi derivada como `receita_transacao / quantidade_vendida`, funcionando como valor medio unitario estimado da transacao. Para KPI executivo de ticket medio, a recomendacao e calcular uma medida no Power BI como `SUM(receita_transacao) / DISTINCTCOUNT(id_transacao)`.
- A base processada esta preparada para Power BI, mas recomendacoes finais devem considerar validacao de negocio antes de qualquer storytelling executivo.

## Metricas De Qualidade Dos Dados

| Dimensao | Definicao | Resultado | Leitura executiva |
|---|---|---:|---|
| Completude | Ausencia de nulos na base processada. | 100,00% | A base final nao possui campos nulos. |
| Unicidade | Ausencia de duplicidade em `id_transacao`. | 100,00% | Cada transacao aparece uma unica vez na base final. |
| Consistencia | Ausencia de categorias invalidas, datas invalidas e horarios invalidos. | 100,00% | Campos criticos passaram nas validacoes implementadas. |
| Validade | Percentual da base bruta mantido como valido para Power BI. | 96,98% | 3,02% dos registros foram removidos por problemas que afetam confiabilidade analitica. |

## Data Quality Score

O Data Quality Score foi definido como uma media simples das quatro dimensoes acima:

```text
Data Quality Score = (Completude + Unicidade + Consistencia + Validade) / 4
```

Aplicando os resultados do tratamento:

```text
Data Quality Score = (100,00 + 100,00 + 100,00 + 96,98) / 4 = 99,25
```

Classificacao sugerida:

- 95 a 100: Alta confiabilidade para analise executiva.
- 85 a 94,99: Confiabilidade boa, com pontos de atencao.
- 70 a 84,99: Requer saneamento adicional antes de uso executivo.
- Abaixo de 70: Nao recomendado para tomada de decisao.

Resultado atual: 99,25, indicando alta confiabilidade para analises e dashboard, desde que as premissas documentadas sejam respeitadas.

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

## Decisoes De Tratamento

| Problema encontrado | Regra aplicada | Justificativa executiva | Impacto estimado |
|---|---|---|---|
| Nomes de colunas em formato original misto, como `ID_Transacao` e `Valor_Total`. | Renomear para nomes analiticos em `snake_case`: `id_transacao`, `receita_transacao`, `canal_venda` etc. | Aumenta padronizacao tecnica e reduz friccao para uso em Python, Power BI e DAX. | 12 colunas de origem padronizadas e nomes finais refinados na camada processed. |
| Espacos extras e inconsistencias textuais. | Remover espacos extras, aplicar capitalizacao em categorias/cidades, e manter `estado` e `id_cliente` em maiusculas. | Evita filtros duplicados e melhora experiencia de navegacao no dashboard. | 22.822 celulas de texto padronizadas. |
| `Data` lida como texto. | Converter para `data_venda`. | Permite calendario, cortes por mes, trimestre, dia da semana e analises temporais confiaveis. | 0 datas invalidas. |
| `Hora` lida como texto. | Validar formato `HH:MM`, criar `hora_venda`, extrair `hora` e classificar `faixa_horaria`. | Viabiliza analise de comportamento de compra por horario, respeitando GMT-3. | 0 horarios invalidos. |
| `Sabor` nulo. | Preencher com `Nao Informado` e criar `flag_sabor_nao_informado`. | Preserva receita valida sem inventar atributo de produto. | 500 registros preenchidos, 1,00% da base. |
| `Cidade` nula. | Preencher com `Nao Informado` e criar `flag_cidade_nao_informada`. | Mantem vendas validas para receita, mas sinaliza limitacao geografica. | 500 registros preenchidos, 1,00% da base. |
| `Valor_Total` nulo. | Remover da base processada e preservar em auditoria. | Registro sem valor financeiro nao sustenta KPI executivo de receita ou ticket medio. | 500 registros afetados, 1,00% da base. |
| `Quantidade <= 0`. | Remover da base processada e preservar em auditoria. | Sem regra confirmada de devolucao/cancelamento, o registro pode distorcer volume, ticket e produtividade. | 1.016 registros marcados, 2,03% da base. |
| `Valor_Total <= 0`. | Remover da base processada e preservar em auditoria. | Valores nao positivos nao representam venda positiva confiavel para dashboard executivo. | 1.509 registros marcados, 3,02% da base. |
| Duplicidade de `id_transacao`. | Manter somente a primeira ocorrencia na base processada e sinalizar duplicatas. | Evita dupla contagem de vendas e preserva a chave primaria indicada no briefing. | 0 duplicatas encontradas. |
| Linhas totalmente duplicadas. | Remover da base processada quando existirem e preservar em auditoria. | Evita inflar receita, volume e contagem de transacoes. | 0 linhas duplicadas encontradas. |
| Categorias de `tipo_sorvete`, `sabor`, `canal_venda` e `estado`. | Validar contra dominios esperados observados na EDA e no briefing. | Garante filtros consistentes e reduz risco de segmentacao incorreta no Power BI. | 0 categorias invalidas. |
| Outliers de receita. | Sinalizar em `flag_outlier_valor_total`, sem remover. | Mantem potencial venda real e permite analise especifica sem perda de informacao. | 101 registros sinalizados, 0,21% da base processada. |

## Colunas Auxiliares Criadas

| Coluna | Uso analitico |
|---|---|
| `ano`, `mes`, `nome_mes`, `ano_mes`, `trimestre` | Analise temporal e ordenacao no Power BI. |
| `dia_semana`, `dia_mes` | Analise de comportamento por calendario. |
| `hora_venda`, `hora`, `faixa_horaria` | Analise por periodo do dia. |
| `valor_transacao` | Valor total da venda por transacao. |
| `valor_unitario_medio`, `valor_unitario_estimado` | Valor medio unitario estimado da transacao. |
| `status_promocao` | Rotulo executivo para segmentar vendas com/sem promocao. |
| `cliente_recorrente`, `quantidade_transacoes_cliente` | Sinais iniciais de recompra e recorrencia. |
| `flag_sabor_nao_informado`, `flag_cidade_nao_informada` | Transparencia sobre preenchimentos de dados ausentes. |
| `flag_outlier_valor_total` | Auditoria de valores monetarios extremos mantidos. |
| `flag_registro_valido_powerbi` | Indicador de prontidao para consumo analitico. |

## Riscos E Validacoes Futuras Com O Negocio

- Confirmar se registros com valor monetario nao positivo ou quantidade nao positiva representam erro, devolucao, cancelamento, cortesia, ajuste financeiro ou outra regra operacional.
- Confirmar se outliers de receita representam compras reais, eventos especiais, venda corporativa ou erro de carga.
- Validar consistencia geografica entre `cidade` e `estado`, especialmente antes de recomendacoes de expansao regional.
- Confirmar regras de negocio para promocao, incluindo se `promocao = True` representa qualquer desconto, campanha especifica ou outra condicao comercial.
- Definir calendario de negocio para Power BI, incluindo feriados, sazonalidade e eventuais campanhas.
- Criar medidas DAX oficiais para KPIs executivos, evitando calculos divergentes entre notebooks e dashboard.

## Recomendacao Para Power BI

Usar `data/processed/vendas_sorvetes_tratado.csv` como fonte principal do modelo. A camada `data/interim` deve ser mantida como auditoria, mas nao precisa ser carregada no dashboard executivo, exceto se houver uma pagina tecnica de qualidade de dados.
