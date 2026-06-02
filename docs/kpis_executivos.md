# KPIs Executivos - Case Sorveteria Analytics

Fonte analisada: `data/processed/vendas_sorvetes_tratado.csv`
Período da base: 20/02/2025 a 20/09/2025
Granularidade: uma linha por transação de venda
Registros válidos analisados: 48.491

## Sumário Executivo

A sorveteria gerou R$ 1.366.105,34 de receita em 48.491 vendas válidas, com 149.400 unidades vendidas e ticket médio de R$ 28,17. O negócio apresenta boa distribuição de canais: Parceiro, App e Loja Física contribuem cada um com aproximadamente um terço da receita, reduzindo dependência excessiva de um único canal comercial.

O principal motor de receita é o Milkshake, responsável por 25,9% do faturamento, acima das demais categorias, que ficam muito próximas entre 18,5% e 18,7%. A operação também apresenta forte recorrência: 97,6% dos clientes fizeram mais de uma compra na base analisada, com média de 5,4 transações por cliente e intervalo mediano de 20 dias entre compras.

O maior ponto de atenção executivo está na queda de agosto. Considerando apenas meses completos, março a julho sustentaram receita diária próxima de R$ 7,2 mil a R$ 7,5 mil. Em agosto, a receita diária caiu para R$ 5,2 mil, redução de 30,7% contra julho. A validação posterior confirmou que a queda abrupta de registros a partir de 22/08/2025 já estava presente no dataset bruto original, portanto o período posterior a essa data deve ser interpretado como limitação da fonte de dados. Setembro e fevereiro são meses parciais na base e devem ser tratados com cautela em comparações mensais.

Outro sinal relevante está nas promoções. Vendas promocionais representam praticamente metade das transações, mas geram apenas 45,4% da receita. O ticket médio com promoção e R$ 25,55, contra R$ 30,80 sem promoção. Isso sugere que as promoções estão reduzindo valor médio de compra sem evidenciar ganho proporcional de volume.

## Premissas Analíticas

- Receita foi calculada pela coluna `receita_transacao`.
- Volume vendido foi calculado pela soma de `quantidade_vendida`.
- Transações foram calculadas por `id_transacao`, que é único na base processada.
- A base não possui custo, margem ou CMV. Por isso, "produtos mais lucrativos" foi interpretado como produtos de maior geração de receita, uma proxy comercial de lucratividade. Para margem real, seria necessário incluir custo unitário por produto.
- Fevereiro e setembro são meses parciais. Comparações de crescimento mensal devem priorizar os meses completos de março a agosto.
- A redução abrupta de registros após 22/08/2025 foi confirmada no dataset bruto original e não foi causada pelo tratamento, modelagem ou dashboard. Nenhum valor foi imputado para recompor esse período.
- A recorrência foi analisada pelo comportamento observado na base final, usando transações por `id_cliente`.

## Números-Chave

| Indicador | Resultado | Leitura executiva |
|---|---:|---|
| Receita total | R$ 1.366.105,34 | Base comercial relevante para decisão gerencial e construção de dashboard executivo. |
| Vendas válidas | 48.491 | Alto volume transacional, suficiente para leitura de padrões por canal, produto, horário e cliente. |
| Unidades vendidas | 149.400 | Média de 3,08 unidades por venda, indicando compras frequentemente multiproduto ou em maior quantidade. |
| Ticket médio | R$ 28,17 | Referência central para metas de upsell, combos e campanhas de aumento de valor por pedido. |
| Clientes únicos | 8.970 | Base de clientes ampla para análise de recorrência e segmentação. |
| Transações por cliente | 5,4 em média | Sinal forte de recompra e potencial para programas de fidelidade. |
| Intervalo mediano entre compras | 20 dias | Cadência útil para campanhas de reativação e CRM. |

## KPIs Financeiros

### Visão Consolidada

| KPI | Fórmula utilizada | Resultado observado | Significado | Importância para o negócio | Possível uso executivo | Possíveis insights gerados |
|---|---|---:|---|---|---|---|
| Receita total | `SUM(receita_transacao)` | R$ 1.366.105,34 | Soma de todo o faturamento validado no período. | Mede o tamanho econômico da operação e serve como indicador principal de performance comercial. | Definir metas mensais, avaliar expansão, priorizar investimentos e acompanhar crescimento. | A receita está distribuída entre canais e categorias, mas há queda relevante em agosto associada a limitação de registros na fonte original. |
| Ticket médio | `SUM(receita_transacao) / COUNT(id_transacao)` | R$ 28,17 | Valor médio gerado por venda. | Indica capacidade de capturar valor por pedido, independentemente do volume de clientes. | Criar metas de aumento de ticket por combos, adicionais, cross-sell e campanhas de recompra. | O ticket sem promoção é R$ 30,80, enquanto o promocional é R$ 25,55; há perda de valor médio quando a promoção é aplicada. |
| Receita por venda | `AVG(receita_transacao)`, com apoio de mediana e percentis | Média R$ 28,17; mediana R$ 25,64; P75 R$ 38,76 | Mostra a distribuição de valor por transação, não apenas a média geral. | Ajuda a entender se a receita depende de muitas vendas pequenas ou de uma fatia de pedidos maiores. | Segmentar ofertas por faixa de gasto e desenhar benefícios para elevar clientes da mediana para o quartil superior. | A mediana abaixo da média indica presença de vendas de maior valor puxando o resultado; há espaço para aumentar pedidos médios com kits e adicionais. |
| Crescimento mensal | `(Receita mes atual / Receita mes anterior) - 1` | Março a agosto: média -5,3%; agosto -30,7% vs julho | Mede a evolução temporal da receita. | Mostra se o negócio está crescendo, estável ou perdendo tração. | Acompanhar metas mensais, planejar estoque, equipe e campanhas sazonais. | Março a julho ficaram estáveis em torno de R$ 220 mil a R$ 233 mil; agosto rompeu o padrão, mas a leitura é limitada pela queda de registros na fonte após 22/08/2025. |
| Receita por canal | `SUM(receita_transacao)` por `canal_venda` | Parceiro R$ 459,3 mil; App R$ 454,1 mil; Loja Física R$ 452,7 mil | Mede a contribuição financeira de cada canal. | Revela dependência ou equilíbrio entre canais de venda. | Alocar verba comercial, negociar com parceiros, priorizar UX do app e dimensionar loja física. | Os canais estão muito equilibrados, cada um com cerca de 33% da receita; a estratégia deve buscar rentabilidade por canal, não apenas volume. |
| Produtos mais lucrativos | `SUM(receita_transacao)` por `tipo_sorvete` e `sabor` | Milkshake: R$ 353,9 mil; top SKU: Milkshake de Açaí, R$ 46,4 mil | Ranking de produtos por geração de receita, usado como proxy de lucratividade. | Identifica produtos que sustentam faturamento e merecem prioridade comercial e operacional. | Definir mix, estoque, campanhas, destaque em cardápio e ofertas de alto valor. | Milkshake domina o ranking: os 8 principais sabores de Milkshake aparecem no topo por receita. |
| Participação percentual por categoria | `Receita da categoria / Receita total` | Milkshake 25,9%; demais categorias entre 18,5% e 18,7% | Mede o peso relativo de cada categoria no faturamento. | Ajuda a proteger categorias relevantes e identificar oportunidades de crescimento no mix. | Ajustar sortimento, precificação e exposição no app, loja e parceiros. | O mix é equilibrado, mas Milkshake tem papel de categoria âncora e pode ser usado como produto de atração para combos. |

### Receita Mensal

| Mês | Receita | Vendas | Receita média diária | Crescimento vs mês anterior | Leitura executiva |
|---|---:|---:|---:|---:|---|
| Fevereiro | R$ 65.563,80 | 2.382 | R$ 7.284,87 | N/A | Mês parcial, iniciado em 20/02. Não deve ser comparado diretamente com meses completos. |
| Março | R$ 224.350,82 | 8.002 | R$ 7.237,12 | N/A para leitura limpa | Primeiro mês completo, usado como referência inicial. |
| Abril | R$ 220.823,30 | 7.846 | R$ 7.360,78 | -1,6% | Receita praticamente estável, sem sinal de perda estrutural. |
| Maio | R$ 232.593,92 | 8.246 | R$ 7.503,03 | 5,3% | Melhor mês em receita, indicando pico de demanda ou execução comercial mais forte. |
| Junho | R$ 220.432,96 | 7.827 | R$ 7.347,77 | -5,2% | Recuo moderado, ainda dentro da faixa histórica de estabilidade. |
| Julho | R$ 232.592,11 | 8.167 | R$ 7.502,97 | 5,5% | Retomada ao patamar de maio, confirmando capacidade de operar acima de R$ 230 mil mensais. |
| Agosto | R$ 161.166,63 | 5.714 | R$ 5.198,92 | -30,7% | Queda material influenciada pela redução abrupta de registros na fonte original a partir de 22/08/2025. |
| Setembro | R$ 8.581,80 | 307 | R$ 429,09 | N/A | Mês parcial até 20/09 e possivelmente incompleto em carga de dados. Não usar para conclusão de performance. |

### Receita Por Canal

| Canal | Receita | Participação | Vendas | Ticket médio | Leitura executiva |
|---|---:|---:|---:|---:|---|
| Parceiro | R$ 459.272,58 | 33,6% | 16.263 | R$ 28,24 | Levemente líder em receita e volume. Deve ser monitorado por comissão e margem real. |
| App | R$ 454.144,95 | 33,2% | 16.115 | R$ 28,18 | Canal próprio com peso equivalente aos demais; pode ser usado para CRM e campanhas de maior controle. |
| Loja Física | R$ 452.687,81 | 33,1% | 16.113 | R$ 28,09 | Mantém relevância mesmo com canais digitais fortes; importante para experiência e conveniência local. |

### Participação Por Categoria

| Categoria | Receita | Participação | Vendas | Ticket médio | Leitura executiva |
|---|---:|---:|---:|---:|---|
| Milkshake | R$ 353.892,93 | 25,9% | 11.598 | R$ 30,51 | Categoria líder em receita, ticket e penetração de clientes. Deve ser tratada como produto âncora. |
| Sundae | R$ 254.810,39 | 18,7% | 9.307 | R$ 27,38 | Categoria relevante, com peso similar a Casquinha, Pote e Picolé. |
| Casquinha | R$ 253.085,49 | 18,5% | 9.148 | R$ 27,67 | Boa participação e ticket levemente superior ao grupo intermediário. |
| Pote | R$ 252.167,48 | 18,5% | 9.213 | R$ 27,37 | Categoria estável, útil para estratégias de volume e kits. |
| Picolé | R$ 252.149,05 | 18,5% | 9.225 | R$ 27,33 | Categoria com receita semelhante a Pote e Casquinha, reforçando mix equilibrado. |

### Produtos De Maior Geração De Receita

| Ranking | Produto | Receita | Vendas | Unidades | Ticket médio | Participação na receita |
|---:|---|---:|---:|---:|---:|---:|
| 1 | Milkshake - Açaí | R$ 46.374,46 | 1.491 | 5.009 | R$ 31,10 | 3,4% |
| 2 | Milkshake - Caramelo | R$ 45.728,14 | 1.491 | 5.001 | R$ 30,67 | 3,3% |
| 3 | Milkshake - Limão | R$ 45.117,38 | 1.472 | 4.949 | R$ 30,65 | 3,3% |
| 4 | Milkshake - Menta | R$ 44.354,81 | 1.439 | 4.853 | R$ 30,82 | 3,2% |
| 5 | Milkshake - Baunilha | R$ 44.201,08 | 1.434 | 4.735 | R$ 30,82 | 3,2% |
| 6 | Milkshake - Cookies | R$ 43.669,46 | 1.437 | 4.761 | R$ 30,39 | 3,2% |
| 7 | Milkshake - Morango | R$ 42.506,39 | 1.447 | 4.692 | R$ 29,38 | 3,1% |
| 8 | Milkshake - Chocolate | R$ 41.941,21 | 1.387 | 4.555 | R$ 30,24 | 3,1% |
| 9 | Sundae - Limão | R$ 33.739,83 | 1.178 | 3.650 | R$ 28,64 | 2,5% |
| 10 | Sundae - Menta | R$ 33.574,01 | 1.213 | 3.683 | R$ 27,68 | 2,5% |

Leitura executiva: os oito primeiros produtos por receita são Milkshakes. Isso reforca que a categoria não lidera apenas por volume agregado; ela domina também no nivel de SKU. A empresa deve proteger disponibilidade desses sabores, acompanhar ruptura de estoque e testar bundles com produtos complementares para ampliar margem por pedido.

## KPIs Operacionais

### Visão Consolidada

| KPI | Fórmula utilizada | Resultado observado | Significado | Importância para o negócio | Possível uso executivo | Possíveis insights gerados |
|---|---|---:|---|---|---|---|
| Volume vendido | `SUM(quantidade_vendida)` | 149.400 unidades | Quantidade total de itens vendidos. | Orienta produção, compras, estoque e capacidade operacional. | Planejar materia-prima, reposição, escala de equipe e metas de produtividade. | A média de 3,08 unidades por venda indica boa oportunidade para combos e venda agregada. |
| Horarios de pico | `COUNT(id_transacao)` por `hora` | 18h: 3.356 vendas; 19h: 3.300; 10h: 3.288 | Identifica os horários de maior fluxo. | Ajuda a dimensionar equipe, preparo e atendimento nos momentos criticos. | Ajustar escala, preparar insumos antes do pico e calibrar campanhas por hora. | O pico não está concentrado em um único horário; há forte demanda no fim da tarde/noite e também as 10h. |
| Vendas por faixa de horário | `COUNT(id_transacao)` por `faixa_horaria` | Tarde 39,9%; Noite 33,7%; Manha 26,4% das vendas | Mostra a distribuição operacional do fluxo ao longo do dia. | Define quando a operação precisa de maior capacidade e maior velocidade de atendimento. | Organizar turnos, estoque de frente de loja e janela de campanhas. | A tarde concentra maior volume, mas a noite tem maior receita por slot ativo, sugerindo maior eficiência operacional. |
| Sazonalidade | `SUM(receita_transacao)` por mês/trimestre | T2: 49,3% da receita; T3: 29,5%; T1: 21,2% | Mede variacao temporal de demanda. | Permite antecipar picos e quedas por período. | Planejar estoque, escala e calendário promocional. | T2 foi o período mais forte, mas a leitura e influenciada por meses parciais em T1 e T3; agosto e o principal alerta dentro dos meses completos. |
| Impacto das promoções | Comparação entre `Com Promocao` e `Sem Promocao` | Promo: 50,1% das vendas e 45,4% da receita | Mede efeito das promoções sobre volume, ticket e receita. | Avalia se desconto está gerando incremento real ou apenas diluindo receita. | Revisar política promocional, limitar descontos e testar ofertas por combo em vez de preço. | Promocoes reduzem o ticket em 17,0% e não mostram ganho expressivo de volume; há risco de erosão de receita. |
| Desempenho por dia da semana | `SUM(receita_transacao)` e `COUNT(id_transacao)` por `dia_semana` | Quinta: R$ 203,5 mil e 7.215 vendas | Mede diferencas de demanda no ciclo semanal. | Apoia escala, campanhas e metas por dia. | Reforcar equipe em dias fortes e criar ativacoes em dias fracos. | Quinta-feira lidera em receita e vendas; segunda e o menor dia em receita total. |
| Eficiencia operacional de vendas | `Vendas / slots ativos` e `Receita / slots ativos` por faixa | Noite: 16,13 vendas/slot e R$ 457,53/slot | Mede produtividade da operação por janela ativa de venda. | Ajuda a comparar faixas horarias considerando intensidade operacional. | Ajustar capacidade por turno e investigar gargalos em faixas com alto volume e menor receita por slot. | A tarde tem maior receita total, mas a noite entrega maior produtividade por slot ativo. |

### Faixas De Horário

| Faixa | Receita | Vendas | Unidades | Ticket médio | Receita por slot ativo | Leitura executiva |
|---|---:|---:|---:|---:|---:|---|
| Tarde | R$ 541.943,17 | 19.326 | 59.404 | R$ 28,04 | R$ 444,22 | Principal janela de demanda. Exige disponibilidade de produto e equipe bem dimensionada. |
| Noite | R$ 463.475,96 | 16.342 | 50.576 | R$ 28,36 | R$ 457,53 | Menor volume que a tarde, mas maior ticket e produtividade por slot. Boa janela para upsell. |
| Manha | R$ 360.686,21 | 12.823 | 39.420 | R$ 28,13 | R$ 446,39 | Menor volume total, mas com produtividade por slot próxima das demais faixas. |

### Dias Da Semana

| Dia | Receita | Vendas | Receita média por dia ativo | Leitura executiva |
|---|---:|---:|---:|---|
| Segunda | R$ 190.343,63 | 6.764 | R$ 6.344,79 | Menor receita total; oportunidade para campanhas de início de semana. |
| Terça | R$ 193.912,47 | 6.898 | R$ 6.463,75 | Desempenho intermediário, próximo da média semanal. |
| Quarta | R$ 194.347,48 | 6.796 | R$ 6.478,25 | Receita consistente, com ticket acima da média semanal. |
| Quinta | R$ 203.532,46 | 7.215 | R$ 6.565,56 | Melhor dia da semana; deve receber reforco operacional e campanhas de maior margem. |
| Sexta | R$ 194.512,16 | 6.854 | R$ 6.274,59 | Volume abaixo do esperado para fim de semana; merece investigação por canal e horário. |
| Sábado | R$ 196.266,92 | 7.072 | R$ 6.331,19 | Bom volume, mas ticket médio menor que quarta e sexta. |
| Domingo | R$ 193.190,22 | 6.892 | R$ 6.439,67 | Demanda estável, adequada para ações familiares e combos. |

### Promocoes

| Status | Receita | Participação na receita | Vendas | Ticket médio | Preco unitário médio | Leitura executiva |
|---|---:|---:|---:|---:|---:|---|
| Sem Promocao | R$ 745.724,31 | 54,6% | 24.214 | R$ 30,80 | R$ 10,01 | Vendas sem desconto sustentam a maior parte da receita e maior valor por pedido. |
| Com Promocao | R$ 620.381,03 | 45,4% | 24.277 | R$ 25,55 | R$ 8,27 | Promocao aumenta ligeiramente o numero de vendas, mas captura menos receita. |

Leitura executiva: a promoção gera 63 vendas a mais que o grupo sem promoção, mas R$ 125,3 mil a menos em receita. Isso indica que, no desenho atual, desconto parece atuar mais como redução de preço do que como alavanca clara de volume. A recomendacao e testar promoções condicionadas a maior quantidade, combos de maior margem ou benefícios por recorrência, evitando descontos amplos sem contrapartida.

## KPIs De Cliente

### Visão Consolidada

| KPI | Fórmula utilizada | Resultado observado | Significado | Importância para o negócio | Possível uso executivo | Possíveis insights gerados |
|---|---|---:|---|---|---|---|
| Frequência de compra | `COUNT(id_transacao) / COUNTD(id_cliente)` | 5,4 compras por cliente | Média de transações realizadas por cliente no período. | Mede intensidade de relacionamento e potencial de receita recorrente. | Criar metas de recompra, segmentar clientes frequentes e calibrar CRM. | A base apresenta alta frequência, sugerindo que estratégias de fidelidade podem ter retorno relevante. |
| Recorrência | `% de clientes com mais de 1 transacao` | 97,6% dos clientes | Mede proporcao de clientes que voltaram a comprar. | Indica fidelidade, aceitacao do produto e dependência menor de aquisicao de novos clientes. | Criar programa de fidelidade, benefícios progressivos e campanhas de reativação. | A recorrência e muito alta; o desafio passa a ser aumentar valor por cliente, não apenas trazer clientes de volta. |
| Comportamento de compra | `Distribuicao de quantidade_vendida` e `receita_transacao` | 61,8% das vendas tem 3 a 5 unidades | Descreve o padrão de tamanho do pedido. | Ajuda a montar combos, embalagens, ofertas e metas de upsell. | Criar combos para 3, 4 e 5 itens, com incentivo para migrar pedidos pequenos para faixas maiores. | Pedidos de 4 e 5 unidades geram juntos R$ 810,9 mil, quase 59,4% da receita. |
| Preferencias de produtos | `COUNTD(id_cliente)` e `SUM(receita_transacao)` por produto | 72,4% dos clientes compraram Milkshake | Mostra quais produtos tem maior alcance e atratividade. | Define prioridade de portfólio e comunicação. | Dar destaque a Milkshake no cardápio e usar categorias complementares como cross-sell. | Milkshake combina maior penetração de clientes com maior receita; e categoria âncora para retenção e ticket. |
| Padrões de consumo | `nunique(canal_venda)` e `nunique(tipo_sorvete)` por cliente | 92,9% usam 2 ou mais canais; 77,9% compram 3 ou mais categorias | Mede diversidade de relacionamento e consumo. | Indica se o cliente se comporta de forma omnicanal e multiproduto. | Unificar CRM por canal, criar ofertas personalizadas e evitar campanhas isoladas por canal. | A maioria dos clientes transita entre canais e categorias; a estratégia deve ser integrada. |
| Canais mais utilizados pelos clientes | `COUNT(id_transacao)` e `COUNTD(id_cliente)` por canal | Parceiro: 16.263 vendas; App: 16.115; Loja: 16.113 | Identifica onde os clientes compram. | Ajuda a priorizar investimentos de atendimento, tecnologia e parcerias. | Otimizar app, negociar parceiros e manter padrão de experiência na loja. | Como os canais são equilibrados, pequenas melhorias de conversao ou ticket em qualquer canal podem gerar impacto relevante. |

### Recorrência E Frequência

| Indicador | Resultado | Interpretacao executiva |
|---|---:|---|
| Clientes únicos | 8.970 | Base suficiente para segmentação comercial e análise de comportamento. |
| Média de transações por cliente | 5,4 | Cliente médio compra varias vezes dentro do período analisado. |
| Mediana de transações por cliente | 5 | Recorrência não depende apenas de poucos clientes extremos. |
| Clientes com compra unica | 2,4% | Baixo percentual de clientes pontuais. |
| Clientes recorrentes | 97,6% | Forte sinal de aceitacao e habito de compra. |
| Intervalo mediano entre compras | 20 dias | Boa janela para campanhas de reativação entre 15 e 25 dias após a ultima compra. |
| Top 20% clientes por receita | 34,9% da receita | Concentracao moderada; há clientes valiosos, mas a receita não está excessivamente dependente deles. |

### Comportamento Por Quantidade Comprada

| Quantidade por venda | Vendas | Receita | Participação nas vendas | Leitura executiva |
|---:|---:|---:|---:|---|
| 1 unidade | 9.079 | R$ 82.708,76 | 18,7% | Publico de compra pequena; alvo para adicionais simples. |
| 2 unidades | 9.200 | R$ 167.619,56 | 19,0% | Faixa natural para oferta "leve 3" ou combo casal/familia. |
| 3 unidades | 9.915 | R$ 272.077,66 | 20,4% | Uma das faixas centrais de consumo. |
| 4 unidades | 9.908 | R$ 362.704,36 | 20,4% | Alta relevância financeira; bom alvo para combos de maior margem. |
| 5 unidades | 9.790 | R$ 448.169,17 | 20,2% | Maior bloco de receita; indica compras familiares ou de grupo. |
| 6 unidades | 599 | R$ 32.825,83 | 1,2% | Nicho pequeno, possível oportunidade para kits maiores. |

## Padrões Importantes Encontrados

1. A receita e bem distribuída por canal. Parceiro, App e Loja Física ficam entre 33,1% e 33,6% da receita, o que reduz risco de dependência, mas exige gestão omnicanal consistente.

2. Milkshake e a categoria líder. Com R$ 353,9 mil em receita e 25,9% de participação, e também a categoria com maior alcance de clientes. A empresa deve trata-la como categoria estratégica, não apenas como mais um item do cardápio.

3. O negócio tem forte comportamento recorrente. A mediana de 5 compras por cliente e o intervalo mediano de 20 dias sugerem um ciclo de recompra previsível, útil para CRM e campanhas de fidelização.

4. A tarde concentra o maior volume absoluto, mas a noite apresenta maior produtividade por slot ativo e maior ticket. Isso indica que estratégias de upsell podem funcionar especialmente bem no período noturno.

5. Promocoes não estão gerando ganho proporcional de volume. O numero de vendas promocionais e quase igual ao de vendas sem promoção, mas o ticket promocional é 17,0% menor.

6. Agosto apresenta ruptura de performance, mas a validação confirmou limitação de origem dos dados a partir de 22/08/2025. A queda de 30,7% contra julho deve ser interpretada com cautela, pois pode não representar integralmente o comportamento real da operação.

## Possíveis Gargalos

| Gargalo | Evidencia nos dados | Impacto potencial | Acao recomendada |
|---|---|---|---|
| Queda de agosto | Receita diária caiu de R$ 7.502,97 em julho para R$ 5.198,92 em agosto; houve queda abrupta de registros na fonte original após 22/08/2025 | Limitação de confiabilidade para indicadores temporais após essa data | Preservar os dados sem imputação e interpretar o período posterior a 22/08/2025 com cautela. |
| Promocoes com baixa eficiência | Promocao tem 50,1% das vendas, mas apenas 45,4% da receita | Desconto pode estar reduzindo margem e receita por pedido | Trocar desconto direto por combos, benefícios progressivos e ofertas condicionadas a quantidade minima. |
| Dependencia estratégica do Milkshake | Milkshake gera 25,9% da receita e lidera o ranking de produtos | Ruptura de insumo ou queda de demanda nessa categoria afetaria fortemente o faturamento | Garantir estoque, qualidade e comunicação da categoria; testar extensoes de sabores e combos. |
| Segunda-feira mais fraca | Segunda tem menor receita total, R$ 190,3 mil | Capacidade comercial menos explorada no início da semana | Criar campanhas de segunda com foco em recompra, sem reduzir excessivamente o ticket. |
| Dados parciais e queda de registros | Período com início em 20/02, redução abrupta de registros após 22/08 e fim em 20/09 | Risco de conclusões incorretas sobre sazonalidade e tendência temporal | Usar média diária, marcar meses parciais e documentar a limitação da fonte nos dashboards. |

## Decisões Estrategicas Baseadas Nos Dados

1. Revisar a política promocional. O desenho atual reduz ticket sem demonstrar incremento relevante de vendas. A recomendacao e priorizar promoções de aumento de cesta, como combos de 4 ou 5 unidades, benefícios por recorrência e ofertas com produtos complementares.

2. Transformar Milkshake em categoria âncora. Como e o maior gerador de receita é o produto de maior penetração entre clientes, deve receber destaque no app, materiais de loja, campanhas com parceiros e testes de novos sabores.

3. Interpretar a queda de agosto como limitação de dados após 22/08/2025. Como a redução já estava no dataset bruto original, a decisão analítica foi preservar os dados sem imputação artificial e documentar o impacto nos indicadores temporais.

4. Criar estratégia de CRM baseada no ciclo de recompra. Com intervalo mediano de 20 dias entre compras, campanhas entre o 15o e o 25o dia após a ultima transação podem aumentar frequência sem depender de desconto generalizado.

5. Otimizar operação por horário. A tarde deve ser tratada como janela de volume e a noite como janela de valor. Isso permite diferenciar escala, estoque e tipo de oferta por faixa horária.

6. Fortalecer gestão omnicanal. Como 92,9% dos clientes usam dois ou mais canais, campanhas isoladas por canal podem perder contexto. A empresa deve acompanhar cliente, historico e preferências de forma integrada.

7. Proteger receita de pedidos de 4 e 5 unidades. Essas faixas somam R$ 810,9 mil, quase 59,4% da receita. Combos familiares e kits de maior valor devem ser tratados como alavanca central de crescimento.

## Recomendacoes Para Dashboard Executivo

| Area | Visual recomendado | Objetivo |
|---|---|---|
| Visão geral | Cards de Receita Total, Ticket Médio, Vendas, Unidades e Clientes | Dar leitura rápida da saúde do negócio. |
| Crescimento | Linha mensal com destaque para meses parciais | Separar tendência real de distorcao de período incompleto. |
| Canais | Barras de receita, vendas e ticket por canal | Comparar escala e valor capturado por canal. |
| Produto | Ranking de categorias e sabores por receita | Identificar produtos âncora e oportunidades de sortimento. |
| Operação | Heatmap de dia da semana por faixa horária | Apoiar escala, estoque e campanhas por janela de demanda. |
| Promocoes | Comparativo com/sem promoção por ticket, volume e receita | Avaliar eficiência de desconto. |
| Cliente | Frequência, recorrência, intervalo entre compras e canais usados | Direcionar CRM e fidelização. |

## Conclusão Executiva

A sorveteria tem uma base comercial saudavel, com receita relevante, canais equilibrados, alta recorrência e uma categoria líder clara. O potencial de crescimento parece menos dependente de aquisicao de novos clientes e mais associado a tres frentes: elevar ticket médio, melhorar eficiência promocional é explorar melhor o ciclo de recompra.

O principal risco de interpretação está na queda abrupta de agosto. A investigação confirmou que a redução de registros após 22/08/2025 já estava presente na fonte original, por isso conclusões sobre sazonalidade e tendência após essa data devem ser feitas com cautela. O principal ganho rápido está na revisão das promoções: os dados indicam que a empresa está concedendo desconto em volume alto de vendas sem capturar aumento proporcional de demanda. Uma estratégia mais executiva seria migrar de desconto amplo para ofertas condicionadas a cesta maior, recorrência e produtos de maior valor.
