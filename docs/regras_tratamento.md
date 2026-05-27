# Regras De Tratamento Dos Dados

Projeto: Case Sorveteria Analytics  
Fonte bruta: `data/raw/vendas_sorvetes.csv`  
Script responsavel: `scripts/data_cleaning.py`  
Notebook de apoio: `notebooks/02_tratamento_dados.ipynb`

## Principio De Governanca

Os arquivos em `data/raw` nao sao alterados. Toda transformacao gera novos arquivos em `data/interim` ou `data/processed`, mantendo rastreabilidade e auditoria.

## Arquivos Gerados

- `data/interim/vendas_sorvetes_interim.csv`: base intermediaria com padronizacoes, conversoes e flags de qualidade.
- `data/interim/vendas_sorvetes_registros_excluidos.csv`: registros removidos da base final, com motivo de exclusao.
- `data/interim/relatorio_qualidade_tratamento.csv`: resumo quantitativo do impacto do tratamento.
- `data/processed/vendas_sorvetes_tratado.csv`: base analitica final para analises, KPIs e Power BI.

## Resumo Do Impacto

- Linhas na base bruta: 50.000
- Linhas na base processada: 48.491
- Linhas removidas da base processada: 1.509, equivalentes a 3,02%
- Celulas de texto padronizadas: 22.822
- Nulos preenchidos em `sabor`: 500, equivalentes a 1,00%
- Nulos preenchidos em `cidade`: 500, equivalentes a 1,00%
- Nulos finais na base processada: 0
- Duplicidade final de `id_transacao`: 0
- Registros finais com `quantidade <= 0`: 0
- Registros finais com `valor_total <= 0`: 0
- Outliers de `valor_total` mantidos e sinalizados: 101, equivalentes a 0,21% da base processada

## Decisoes De Tratamento

| Problema encontrado | Regra aplicada | Justificativa | Impacto estimado |
|---|---|---|---|
| Nomes de colunas em formato original misto, como `ID_Transacao` e `Valor_Total`. | Renomear para `snake_case`: `id_transacao`, `valor_total`, `canal_venda` etc. | Facilita uso em Python, Power BI, DAX e documentacao tecnica. | 12 colunas padronizadas. |
| Espacos extras e inconsistencias textuais. | Remover espacos extras, aplicar capitalizacao em categorias e cidades, e manter `estado` e `id_cliente` em maiusculas. | Reduz duplicidades artificiais em segmentacoes e filtros. | 22.822 celulas de texto padronizadas. |
| `Data` lida como texto. | Converter para `data_venda` em formato de data. | Necessario para analises temporais, calendario e Power BI. | 0 datas invalidas encontradas. |
| `Hora` lida como texto. | Validar formato `HH:MM`, criar `hora_venda` e extrair `hora` numerica. | Permite analises por faixa horaria e comportamento de compra. | 0 horarios invalidos encontrados. |
| `Sabor` nulo. | Preencher com `Nao Informado` e criar `flag_sabor_nao_informado`. | Preserva o registro valido de venda sem inventar um sabor. | 500 registros preenchidos, 1,00% da base. |
| `Cidade` nula. | Preencher com `Nao Informado` e criar `flag_cidade_nao_informada`. | Mantem vendas validas para receita sem forcar geografia inexistente. | 500 registros preenchidos, 1,00% da base. |
| `Valor_Total` nulo. | Remover da base processada e preservar em `data/interim/vendas_sorvetes_registros_excluidos.csv`. | Receita, ticket medio e KPIs financeiros exigem valor monetario confiavel. | 500 registros afetados, 1,00% da base. |
| `Quantidade <= 0`. | Remover da base processada e preservar em auditoria. | Sem regra de negocio de devolucao/cancelamento, esses registros distorcem volume, ticket e receita. | 1.016 registros marcados como invalidos, 2,03% da base. |
| `Valor_Total <= 0`. | Remover da base processada e preservar em auditoria. | Valores nao positivos nao representam venda positiva confiavel para dashboard executivo. | 1.509 registros marcados como invalidos, 3,02% da base. |
| Duplicidade de `id_transacao`. | Manter somente a primeira ocorrencia na base processada e sinalizar duplicatas. | `id_transacao` foi indicado como chave primaria no briefing. | 0 duplicatas encontradas. |
| Linhas totalmente duplicadas. | Remover da base processada quando existirem e preservar em auditoria. | Evita dupla contagem de vendas. | 0 linhas duplicadas encontradas. |
| Categorias de `tipo_sorvete`, `sabor`, `canal_venda` e `estado`. | Validar contra dominios esperados observados na EDA e no briefing. | Garante consistencia dos filtros e agrupamentos no Power BI. | 0 categorias invalidas encontradas. |
| Outliers de `valor_total`. | Sinalizar em `flag_outlier_valor_total`, sem remover. | Valores altos podem representar vendas reais; sem evidencia de erro, devem ser auditaveis, nao descartados. | 101 registros sinalizados, 0,21% da base processada. |

## Colunas Auxiliares Criadas

- `ano`
- `mes`
- `nome_mes`
- `ano_mes`
- `trimestre`
- `dia_semana`
- `dia_mes`
- `hora_venda`
- `hora`
- `faixa_horario`
- `ticket_transacao`
- `ticket_medio`
- `valor_unitario_estimado`
- `promocao_label`
- `cliente_recorrente`
- `qtd_transacoes_cliente`
- `flag_sabor_nao_informado`
- `flag_cidade_nao_informada`
- `flag_outlier_valor_total`
- `registro_valido_powerbi`

## Observacoes Para Proximas Etapas

- A base processada esta pronta para analises, KPIs e Power BI.
- Registros excluidos nao foram descartados definitivamente; permanecem auditaveis em `data/interim`.
- Antes de recomendacoes executivas finais, validar com o negocio se valores negativos ou zero podem representar devolucao, cancelamento ou ajuste financeiro.
- Outliers devem ser avaliados nas analises de receita, mas foram mantidos por nao haver evidencia suficiente de erro.
