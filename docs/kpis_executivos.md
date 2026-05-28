# KPIs Executivos - Case Sorveteria Analytics

Fonte analisada: `data/processed/vendas_sorvetes_tratado.csv`  
Periodo da base: 20/02/2025 a 20/09/2025  
Granularidade: uma linha por transacao de venda  
Registros validos analisados: 48.491

## Sumario Executivo

A sorveteria gerou R$ 1.366.105,34 de receita em 48.491 vendas validas, com 149.400 unidades vendidas e ticket medio de R$ 28,17. O negocio apresenta boa distribuicao de canais: Parceiro, App e Loja Fisica contribuem cada um com aproximadamente um terco da receita, reduzindo dependencia excessiva de um unico canal comercial.

O principal motor de receita e o Milkshake, responsavel por 25,9% do faturamento, acima das demais categorias, que ficam muito proximas entre 18,5% e 18,7%. A operacao tambem apresenta forte recorrencia: 97,6% dos clientes fizeram mais de uma compra na base analisada, com media de 5,4 transacoes por cliente e intervalo mediano de 20 dias entre compras.

O maior ponto de atencao executivo esta na queda de agosto. Considerando apenas meses completos, marco a julho sustentaram receita diaria proxima de R$ 7,2 mil a R$ 7,5 mil. Em agosto, a receita diaria caiu para R$ 5,2 mil, reducao de 30,7% contra julho. Setembro e fevereiro sao meses parciais na base e devem ser tratados com cautela em comparacoes mensais.

Outro sinal relevante esta nas promocoes. Vendas promocionais representam praticamente metade das transacoes, mas geram apenas 45,4% da receita. O ticket medio com promocao e R$ 25,55, contra R$ 30,80 sem promocao. Isso sugere que as promocoes estao reduzindo valor medio de compra sem evidenciar ganho proporcional de volume.

## Premissas Analiticas

- Receita foi calculada pela coluna `receita_transacao`.
- Volume vendido foi calculado pela soma de `quantidade_vendida`.
- Transacoes foram calculadas por `id_transacao`, que e unico na base processada.
- A base nao possui custo, margem ou CMV. Por isso, "produtos mais lucrativos" foi interpretado como produtos de maior geracao de receita, uma proxy comercial de lucratividade. Para margem real, seria necessario incluir custo unitario por produto.
- Fevereiro e setembro sao meses parciais. Comparacoes de crescimento mensal devem priorizar os meses completos de marco a agosto.
- A recorrencia foi analisada pelo comportamento observado na base final, usando transacoes por `id_cliente`.

## Numeros-Chave

| Indicador | Resultado | Leitura executiva |
|---|---:|---|
| Receita total | R$ 1.366.105,34 | Base comercial relevante para decisao gerencial e construcao de dashboard executivo. |
| Vendas validas | 48.491 | Alto volume transacional, suficiente para leitura de padroes por canal, produto, horario e cliente. |
| Unidades vendidas | 149.400 | Media de 3,08 unidades por venda, indicando compras frequentemente multiproduto ou em maior quantidade. |
| Ticket medio | R$ 28,17 | Referencia central para metas de upsell, combos e campanhas de aumento de valor por pedido. |
| Clientes unicos | 8.970 | Base de clientes ampla para analise de recorrencia e segmentacao. |
| Transacoes por cliente | 5,4 em media | Sinal forte de recompra e potencial para programas de fidelidade. |
| Intervalo mediano entre compras | 20 dias | Cadencia util para campanhas de reativacao e CRM. |

## KPIs Financeiros

### Visao Consolidada

| KPI | Formula utilizada | Resultado observado | Significado | Importancia para o negocio | Possivel uso executivo | Possiveis insights gerados |
|---|---|---:|---|---|---|---|
| Receita total | `SUM(receita_transacao)` | R$ 1.366.105,34 | Soma de todo o faturamento validado no periodo. | Mede o tamanho economico da operacao e serve como indicador principal de performance comercial. | Definir metas mensais, avaliar expansao, priorizar investimentos e acompanhar crescimento. | A receita esta distribuida entre canais e categorias, mas ha queda relevante em agosto que exige investigacao. |
| Ticket medio | `SUM(receita_transacao) / COUNT(id_transacao)` | R$ 28,17 | Valor medio gerado por venda. | Indica capacidade de capturar valor por pedido, independentemente do volume de clientes. | Criar metas de aumento de ticket por combos, adicionais, cross-sell e campanhas de recompra. | O ticket sem promocao e R$ 30,80, enquanto o promocional e R$ 25,55; ha perda de valor medio quando a promocao e aplicada. |
| Receita por venda | `AVG(receita_transacao)`, com apoio de mediana e percentis | Media R$ 28,17; mediana R$ 25,64; P75 R$ 38,76 | Mostra a distribuicao de valor por transacao, nao apenas a media geral. | Ajuda a entender se a receita depende de muitas vendas pequenas ou de uma fatia de pedidos maiores. | Segmentar ofertas por faixa de gasto e desenhar beneficios para elevar clientes da mediana para o quartil superior. | A mediana abaixo da media indica presenca de vendas de maior valor puxando o resultado; ha espaco para aumentar pedidos medios com kits e adicionais. |
| Crescimento mensal | `(Receita mes atual / Receita mes anterior) - 1` | Marco a agosto: media -5,3%; agosto -30,7% vs julho | Mede a evolucao temporal da receita. | Mostra se o negocio esta crescendo, estavel ou perdendo tracao. | Acompanhar metas mensais, planejar estoque, equipe e campanhas sazonais. | Marco a julho ficaram estaveis em torno de R$ 220 mil a R$ 233 mil; agosto rompeu o padrao e deve ser tratado como alerta. |
| Receita por canal | `SUM(receita_transacao)` por `canal_venda` | Parceiro R$ 459,3 mil; App R$ 454,1 mil; Loja Fisica R$ 452,7 mil | Mede a contribuicao financeira de cada canal. | Revela dependencia ou equilibrio entre canais de venda. | Alocar verba comercial, negociar com parceiros, priorizar UX do app e dimensionar loja fisica. | Os canais estao muito equilibrados, cada um com cerca de 33% da receita; a estrategia deve buscar rentabilidade por canal, nao apenas volume. |
| Produtos mais lucrativos | `SUM(receita_transacao)` por `tipo_sorvete` e `sabor` | Milkshake: R$ 353,9 mil; top SKU: Milkshake de Acai, R$ 46,4 mil | Ranking de produtos por geracao de receita, usado como proxy de lucratividade. | Identifica produtos que sustentam faturamento e merecem prioridade comercial e operacional. | Definir mix, estoque, campanhas, destaque em cardapio e ofertas de alto valor. | Milkshake domina o ranking: os 8 principais sabores de Milkshake aparecem no topo por receita. |
| Participacao percentual por categoria | `Receita da categoria / Receita total` | Milkshake 25,9%; demais categorias entre 18,5% e 18,7% | Mede o peso relativo de cada categoria no faturamento. | Ajuda a proteger categorias relevantes e identificar oportunidades de crescimento no mix. | Ajustar sortimento, precificacao e exposicao no app, loja e parceiros. | O mix e equilibrado, mas Milkshake tem papel de categoria ancora e pode ser usado como produto de atracao para combos. |

### Receita Mensal

| Mes | Receita | Vendas | Receita media diaria | Crescimento vs mes anterior | Leitura executiva |
|---|---:|---:|---:|---:|---|
| Fevereiro | R$ 65.563,80 | 2.382 | R$ 7.284,87 | N/A | Mes parcial, iniciado em 20/02. Nao deve ser comparado diretamente com meses completos. |
| Marco | R$ 224.350,82 | 8.002 | R$ 7.237,12 | N/A para leitura limpa | Primeiro mes completo, usado como referencia inicial. |
| Abril | R$ 220.823,30 | 7.846 | R$ 7.360,78 | -1,6% | Receita praticamente estavel, sem sinal de perda estrutural. |
| Maio | R$ 232.593,92 | 8.246 | R$ 7.503,03 | 5,3% | Melhor mes em receita, indicando pico de demanda ou execucao comercial mais forte. |
| Junho | R$ 220.432,96 | 7.827 | R$ 7.347,77 | -5,2% | Recuo moderado, ainda dentro da faixa historica de estabilidade. |
| Julho | R$ 232.592,11 | 8.167 | R$ 7.502,97 | 5,5% | Retomada ao patamar de maio, confirmando capacidade de operar acima de R$ 230 mil mensais. |
| Agosto | R$ 161.166,63 | 5.714 | R$ 5.198,92 | -30,7% | Queda material, com impacto de volume e nao de ticket. Deve ser investigada como desvio operacional, comercial ou sazonal. |
| Setembro | R$ 8.581,80 | 307 | R$ 429,09 | N/A | Mes parcial ate 20/09 e possivelmente incompleto em carga de dados. Nao usar para conclusao de performance. |

### Receita Por Canal

| Canal | Receita | Participacao | Vendas | Ticket medio | Leitura executiva |
|---|---:|---:|---:|---:|---|
| Parceiro | R$ 459.272,58 | 33,6% | 16.263 | R$ 28,24 | Levemente lider em receita e volume. Deve ser monitorado por comissao e margem real. |
| App | R$ 454.144,95 | 33,2% | 16.115 | R$ 28,18 | Canal proprio com peso equivalente aos demais; pode ser usado para CRM e campanhas de maior controle. |
| Loja Fisica | R$ 452.687,81 | 33,1% | 16.113 | R$ 28,09 | Mantem relevancia mesmo com canais digitais fortes; importante para experiencia e conveniencia local. |

### Participacao Por Categoria

| Categoria | Receita | Participacao | Vendas | Ticket medio | Leitura executiva |
|---|---:|---:|---:|---:|---|
| Milkshake | R$ 353.892,93 | 25,9% | 11.598 | R$ 30,51 | Categoria lider em receita, ticket e penetracao de clientes. Deve ser tratada como produto ancora. |
| Sundae | R$ 254.810,39 | 18,7% | 9.307 | R$ 27,38 | Categoria relevante, com peso similar a Casquinha, Pote e Picole. |
| Casquinha | R$ 253.085,49 | 18,5% | 9.148 | R$ 27,67 | Boa participacao e ticket levemente superior ao grupo intermediario. |
| Pote | R$ 252.167,48 | 18,5% | 9.213 | R$ 27,37 | Categoria estavel, util para estrategias de volume e kits. |
| Picole | R$ 252.149,05 | 18,5% | 9.225 | R$ 27,33 | Categoria com receita semelhante a Pote e Casquinha, reforcando mix equilibrado. |

### Produtos De Maior Geracao De Receita

| Ranking | Produto | Receita | Vendas | Unidades | Ticket medio | Participacao na receita |
|---:|---|---:|---:|---:|---:|---:|
| 1 | Milkshake - Acai | R$ 46.374,46 | 1.491 | 5.009 | R$ 31,10 | 3,4% |
| 2 | Milkshake - Caramelo | R$ 45.728,14 | 1.491 | 5.001 | R$ 30,67 | 3,3% |
| 3 | Milkshake - Limao | R$ 45.117,38 | 1.472 | 4.949 | R$ 30,65 | 3,3% |
| 4 | Milkshake - Menta | R$ 44.354,81 | 1.439 | 4.853 | R$ 30,82 | 3,2% |
| 5 | Milkshake - Baunilha | R$ 44.201,08 | 1.434 | 4.735 | R$ 30,82 | 3,2% |
| 6 | Milkshake - Cookies | R$ 43.669,46 | 1.437 | 4.761 | R$ 30,39 | 3,2% |
| 7 | Milkshake - Morango | R$ 42.506,39 | 1.447 | 4.692 | R$ 29,38 | 3,1% |
| 8 | Milkshake - Chocolate | R$ 41.941,21 | 1.387 | 4.555 | R$ 30,24 | 3,1% |
| 9 | Sundae - Limao | R$ 33.739,83 | 1.178 | 3.650 | R$ 28,64 | 2,5% |
| 10 | Sundae - Menta | R$ 33.574,01 | 1.213 | 3.683 | R$ 27,68 | 2,5% |

Leitura executiva: os oito primeiros produtos por receita sao Milkshakes. Isso reforca que a categoria nao lidera apenas por volume agregado; ela domina tambem no nivel de SKU. A empresa deve proteger disponibilidade desses sabores, acompanhar ruptura de estoque e testar bundles com produtos complementares para ampliar margem por pedido.

## KPIs Operacionais

### Visao Consolidada

| KPI | Formula utilizada | Resultado observado | Significado | Importancia para o negocio | Possivel uso executivo | Possiveis insights gerados |
|---|---|---:|---|---|---|---|
| Volume vendido | `SUM(quantidade_vendida)` | 149.400 unidades | Quantidade total de itens vendidos. | Orienta producao, compras, estoque e capacidade operacional. | Planejar materia-prima, reposicao, escala de equipe e metas de produtividade. | A media de 3,08 unidades por venda indica boa oportunidade para combos e venda agregada. |
| Horarios de pico | `COUNT(id_transacao)` por `hora` | 18h: 3.356 vendas; 19h: 3.300; 10h: 3.288 | Identifica os horarios de maior fluxo. | Ajuda a dimensionar equipe, preparo e atendimento nos momentos criticos. | Ajustar escala, preparar insumos antes do pico e calibrar campanhas por hora. | O pico nao esta concentrado em um unico horario; ha forte demanda no fim da tarde/noite e tambem as 10h. |
| Vendas por faixa de horario | `COUNT(id_transacao)` por `faixa_horaria` | Tarde 39,9%; Noite 33,7%; Manha 26,4% das vendas | Mostra a distribuicao operacional do fluxo ao longo do dia. | Define quando a operacao precisa de maior capacidade e maior velocidade de atendimento. | Organizar turnos, estoque de frente de loja e janela de campanhas. | A tarde concentra maior volume, mas a noite tem maior receita por slot ativo, sugerindo maior eficiencia operacional. |
| Sazonalidade | `SUM(receita_transacao)` por mes/trimestre | T2: 49,3% da receita; T3: 29,5%; T1: 21,2% | Mede variacao temporal de demanda. | Permite antecipar picos e quedas por periodo. | Planejar estoque, escala e calendario promocional. | T2 foi o periodo mais forte, mas a leitura e influenciada por meses parciais em T1 e T3; agosto e o principal alerta dentro dos meses completos. |
| Impacto das promocoes | Comparacao entre `Com Promocao` e `Sem Promocao` | Promo: 50,1% das vendas e 45,4% da receita | Mede efeito das promocoes sobre volume, ticket e receita. | Avalia se desconto esta gerando incremento real ou apenas diluindo receita. | Revisar politica promocional, limitar descontos e testar ofertas por combo em vez de preco. | Promocoes reduzem o ticket em 17,0% e nao mostram ganho expressivo de volume; ha risco de erosao de receita. |
| Desempenho por dia da semana | `SUM(receita_transacao)` e `COUNT(id_transacao)` por `dia_semana` | Quinta: R$ 203,5 mil e 7.215 vendas | Mede diferencas de demanda no ciclo semanal. | Apoia escala, campanhas e metas por dia. | Reforcar equipe em dias fortes e criar ativacoes em dias fracos. | Quinta-feira lidera em receita e vendas; segunda e o menor dia em receita total. |
| Eficiencia operacional de vendas | `Vendas / slots ativos` e `Receita / slots ativos` por faixa | Noite: 16,13 vendas/slot e R$ 457,53/slot | Mede produtividade da operacao por janela ativa de venda. | Ajuda a comparar faixas horarias considerando intensidade operacional. | Ajustar capacidade por turno e investigar gargalos em faixas com alto volume e menor receita por slot. | A tarde tem maior receita total, mas a noite entrega maior produtividade por slot ativo. |

### Faixas De Horario

| Faixa | Receita | Vendas | Unidades | Ticket medio | Receita por slot ativo | Leitura executiva |
|---|---:|---:|---:|---:|---:|---|
| Tarde | R$ 541.943,17 | 19.326 | 59.404 | R$ 28,04 | R$ 444,22 | Principal janela de demanda. Exige disponibilidade de produto e equipe bem dimensionada. |
| Noite | R$ 463.475,96 | 16.342 | 50.576 | R$ 28,36 | R$ 457,53 | Menor volume que a tarde, mas maior ticket e produtividade por slot. Boa janela para upsell. |
| Manha | R$ 360.686,21 | 12.823 | 39.420 | R$ 28,13 | R$ 446,39 | Menor volume total, mas com produtividade por slot proxima das demais faixas. |

### Dias Da Semana

| Dia | Receita | Vendas | Receita media por dia ativo | Leitura executiva |
|---|---:|---:|---:|---|
| Segunda | R$ 190.343,63 | 6.764 | R$ 6.344,79 | Menor receita total; oportunidade para campanhas de inicio de semana. |
| Terca | R$ 193.912,47 | 6.898 | R$ 6.463,75 | Desempenho intermediario, proximo da media semanal. |
| Quarta | R$ 194.347,48 | 6.796 | R$ 6.478,25 | Receita consistente, com ticket acima da media semanal. |
| Quinta | R$ 203.532,46 | 7.215 | R$ 6.565,56 | Melhor dia da semana; deve receber reforco operacional e campanhas de maior margem. |
| Sexta | R$ 194.512,16 | 6.854 | R$ 6.274,59 | Volume abaixo do esperado para fim de semana; merece investigacao por canal e horario. |
| Sabado | R$ 196.266,92 | 7.072 | R$ 6.331,19 | Bom volume, mas ticket medio menor que quarta e sexta. |
| Domingo | R$ 193.190,22 | 6.892 | R$ 6.439,67 | Demanda estavel, adequada para acoes familiares e combos. |

### Promocoes

| Status | Receita | Participacao na receita | Vendas | Ticket medio | Preco unitario medio | Leitura executiva |
|---|---:|---:|---:|---:|---:|---|
| Sem Promocao | R$ 745.724,31 | 54,6% | 24.214 | R$ 30,80 | R$ 10,01 | Vendas sem desconto sustentam a maior parte da receita e maior valor por pedido. |
| Com Promocao | R$ 620.381,03 | 45,4% | 24.277 | R$ 25,55 | R$ 8,27 | Promocao aumenta ligeiramente o numero de vendas, mas captura menos receita. |

Leitura executiva: a promocao gera 63 vendas a mais que o grupo sem promocao, mas R$ 125,3 mil a menos em receita. Isso indica que, no desenho atual, desconto parece atuar mais como reducao de preco do que como alavanca clara de volume. A recomendacao e testar promocoes condicionadas a maior quantidade, combos de maior margem ou beneficios por recorrencia, evitando descontos amplos sem contrapartida.

## KPIs De Cliente

### Visao Consolidada

| KPI | Formula utilizada | Resultado observado | Significado | Importancia para o negocio | Possivel uso executivo | Possiveis insights gerados |
|---|---|---:|---|---|---|---|
| Frequencia de compra | `COUNT(id_transacao) / COUNTD(id_cliente)` | 5,4 compras por cliente | Media de transacoes realizadas por cliente no periodo. | Mede intensidade de relacionamento e potencial de receita recorrente. | Criar metas de recompra, segmentar clientes frequentes e calibrar CRM. | A base apresenta alta frequencia, sugerindo que estrategias de fidelidade podem ter retorno relevante. |
| Recorrencia | `% de clientes com mais de 1 transacao` | 97,6% dos clientes | Mede proporcao de clientes que voltaram a comprar. | Indica fidelidade, aceitacao do produto e dependencia menor de aquisicao de novos clientes. | Criar programa de fidelidade, beneficios progressivos e campanhas de reativacao. | A recorrencia e muito alta; o desafio passa a ser aumentar valor por cliente, nao apenas trazer clientes de volta. |
| Comportamento de compra | `Distribuicao de quantidade_vendida` e `receita_transacao` | 61,8% das vendas tem 3 a 5 unidades | Descreve o padrao de tamanho do pedido. | Ajuda a montar combos, embalagens, ofertas e metas de upsell. | Criar combos para 3, 4 e 5 itens, com incentivo para migrar pedidos pequenos para faixas maiores. | Pedidos de 4 e 5 unidades geram juntos R$ 810,9 mil, quase 59,4% da receita. |
| Preferencias de produtos | `COUNTD(id_cliente)` e `SUM(receita_transacao)` por produto | 72,4% dos clientes compraram Milkshake | Mostra quais produtos tem maior alcance e atratividade. | Define prioridade de portfolio e comunicacao. | Dar destaque a Milkshake no cardapio e usar categorias complementares como cross-sell. | Milkshake combina maior penetracao de clientes com maior receita; e categoria ancora para retencao e ticket. |
| Padroes de consumo | `nunique(canal_venda)` e `nunique(tipo_sorvete)` por cliente | 92,9% usam 2 ou mais canais; 77,9% compram 3 ou mais categorias | Mede diversidade de relacionamento e consumo. | Indica se o cliente se comporta de forma omnicanal e multiproduto. | Unificar CRM por canal, criar ofertas personalizadas e evitar campanhas isoladas por canal. | A maioria dos clientes transita entre canais e categorias; a estrategia deve ser integrada. |
| Canais mais utilizados pelos clientes | `COUNT(id_transacao)` e `COUNTD(id_cliente)` por canal | Parceiro: 16.263 vendas; App: 16.115; Loja: 16.113 | Identifica onde os clientes compram. | Ajuda a priorizar investimentos de atendimento, tecnologia e parcerias. | Otimizar app, negociar parceiros e manter padrao de experiencia na loja. | Como os canais sao equilibrados, pequenas melhorias de conversao ou ticket em qualquer canal podem gerar impacto relevante. |

### Recorrencia E Frequencia

| Indicador | Resultado | Interpretacao executiva |
|---|---:|---|
| Clientes unicos | 8.970 | Base suficiente para segmentacao comercial e analise de comportamento. |
| Media de transacoes por cliente | 5,4 | Cliente medio compra varias vezes dentro do periodo analisado. |
| Mediana de transacoes por cliente | 5 | Recorrencia nao depende apenas de poucos clientes extremos. |
| Clientes com compra unica | 2,4% | Baixo percentual de clientes pontuais. |
| Clientes recorrentes | 97,6% | Forte sinal de aceitacao e habito de compra. |
| Intervalo mediano entre compras | 20 dias | Boa janela para campanhas de reativacao entre 15 e 25 dias apos a ultima compra. |
| Top 20% clientes por receita | 34,9% da receita | Concentracao moderada; ha clientes valiosos, mas a receita nao esta excessivamente dependente deles. |

### Comportamento Por Quantidade Comprada

| Quantidade por venda | Vendas | Receita | Participacao nas vendas | Leitura executiva |
|---:|---:|---:|---:|---|
| 1 unidade | 9.079 | R$ 82.708,76 | 18,7% | Publico de compra pequena; alvo para adicionais simples. |
| 2 unidades | 9.200 | R$ 167.619,56 | 19,0% | Faixa natural para oferta "leve 3" ou combo casal/familia. |
| 3 unidades | 9.915 | R$ 272.077,66 | 20,4% | Uma das faixas centrais de consumo. |
| 4 unidades | 9.908 | R$ 362.704,36 | 20,4% | Alta relevancia financeira; bom alvo para combos de maior margem. |
| 5 unidades | 9.790 | R$ 448.169,17 | 20,2% | Maior bloco de receita; indica compras familiares ou de grupo. |
| 6 unidades | 599 | R$ 32.825,83 | 1,2% | Nicho pequeno, possivel oportunidade para kits maiores. |

## Padroes Importantes Encontrados

1. A receita e bem distribuida por canal. Parceiro, App e Loja Fisica ficam entre 33,1% e 33,6% da receita, o que reduz risco de dependencia, mas exige gestao omnicanal consistente.

2. Milkshake e a categoria lider. Com R$ 353,9 mil em receita e 25,9% de participacao, e tambem a categoria com maior alcance de clientes. A empresa deve trata-la como categoria estrategica, nao apenas como mais um item do cardapio.

3. O negocio tem forte comportamento recorrente. A mediana de 5 compras por cliente e o intervalo mediano de 20 dias sugerem um ciclo de recompra previsivel, util para CRM e campanhas de fidelizacao.

4. A tarde concentra o maior volume absoluto, mas a noite apresenta maior produtividade por slot ativo e maior ticket. Isso indica que estrategias de upsell podem funcionar especialmente bem no periodo noturno.

5. Promocoes nao estao gerando ganho proporcional de volume. O numero de vendas promocionais e quase igual ao de vendas sem promocao, mas o ticket promocional e 17,0% menor.

6. Agosto apresenta ruptura de performance. A queda de 30,7% contra julho e muito superior as oscilacoes observadas entre marco e julho, sugerindo necessidade de investigacao especifica.

## Possiveis Gargalos

| Gargalo | Evidencia nos dados | Impacto potencial | Acao recomendada |
|---|---|---|---|
| Queda de agosto | Receita diaria caiu de R$ 7.502,97 em julho para R$ 5.198,92 em agosto | Perda de tracao comercial e possivel subutilizacao operacional | Auditar campanhas, estoque, funcionamento dos canais, calendario local e possiveis falhas de captura de dados. |
| Promocoes com baixa eficiencia | Promocao tem 50,1% das vendas, mas apenas 45,4% da receita | Desconto pode estar reduzindo margem e receita por pedido | Trocar desconto direto por combos, beneficios progressivos e ofertas condicionadas a quantidade minima. |
| Dependencia estrategica do Milkshake | Milkshake gera 25,9% da receita e lidera o ranking de produtos | Ruptura de insumo ou queda de demanda nessa categoria afetaria fortemente o faturamento | Garantir estoque, qualidade e comunicacao da categoria; testar extensoes de sabores e combos. |
| Segunda-feira mais fraca | Segunda tem menor receita total, R$ 190,3 mil | Capacidade comercial menos explorada no inicio da semana | Criar campanhas de segunda com foco em recompra, sem reduzir excessivamente o ticket. |
| Dados parciais em fevereiro e setembro | Periodo com inicio em 20/02 e fim em 20/09 | Risco de conclusoes incorretas sobre sazonalidade | Usar media diaria e marcar meses parciais nos dashboards. |

## Decisoes Estrategicas Baseadas Nos Dados

1. Revisar a politica promocional. O desenho atual reduz ticket sem demonstrar incremento relevante de vendas. A recomendacao e priorizar promocoes de aumento de cesta, como combos de 4 ou 5 unidades, beneficios por recorrencia e ofertas com produtos complementares.

2. Transformar Milkshake em categoria ancora. Como e o maior gerador de receita e o produto de maior penetracao entre clientes, deve receber destaque no app, materiais de loja, campanhas com parceiros e testes de novos sabores.

3. Investigar imediatamente a queda de agosto. A diferenca de patamar e grande demais para ser tratada como variacao normal. A analise deve cruzar agosto por canal, produto, promocao, cidade e disponibilidade operacional.

4. Criar estrategia de CRM baseada no ciclo de recompra. Com intervalo mediano de 20 dias entre compras, campanhas entre o 15o e o 25o dia apos a ultima transacao podem aumentar frequencia sem depender de desconto generalizado.

5. Otimizar operacao por horario. A tarde deve ser tratada como janela de volume e a noite como janela de valor. Isso permite diferenciar escala, estoque e tipo de oferta por faixa horaria.

6. Fortalecer gestao omnicanal. Como 92,9% dos clientes usam dois ou mais canais, campanhas isoladas por canal podem perder contexto. A empresa deve acompanhar cliente, historico e preferencias de forma integrada.

7. Proteger receita de pedidos de 4 e 5 unidades. Essas faixas somam R$ 810,9 mil, quase 59,4% da receita. Combos familiares e kits de maior valor devem ser tratados como alavanca central de crescimento.

## Recomendacoes Para Dashboard Executivo

| Area | Visual recomendado | Objetivo |
|---|---|---|
| Visao geral | Cards de Receita Total, Ticket Medio, Vendas, Unidades e Clientes | Dar leitura rapida da saude do negocio. |
| Crescimento | Linha mensal com destaque para meses parciais | Separar tendencia real de distorcao de periodo incompleto. |
| Canais | Barras de receita, vendas e ticket por canal | Comparar escala e valor capturado por canal. |
| Produto | Ranking de categorias e sabores por receita | Identificar produtos ancora e oportunidades de sortimento. |
| Operacao | Heatmap de dia da semana por faixa horaria | Apoiar escala, estoque e campanhas por janela de demanda. |
| Promocoes | Comparativo com/sem promocao por ticket, volume e receita | Avaliar eficiencia de desconto. |
| Cliente | Frequencia, recorrencia, intervalo entre compras e canais usados | Direcionar CRM e fidelizacao. |

## Conclusao Executiva

A sorveteria tem uma base comercial saudavel, com receita relevante, canais equilibrados, alta recorrencia e uma categoria lider clara. O potencial de crescimento parece menos dependente de aquisicao de novos clientes e mais associado a tres frentes: elevar ticket medio, melhorar eficiencia promocional e explorar melhor o ciclo de recompra.

O principal risco identificado e a queda abrupta de agosto, que precisa ser investigada antes de qualquer conclusao definitiva sobre sazonalidade. O principal ganho rapido esta na revisao das promocoes: os dados indicam que a empresa esta concedendo desconto em volume alto de vendas sem capturar aumento proporcional de demanda. Uma estrategia mais executiva seria migrar de desconto amplo para ofertas condicionadas a cesta maior, recorrencia e produtos de maior valor.
