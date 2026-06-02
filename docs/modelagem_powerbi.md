# Modelagem Power BI - Case Sorveteria Analytics

Fonte original da camada analítica: `data/processed/vendas_sorvetes_tratado.csv`
Camada derivada para Power BI: `data/powerbi/`
Objetivo: facilitar a construção de um modelo analítico profissional em formato estrela, separando tabela fato e dimensões.

## Arquivos Criados

| Arquivo | Papel no modelo | Linhas | Descrição |
|---|---:|---:|---|
| `data/powerbi/fato_vendas.csv` | Fato | 48.491 | Tabela transacional com métricas de venda e chaves para dimensões. |
| `data/powerbi/dim_produtos.csv` | Dimensão | 40 | Cadastro analítico de produtos por categoria e sabor. |
| `data/powerbi/dim_clientes.csv` | Dimensão | 8.970 | Cadastro de clientes com atributos de recorrência, valor e preferências. |
| `data/powerbi/dim_canais.csv` | Dimensão | 3 | Cadastro dos canais de venda. |
| `data/powerbi/dim_tempo.csv` | Dimensão calendário | 213 | Calendário continuo entre a primeira e a ultima data da base. |

Os arquivos foram gerados sem alterar `data/processed/vendas_sorvetes_tratado.csv`. A rotina reprodutivel está em `scripts/export_powerbi_model.py`.

## Desenho Do Modelo

```text
dim_tempo[data_venda]       1 ---- * fato_vendas[data_venda]
dim_produtos[id_produto]    1 ---- * fato_vendas[id_produto]
dim_clientes[id_cliente]    1 ---- * fato_vendas[id_cliente]
dim_canais[id_canal]        1 ---- * fato_vendas[id_canal]
```

Modelo recomendado: estrela simples, com filtros fluindo das dimensões para a fato.

## Tabelas E Colunas

### fato_vendas.csv

| Coluna | Tipo recomendado no Power BI | Uso |
|---|---|---|
| `id_transacao` | Numero inteiro | Chave unica da venda; usada em contagem distinta. |
| `data_venda` | Data | Chave de relacionamento com `dim_tempo`. |
| `id_produto` | Numero inteiro | Chave de relacionamento com `dim_produtos`. |
| `id_cliente` | Texto | Chave de relacionamento com `dim_clientes`. |
| `id_canal` | Numero inteiro | Chave de relacionamento com `dim_canais`. |
| `quantidade_vendida` | Numero inteiro | Métrica de volume vendido. |
| `receita_transacao` | Decimal | Métrica principal de receita. |
| `valor_transacao` | Decimal | Valor monetario total da transação, mantido por rastreabilidade. |
| `valor_unitario_medio` | Decimal | Valor médio por unidade na transação. |
| `promocao` | Verdadeiro/Falso | Flag técnica de promoção. |
| `status_promocao` | Texto | Rotulo de promoção: `Com Promocao` ou `Sem Promocao`. |
| `hora_venda` | Texto | Hora original da venda em formato `HH:MM`. |
| `hora` | Numero inteiro | Hora cheia para análises operacionais. |
| `faixa_horaria` | Texto | Faixa do dia: Manha, Tarde ou Noite. |
| `flag_outlier_valor_total` | Verdadeiro/Falso | Indica outlier financeiro sinalizado no tratamento. |
| `flag_registro_valido_powerbi` | Verdadeiro/Falso | Indica registro válido para consumo analítico. |

### dim_produtos.csv

| Coluna | Tipo recomendado no Power BI | Uso |
|---|---|---|
| `id_produto` | Numero inteiro | Chave primaria da dimensão de produto. |
| `produto` | Texto | Nome completo do produto no formato `categoria - sabor`. |
| `tipo_sorvete` | Texto | Categoria do produto. |
| `sabor` | Texto | Sabor do produto. |
| `flag_sabor_nao_informado` | Verdadeiro/Falso | Rastreia produtos com sabor ausente na origem. |

### dim_clientes.csv

| Coluna | Tipo recomendado no Power BI | Uso |
|---|---|---|
| `id_cliente` | Texto | Chave primaria da dimensão de cliente. |
| `cliente_recorrente` | Verdadeiro/Falso | Indica se o cliente possui mais de uma compra. |
| `quantidade_transacoes_cliente` | Numero inteiro | Total de transações observadas para o cliente. |
| `faixa_frequencia_cliente` | Texto | Segmento de frequência de compra. |
| `segmento_valor_cliente` | Texto | Segmento de valor do cliente com base em receita total. |
| `primeira_data_compra` | Data | Primeira compra observada do cliente. |
| `ultima_data_compra` | Data | Ultima compra observada do cliente. |
| `dias_entre_primeira_ultima_compra` | Numero inteiro | Janela de relacionamento observada na base. |
| `receita_total_cliente` | Decimal | Receita histórica do cliente na base. |
| `volume_total_cliente` | Numero inteiro | Total de unidades compradas pelo cliente. |
| `ticket_medio_cliente` | Decimal | Receita média por transação do cliente. |
| `cidade_principal` | Texto | Cidade mais frequente do cliente na base. |
| `estado_principal` | Texto | Estado mais frequente do cliente na base. |
| `canal_preferencial` | Texto | Canal mais frequente do cliente. |
| `categoria_preferencial` | Texto | Categoria de produto mais frequente do cliente. |

### dim_canais.csv

| Coluna | Tipo recomendado no Power BI | Uso |
|---|---|---|
| `id_canal` | Numero inteiro | Chave primaria da dimensão de canal. |
| `canal_venda` | Texto | Nome do canal: App, Parceiro ou Loja Física. |
| `tipo_canal` | Texto | Classificação executiva do canal. |

### dim_tempo.csv

| Coluna | Tipo recomendado no Power BI | Uso |
|---|---|---|
| `data_venda` | Data | Chave primaria da dimensão de tempo. |
| `ano` | Numero inteiro | Ano da venda. |
| `mes` | Numero inteiro | Numero do mês. |
| `nome_mes` | Texto | Nome do mês para exibicao. |
| `ano_mes` | Texto | Período mensal no formato `YYYY-MM`. |
| `ordem_ano_mes` | Numero inteiro | Coluna de ordenacao de `ano_mes`. |
| `trimestre_numero` | Numero inteiro | Numero do trimestre. |
| `trimestre` | Texto | Trimestre no formato `T1`, `T2`, `T3`, `T4`. |
| `dia_mes` | Numero inteiro | Dia do mês. |
| `numero_dia_semana` | Numero inteiro | Dia da semana numerico, segunda = 1. |
| `dia_semana` | Texto | Nome do dia da semana. |
| `fim_de_semana` | Verdadeiro/Falso | Indica sabado ou domingo. |

## Como Importar No Power BI

1. Abra o Power BI Desktop.
2. Selecione `Obter dados` > `Texto/CSV`.
3. Importe os cinco arquivos da pasta `data/powerbi/`.
4. No Power Query, confira os tipos de dados:
   - datas como `Data`;
   - valores monetarios como `Numero decimal`;
   - flags como `Verdadeiro/Falso`;
   - chaves de texto como `Texto`.
5. Renomeie as consultas, se necessário, mantendo os nomes:
   - `fato_vendas`
   - `dim_produtos`
   - `dim_clientes`
   - `dim_canais`
   - `dim_tempo`
6. Carregue os dados no modelo.
7. Em `Modelagem`, marque `dim_tempo` como tabela de datas usando a coluna `data_venda`.
8. Ordene:
   - `dim_tempo[nome_mes]` por `dim_tempo[mes]`;
   - `dim_tempo[ano_mes]` por `dim_tempo[ordem_ano_mes]`;
   - `dim_tempo[dia_semana]` por `dim_tempo[numero_dia_semana]`.

## Relacionamentos Recomendados

| Tabela origem | Coluna origem | Tabela destino | Coluna destino | Cardinalidade | Direcao de filtro |
|---|---|---|---|---|---|
| `dim_tempo` | `data_venda` | `fato_vendas` | `data_venda` | Um para muitos | Simples |
| `dim_produtos` | `id_produto` | `fato_vendas` | `id_produto` | Um para muitos | Simples |
| `dim_clientes` | `id_cliente` | `fato_vendas` | `id_cliente` | Um para muitos | Simples |
| `dim_canais` | `id_canal` | `fato_vendas` | `id_canal` | Um para muitos | Simples |

Evite relacionamentos muitos-para-muitos e filtros bidirecionais nesta versão. O modelo estrela já atende as principais perguntas executivas com melhor performance e menor risco de ambiguidade.

## Medidas DAX Principais

Crie uma tabela vazia chamada `Medidas` no Power BI e adicione as medidas abaixo.

```DAX
Receita Total =
SUM ( fato_vendas[receita_transacao] )
```

```DAX
Total de Vendas =
DISTINCTCOUNT ( fato_vendas[id_transacao] )
```

```DAX
Volume Vendido =
SUM ( fato_vendas[quantidade_vendida] )
```

```DAX
Ticket Medio =
DIVIDE ( [Receita Total], [Total de Vendas] )
```

```DAX
Clientes Unicos =
DISTINCTCOUNT ( fato_vendas[id_cliente] )
```

```DAX
Frequencia Media de Compra =
DIVIDE ( [Total de Vendas], [Clientes Unicos] )
```

```DAX
Receita com Promocao =
CALCULATE (
    [Receita Total],
    fato_vendas[status_promocao] = "Com Promocao"
)
```

```DAX
Receita sem Promocao =
CALCULATE (
    [Receita Total],
    fato_vendas[status_promocao] = "Sem Promocao"
)
```

```DAX
Crescimento Mensal =
VAR ReceitaMesAnterior =
    CALCULATE (
        [Receita Total],
        DATEADD ( dim_tempo[data_venda], -1, MONTH )
    )
RETURN
    DIVIDE ( [Receita Total] - ReceitaMesAnterior, ReceitaMesAnterior )
```

```DAX
Receita por Canal =
[Receita Total]
```

Use está medida em gráficos filtrados por `dim_canais[canal_venda]`.

```DAX
Participacao por Categoria =
DIVIDE (
    [Receita Total],
    CALCULATE ( [Receita Total], ALL ( dim_produtos ) )
)
```

Use está medida em visuais por `dim_produtos[tipo_sorvete]`.

### Medidas Complementares Recomendadas

```DAX
Preco Medio Unitario =
DIVIDE ( [Receita Total], [Volume Vendido] )
```

```DAX
Receita Media Diaria =
AVERAGEX (
    VALUES ( dim_tempo[data_venda] ),
    [Receita Total]
)
```

```DAX
Clientes Recorrentes =
CALCULATE (
    [Clientes Unicos],
    dim_clientes[cliente_recorrente] = TRUE ()
)
```

```DAX
Taxa de Recorrencia =
DIVIDE ( [Clientes Recorrentes], [Clientes Unicos] )
```

```DAX
Ticket Medio com Promocao =
DIVIDE (
    [Receita com Promocao],
    CALCULATE ( [Total de Vendas], fato_vendas[status_promocao] = "Com Promocao" )
)
```

```DAX
Ticket Medio sem Promocao =
DIVIDE (
    [Receita sem Promocao],
    CALCULATE ( [Total de Vendas], fato_vendas[status_promocao] = "Sem Promocao" )
)
```

## Páginas De Dashboard Recomendadas

### 1. Visão Executiva

Objetivo: mostrar a saúde geral do negócio.

Elementos:

- Cards: Receita Total, Total de Vendas, Ticket Médio, Volume Vendido e Clientes Únicos.
- Linha mensal: Receita Total por `dim_tempo[ano_mes]`.
- Barras: Receita por Canal.
- Barras: Receita por Categoria.
- Destaque textual: queda de agosto e eficiência de promoções.

### 2. Performance Financeira

Objetivo: analisar receita, ticket e crescimento.

Elementos:

- Linha de Receita Total e Crescimento Mensal.
- Matriz por mês com Receita Total, Total de Vendas, Ticket Médio e Volume Vendido.
- Grafico de participação por categoria.
- Ranking de produtos por receita.

### 3. Canais E Promocoes

Objetivo: entender desempenho comercial por origem da venda e impacto de desconto.

Elementos:

- Barras comparando App, Parceiro e Loja Física.
- Matriz de canal por status_promocao.
- Cards: Receita com Promocao, Receita sem Promocao, Ticket Médio com Promocao e Ticket Médio sem Promocao.
- Grafico de barras para Receita por Canal.

### 4. Operação E Sazonalidade

Objetivo: orientar escala, estoque e horários de maior demanda.

Elementos:

- Heatmap de `dim_tempo[dia_semana]` por `fato_vendas[faixa_horaria]`.
- Barras por `fato_vendas[hora]`.
- Linha mensal de Volume Vendido.
- Segmentadores de trimestre, mês, dia da semana e faixa horária.

### 5. Clientes E Recorrência

Objetivo: acompanhar comportamento de compra e valor do cliente.

Elementos:

- Cards: Clientes Únicos, Frequência Média de Compra, Clientes Recorrentes e Taxa de Recorrência.
- Barras por `dim_clientes[faixa_frequencia_cliente]`.
- Barras por `dim_clientes[segmento_valor_cliente]`.
- Matriz com canal preferencial, categoria preferencial, receita e ticket.

## Boas Praticas De Modelo

- Oculte na visualizacao de relatório as chaves técnicas `id_produto`, `id_canal` e, se preferir, `id_transacao`.
- Mantenha campos monetarios formatados como moeda brasileira.
- Mantenha percentuais como porcentagem com uma casa decimal.
- Use `dim_tempo` como unica tabela de calendário para medidas temporais.
- Evite usar colunas agregadas da dimensão cliente como substitutas das medidas principais. Para indicadores dinamicos, prefira medidas calculadas sobre `fato_vendas`.
- Use segmentadores principais: período, canal, categoria, promoção e segmento de cliente.

## Observacoes De Governança

- A camada `data/powerbi/` e derivada da camada processada e pode ser regenerada.
- O CSV tratado original permanece inalterado.
- Caso a base processada seja atualizada, execute novamente:

```powershell
.\.venv\Scripts\python.exe scripts/export_powerbi_model.py
```

- A dimensão de clientes contem atributos calculados com base no historico observado. Se o período da base mudar, segmentos de frequência e valor também podem mudar.
