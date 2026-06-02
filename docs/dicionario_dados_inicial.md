# Dicionário De Dados Inicial

Fonte principal: `data/raw/vendas_sorvetes.csv`  
Contexto de negócio: `docs/case_sorveteria.pptx`

Este dicionário foi criado a partir da leitura inicial da base bruta e do briefing do case. Nenhuma limpeza, transformação ou imputação foi aplicada aos dados.

## Resumo Da Base

- Linhas: 50.000
- Colunas: 12
- Período identificado: 2025-02-20 a 2025-09-20
- Linhas duplicadas: 0
- `ID_Transacao` duplicado: 0
- Valores nulos encontrados em `Sabor`, `Valor_Total` e `Cidade`
- Campos com valores não positivos a investigar: `Quantidade` e `Valor_Total`

## Dicionário Inicial

| Coluna | Tipo identificado | Descrição provavel | Observacoes de qualidade | Duvidas ou premissas |
|---|---:|---|---|---|
| `ID_Transacao` | `int64` | Identificador único da venda/transação. O briefing indica que e a PK. | Sem nulos; 50.000 valores únicos; sem duplicidade identificada. | Premissa: cada linha representa uma venda unica. |
| `Data` | `object` / texto | Data da venda. | Sem nulos; todas as datas foram parseaveis; período identificado entre 2025-02-20 e 2025-09-20; lida inicialmente como texto. | Converter para data em etapa futura. Confirmar se a ausencia de meses fora desse intervalo e esperada. |
| `Hora` | `object` / texto | Hora da venda em GMT-3, conforme briefing. | Sem nulos; horários parseaveis no formato `HH:MM`; 60 valores únicos. | Converter para tipo horário ou extrair faixa horária em etapa futura. |
| `Tipo_Sorvete` | `object` / texto | Categoria do produto vendido. | Sem nulos; 5 categorias identificadas. | Confirmar se todos os tipos esperados estão presentes. |
| `Sabor` | `object` / texto | Sabor do item vendido. | 500 nulos, equivalentes a 1,00% da base; 8 sabores não nulos identificados. | Definir se nulo significa sabor não informado, item sem sabor aplicavel ou falha de carga. |
| `Quantidade` | `int64` | Quantia vendida, conforme briefing. | Sem nulos; valores variam de -6 a 6; 1.016 registros com quantidade menor ou igual a zero. | Investigar se valores negativos/zero representam devolucao, cancelamento, ajuste operacional ou erro. |
| `Valor_Total` | `float64` | Valor recebido na venda, conforme briefing. | 500 nulos, equivalentes a 1,00% da base; valores variam de -89,82 a 89,88; 1.009 registros com valor menor ou igual a zero. | Definir regra para receita: excluir, tratar como devolucao/cancelamento ou manter conforme regra de negócio. |
| `Cidade` | `object` / texto | Cidade da venda. | 500 nulos, equivalentes a 1,00% da base; alta cardinalidade, com 6.554 cidades não nulas. | Validar consistência com `Estado`; exemplos iniciais sugerem possível necessidade de checagem geográfica. |
| `Estado` | `object` / texto | UF/estado da venda. | Sem nulos; 27 UFs identificadas. | Confirmar se a distribuição por UF e esperada e se deve ser agrupada por região. |
| `Canal_Venda` | `object` / texto | Canal da venda. | Sem nulos; 3 canais identificados: `Parceiro`, `App` e `Loja Fisica`. | Confirmar definicoes operacionais de cada canal. |
| `Promocao` | `bool` | Indica se houve promoção na venda. | Sem nulos; valores booleanos `True` e `False` com distribuição aproximadamente equilibrada. | Confirmar se `True` representa qualquer tipo de promoção ou apenas campanhas especificas. |
| `ID_Cliente` | `object` / texto | Identificador do cliente. | Sem nulos; 8.974 clientes distintos; não e chave unica da base. | Premissa: um mesmo cliente pode realizar multiplas compras. |

## Campos Por Papel Analítico

| Papel analítico | Campos provaveis |
|---|---|
| Data | `Data`, `Hora` |
| Produto | `Tipo_Sorvete`, `Sabor` |
| Canal | `Canal_Venda` |
| Receita | `Valor_Total` |
| Quantidade | `Quantidade` |
| Loja | Não identificado explicitamente na base |
| Região | `Cidade`, `Estado` |
| Vendedor | Não identificado explicitamente na base |
| Cliente | `ID_Cliente` |

## Pontos De Atencao Para A Proxima Etapa

- Definir tratamento para nulos em `Sabor`, `Valor_Total` e `Cidade`.
- Investigar registros com `Quantidade <= 0`.
- Investigar registros com `Valor_Total <= 0`.
- Converter `Data` e `Hora` para tipos adequados.
- Validar consistência geográfica entre `Cidade` e `Estado`.
- Confirmar regras de negócio para promoção, canais e possíveis devolucoes/cancelamentos.
- Evitar qualquer alteração em `data/raw`; bases tratadas devem ser geradas em `data/interim` ou `data/processed`.
