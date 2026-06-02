# Roteiro Da Apresentação - Case Sorveteria Analytics

Este roteiro organiza a apresentação do case como uma história de negócio, conectando contexto, qualidade dos dados, modelagem, dashboards, descobertas e recomendações. O objetivo e orientar a narrativa antes da criação de slides, sem substituir a documentação técnica existente.

## 1. Contexto do negócio

**Objetivo do slide:** apresentar o desafio da sorveteria e situar o case como uma jornada completa de analytics aplicada a vendas.

**Mensagem principal:** a sorveteria precisava transformar uma base transacional em informação gerencial para apoiar decisões sobre receita, produtos, canais, horários e comportamento de clientes.

**Evidencias que sustentam a mensagem:**

- O projeto trabalha uma base de vendas de sorvetes com foco em 2025.
- A pergunta de negócio documentada e: como aumentar receita considerando produtos, sazonalidade, canais, regiões, mix de vendas e oportunidades operacionais.
- O escopo inclui EDA, tratamento, KPIs, modelagem dimensional, dashboard Power BI e apresentação do case.

## 2. Objetivo da análise

**Objetivo do slide:** mostrar o que a análise precisava responder e quais decisões deveriam ser apoiadas pelos dados.

**Mensagem principal:** a análise buscou criar uma base confiável e indicadores executivos para entender desempenho comercial, eficiência operacional e oportunidades de crescimento.

**Evidencias que sustentam a mensagem:**

- O README define como objetivo organizar a base para entendimento do problema, validação, KPIs, modelagem, dashboards e documentação das limitações.
- Os KPIs documentados incluem receita total, total de vendas, ticket médio, clientes únicos e volume vendido.
- As análises também cobrem canal de venda, tipo de sorvete, dia da semana, faixa horária, trimestre e evolução temporal.

## 3. Dataset utilizado

**Objetivo do slide:** apresentar a origem, o tamanho e a granularidade da base analisada.

**Mensagem principal:** o projeto partiu de uma base bruta de 50.000 registros e chegou a uma base analítica tratada com 48.491 vendas válidas.

**Evidencias que sustentam a mensagem:**

- Fonte bruta: `data/raw/vendas_sorvetes.csv`.
- Período da base: 20/02/2025 a 20/09/2025.
- Granularidade: uma linha por transação de venda.
- Base tratada: `data/processed/vendas_sorvetes_tratado.csv`, com 48.491 registros válidos e 31 colunas.

## 4. Problemas encontrados nos dados

**Objetivo do slide:** explicar por que a etapa de qualidade era necessaria antes de construir indicadores ou dashboard.

**Mensagem principal:** a base original tinha problemas que poderiam distorcer receita, volume, ticket médio, filtros e leitura operacional se fossem consumidos diretamente.

**Evidencias que sustentam a mensagem:**

- Foram encontrados nulos em campos como `sabor`, `cidade` e `Valor_Total`.
- Havia registros com quantidade vendida não positiva e valores monetarios não positivos.
- Existiam inconsistencias textuais, espacos extras e nomes de colunas pouco adequados para Power BI e DAX.
- Outliers financeiros foram identificados e mantidos com flag, sem exclusao automatica.

## 5. Processo de limpeza e tratamento

**Objetivo do slide:** mostrar a abordagem de tratamento sem entrar em excesso técnico.

**Mensagem principal:** o tratamento preservou a fonte original, separou camadas de auditoria e criou uma base final limpa, rastreavel e pronta para consumo analítico.

**Evidencias que sustentam a mensagem:**

- A arquitetura documentada segue o fluxo `Raw -> Interim -> Processed -> Power BI`.
- Arquivos em `data/raw` foram preservados como fonte imutável.
- Registros removidos permaneceram auditaveis em `data/interim/vendas_sorvetes_registros_excluidos.csv`.
- Nulos em `sabor` e `cidade` foram preenchidos como `Nao Informado` com flags de rastreabilidade.
- Valores monetarios e quantidades não positivas foram removidos da base processada e preservados na auditoria.

## 6. Qualidade dos dados após tratamento

**Objetivo do slide:** demonstrar que a base final tem confiabilidade suficiente para análise executiva.

**Mensagem principal:** após o tratamento, a base processada ficou consistente, sem nulos finais, sem duplicidade de transação e com alto indice de validade para Power BI.

**Evidencias que sustentam a mensagem:**

- 48.491 registros válidos mantidos de 50.000 registros originais.
- 1.509 registros removidos, equivalentes a 3,02% da base bruta.
- Taxa de aproveitamento: 96,98%.
- Nulos finais: 0.
- Duplicidade em `id_transacao`: 0.
- Registros finais com `quantidade_vendida <= 0`: 0.
- Registros finais com `receita_transacao <= 0`: 0.
- Data Quality Score documentado: 99,25.

## 7. Modelagem dimensional

**Objetivo do slide:** explicar como a base foi organizada para facilitar análises no Power BI.

**Mensagem principal:** a modelagem em estrela separou fatos e dimensões, reduzindo ambiguidade e tornando o modelo mais claro para filtros, medidas e dashboards.

**Evidencias que sustentam a mensagem:**

- Camada derivada criada em `data/powerbi/`.
- Tabela fato: `fato_vendas.csv`, com 48.491 linhas.
- Dimensões: `dim_tempo.csv`, `dim_produtos.csv`, `dim_clientes.csv` e `dim_canais.csv`.
- Relacionamentos recomendados: dimensões em relacao um-para-muitos com `fato_vendas`.
- Direcao de filtro recomendada: simples, evitando muitos-para-muitos e filtros bidirecionais.

## 8. Construção dos dashboards

**Objetivo do slide:** apresentar como os dashboards foram estruturados para responder a publicos e perguntas diferentes.

**Mensagem principal:** o Power BI foi organizado em duas visoes complementares: uma executiva para leitura rápida do negócio e outra operacional para rotina de demanda, volume, horários e sazonalidade.

**Evidencias que sustentam a mensagem:**

- O dashboard final possui duas páginas: `Visao Executiva` e `Visao Operacional`.
- A visão executiva usa filtros superiores, KPIs principais, evolução da receita e gráficos de apoio por canal, tipo de sorvete e dia da semana.
- A visão operacional inclui vendas por faixa horária, receita por faixa horária, receita por trimestre, volume por tipo de sorvete, receita por dia da semana e evolução do volume vendido.
- O layout prioriza leitura rápida, separacao clara entre páginas e titulos orientados a negócio.

## 9. Principais descobertas

**Objetivo do slide:** consolidar os achados mais importantes para a tomada de decisão.

**Mensagem principal:** a sorveteria apresenta base comercial relevante, canais equilibrados, alta recorrência e uma categoria âncora clara, mas também pontos de atenção em promoções e leitura temporal.

**Evidencias que sustentam a mensagem:**

- Receita total: R$ 1.366.105,34.
- Vendas válidas: 48.491.
- Unidades vendidas: 149.400.
- Ticket médio: R$ 28,17.
- Clientes únicos: 8.970.
- Canais equilibrados: Parceiro, App e Loja Física ficam cada um em torno de um terço da receita.
- Milkshake representa 25,9% da receita e lidera também no ranking de produtos.
- Clientes recorrentes representam 97,6% da base analisada.
- Tarde concentra 39,9% das vendas; noite apresenta maior produtividade por slot ativo.
- Promocoes representam 50,1% das vendas, mas apenas 45,4% da receita.

## 10. Investigação da anomalia pos-22/08/2025

**Objetivo do slide:** explicar a queda abrupta identificada e a decisão analítica adotada.

**Mensagem principal:** a queda de registros após 22/08/2025 não foi causada pelo tratamento, modelagem ou dashboard; ela já existia na fonte original e deve ser tratada como limitação dos dados.

**Evidencias que sustentam a mensagem:**

- A investigação comparou `data/processed/vendas_sorvetes_tratado.csv` com `data/raw/vendas_sorvetes.csv`.
- Antes de 22/08/2025, a base tinha aproximadamente 250 registros por dia.
- No dataset bruto, houve 251 registros em 21/08/2025 e 26 registros em 22/08/2025.
- No dataset tratado, houve 243 registros em 21/08/2025 e 25 registros em 22/08/2025.
- Nenhum valor foi corrigido, estimado ou imputado artificialmente.
- Indicadores temporais após essa data devem ser interpretados com cautela.

## 11. Recomendacoes de negócio

**Objetivo do slide:** traduzir os achados em ações práticas para crescimento e gestão.

**Mensagem principal:** as oportunidades mais claras estão em aumentar ticket, revisar promoções, proteger a categoria Milkshake, explorar CRM e ajustar operação por horário.

**Evidencias que sustentam a mensagem:**

- Revisar política promocional: vendas com promoção geram ticket médio de R$ 25,55, contra R$ 30,80 sem promoção.
- Trocar desconto amplo por combos, benefícios progressivos e ofertas condicionadas a quantidade minima.
- Tratar Milkshake como categoria âncora, pois responde por 25,9% da receita e lidera o ranking de produtos.
- Explorar o ciclo de recompra: intervalo mediano entre compras de 20 dias.
- Criar campanhas de CRM entre o 15o e o 25o dia após a ultima compra.
- Diferenciar operação por horário: tarde como janela de volume e noite como janela de valor.
- Fortalecer gestão omnicanal, considerando que os canais apresentam participação equilibrada.

## 12. Conclusão

**Objetivo do slide:** fechar a narrativa reforçando o valor do projeto e a qualidade da decisão analítica.

**Mensagem principal:** o projeto transformou uma base transacional em um ativo analítico confiável, com governança, modelo dimensional, dashboards e conclusões acionaveis para o negócio.

**Evidencias que sustentam a mensagem:**

- A fonte bruta foi preservada e as transformações ficaram rastreaveis.
- A base final ficou pronta para análises, KPIs e Power BI.
- O modelo dimensional organizou fatos e dimensões para consumo executivo.
- Os dashboards separaram leitura executiva e operacional.
- A anomalia pos-22/08/2025 foi investigada na origem e documentada sem imputação artificial.
- O case entrega uma história completa: problema de negócio, qualidade dos dados, modelagem, visualizacao, achados e recomendações.

## Fontes internas utilizadas

- `README.md`
- `docs/regras_tratamento.md`
- `docs/dicionario_dados_processado.md`
- `docs/revisao_nomenclatura_colunas.md`
- `docs/modelagem_powerbi.md`
- `docs/dashboard_powerbi.md`
- `docs/kpis_executivos.md`
- `CHANGELOG.md`
