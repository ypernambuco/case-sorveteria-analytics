# Dicionario De Dados Inicial

Fonte principal: `data/raw/vendas_sorvetes.csv`  
Contexto de negocio: `docs/case_sorveteria.pptx`

Este dicionario foi criado a partir da leitura inicial da base bruta e do briefing do case. Nenhuma limpeza, transformacao ou imputacao foi aplicada aos dados.

## Resumo Da Base

- Linhas: 50.000
- Colunas: 12
- Periodo identificado: 2025-02-20 a 2025-09-20
- Linhas duplicadas: 0
- `ID_Transacao` duplicado: 0
- Valores nulos encontrados em `Sabor`, `Valor_Total` e `Cidade`
- Campos com valores nao positivos a investigar: `Quantidade` e `Valor_Total`

## Dicionario Inicial

| Coluna | Tipo identificado | Descricao provavel | Observacoes de qualidade | Duvidas ou premissas |
|---|---:|---|---|---|
| `ID_Transacao` | `int64` | Identificador unico da venda/transacao. O briefing indica que e a PK. | Sem nulos; 50.000 valores unicos; sem duplicidade identificada. | Premissa: cada linha representa uma venda unica. |
| `Data` | `object` / texto | Data da venda. | Sem nulos; todas as datas foram parseaveis; periodo identificado entre 2025-02-20 e 2025-09-20; lida inicialmente como texto. | Converter para data em etapa futura. Confirmar se a ausencia de meses fora desse intervalo e esperada. |
| `Hora` | `object` / texto | Hora da venda em GMT-3, conforme briefing. | Sem nulos; horarios parseaveis no formato `HH:MM`; 60 valores unicos. | Converter para tipo horario ou extrair faixa horaria em etapa futura. |
| `Tipo_Sorvete` | `object` / texto | Categoria do produto vendido. | Sem nulos; 5 categorias identificadas. | Confirmar se todos os tipos esperados estao presentes. |
| `Sabor` | `object` / texto | Sabor do item vendido. | 500 nulos, equivalentes a 1,00% da base; 8 sabores nao nulos identificados. | Definir se nulo significa sabor nao informado, item sem sabor aplicavel ou falha de carga. |
| `Quantidade` | `int64` | Quantia vendida, conforme briefing. | Sem nulos; valores variam de -6 a 6; 1.016 registros com quantidade menor ou igual a zero. | Investigar se valores negativos/zero representam devolucao, cancelamento, ajuste operacional ou erro. |
| `Valor_Total` | `float64` | Valor recebido na venda, conforme briefing. | 500 nulos, equivalentes a 1,00% da base; valores variam de -89,82 a 89,88; 1.009 registros com valor menor ou igual a zero. | Definir regra para receita: excluir, tratar como devolucao/cancelamento ou manter conforme regra de negocio. |
| `Cidade` | `object` / texto | Cidade da venda. | 500 nulos, equivalentes a 1,00% da base; alta cardinalidade, com 6.554 cidades nao nulas. | Validar consistencia com `Estado`; exemplos iniciais sugerem possivel necessidade de checagem geografica. |
| `Estado` | `object` / texto | UF/estado da venda. | Sem nulos; 27 UFs identificadas. | Confirmar se a distribuicao por UF e esperada e se deve ser agrupada por regiao. |
| `Canal_Venda` | `object` / texto | Canal da venda. | Sem nulos; 3 canais identificados: `Parceiro`, `App` e `Loja Fisica`. | Confirmar definicoes operacionais de cada canal. |
| `Promocao` | `bool` | Indica se houve promocao na venda. | Sem nulos; valores booleanos `True` e `False` com distribuicao aproximadamente equilibrada. | Confirmar se `True` representa qualquer tipo de promocao ou apenas campanhas especificas. |
| `ID_Cliente` | `object` / texto | Identificador do cliente. | Sem nulos; 8.974 clientes distintos; nao e chave unica da base. | Premissa: um mesmo cliente pode realizar multiplas compras. |

## Campos Por Papel Analitico

| Papel analitico | Campos provaveis |
|---|---|
| Data | `Data`, `Hora` |
| Produto | `Tipo_Sorvete`, `Sabor` |
| Canal | `Canal_Venda` |
| Receita | `Valor_Total` |
| Quantidade | `Quantidade` |
| Loja | Nao identificado explicitamente na base |
| Regiao | `Cidade`, `Estado` |
| Vendedor | Nao identificado explicitamente na base |
| Cliente | `ID_Cliente` |

## Pontos De Atencao Para A Proxima Etapa

- Definir tratamento para nulos em `Sabor`, `Valor_Total` e `Cidade`.
- Investigar registros com `Quantidade <= 0`.
- Investigar registros com `Valor_Total <= 0`.
- Converter `Data` e `Hora` para tipos adequados.
- Validar consistencia geografica entre `Cidade` e `Estado`.
- Confirmar regras de negocio para promocao, canais e possiveis devolucoes/cancelamentos.
- Evitar qualquer alteracao em `data/raw`; bases tratadas devem ser geradas em `data/interim` ou `data/processed`.
