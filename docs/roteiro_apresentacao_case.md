# Roteiro Da Apresentacao - Case Sorveteria Analytics

Este roteiro organiza a apresentacao do case como uma historia de negocio, conectando contexto, qualidade dos dados, modelagem, dashboards, descobertas e recomendacoes. O objetivo e orientar a narrativa antes da criacao de slides, sem substituir a documentacao tecnica existente.

## 1. Contexto do negocio

**Objetivo do slide:** apresentar o desafio da sorveteria e situar o case como uma jornada completa de analytics aplicada a vendas.

**Mensagem principal:** a sorveteria precisava transformar uma base transacional em informacao gerencial para apoiar decisoes sobre receita, produtos, canais, horarios e comportamento de clientes.

**Evidencias que sustentam a mensagem:**

- O projeto trabalha uma base de vendas de sorvetes com foco em 2025.
- A pergunta de negocio documentada e: como aumentar receita considerando produtos, sazonalidade, canais, regioes, mix de vendas e oportunidades operacionais.
- O escopo inclui EDA, tratamento, KPIs, modelagem dimensional, dashboard Power BI e apresentacao do case.

## 2. Objetivo da analise

**Objetivo do slide:** mostrar o que a analise precisava responder e quais decisoes deveriam ser apoiadas pelos dados.

**Mensagem principal:** a analise buscou criar uma base confiavel e indicadores executivos para entender desempenho comercial, eficiencia operacional e oportunidades de crescimento.

**Evidencias que sustentam a mensagem:**

- O README define como objetivo organizar a base para entendimento do problema, validacao, KPIs, modelagem, dashboards e documentacao das limitacoes.
- Os KPIs documentados incluem receita total, total de vendas, ticket medio, clientes unicos e volume vendido.
- As analises tambem cobrem canal de venda, tipo de sorvete, dia da semana, faixa horaria, trimestre e evolucao temporal.

## 3. Dataset utilizado

**Objetivo do slide:** apresentar a origem, o tamanho e a granularidade da base analisada.

**Mensagem principal:** o projeto partiu de uma base bruta de 50.000 registros e chegou a uma base analitica tratada com 48.491 vendas validas.

**Evidencias que sustentam a mensagem:**

- Fonte bruta: `data/raw/vendas_sorvetes.csv`.
- Periodo da base: 20/02/2025 a 20/09/2025.
- Granularidade: uma linha por transacao de venda.
- Base tratada: `data/processed/vendas_sorvetes_tratado.csv`, com 48.491 registros validos e 31 colunas.

## 4. Problemas encontrados nos dados

**Objetivo do slide:** explicar por que a etapa de qualidade era necessaria antes de construir indicadores ou dashboard.

**Mensagem principal:** a base original tinha problemas que poderiam distorcer receita, volume, ticket medio, filtros e leitura operacional se fossem consumidos diretamente.

**Evidencias que sustentam a mensagem:**

- Foram encontrados nulos em campos como `sabor`, `cidade` e `Valor_Total`.
- Havia registros com quantidade vendida nao positiva e valores monetarios nao positivos.
- Existiam inconsistencias textuais, espacos extras e nomes de colunas pouco adequados para Power BI e DAX.
- Outliers financeiros foram identificados e mantidos com flag, sem exclusao automatica.

## 5. Processo de limpeza e tratamento

**Objetivo do slide:** mostrar a abordagem de tratamento sem entrar em excesso tecnico.

**Mensagem principal:** o tratamento preservou a fonte original, separou camadas de auditoria e criou uma base final limpa, rastreavel e pronta para consumo analitico.

**Evidencias que sustentam a mensagem:**

- A arquitetura documentada segue o fluxo `Raw -> Interim -> Processed -> Power BI`.
- Arquivos em `data/raw` foram preservados como fonte imutavel.
- Registros removidos permaneceram auditaveis em `data/interim/vendas_sorvetes_registros_excluidos.csv`.
- Nulos em `sabor` e `cidade` foram preenchidos como `Nao Informado` com flags de rastreabilidade.
- Valores monetarios e quantidades nao positivas foram removidos da base processada e preservados na auditoria.

## 6. Qualidade dos dados apos tratamento

**Objetivo do slide:** demonstrar que a base final tem confiabilidade suficiente para analise executiva.

**Mensagem principal:** apos o tratamento, a base processada ficou consistente, sem nulos finais, sem duplicidade de transacao e com alto indice de validade para Power BI.

**Evidencias que sustentam a mensagem:**

- 48.491 registros validos mantidos de 50.000 registros originais.
- 1.509 registros removidos, equivalentes a 3,02% da base bruta.
- Taxa de aproveitamento: 96,98%.
- Nulos finais: 0.
- Duplicidade em `id_transacao`: 0.
- Registros finais com `quantidade_vendida <= 0`: 0.
- Registros finais com `receita_transacao <= 0`: 0.
- Data Quality Score documentado: 99,25.

## 7. Modelagem dimensional

**Objetivo do slide:** explicar como a base foi organizada para facilitar analises no Power BI.

**Mensagem principal:** a modelagem em estrela separou fatos e dimensoes, reduzindo ambiguidade e tornando o modelo mais claro para filtros, medidas e dashboards.

**Evidencias que sustentam a mensagem:**

- Camada derivada criada em `data/powerbi/`.
- Tabela fato: `fato_vendas.csv`, com 48.491 linhas.
- Dimensoes: `dim_tempo.csv`, `dim_produtos.csv`, `dim_clientes.csv` e `dim_canais.csv`.
- Relacionamentos recomendados: dimensoes em relacao um-para-muitos com `fato_vendas`.
- Direcao de filtro recomendada: simples, evitando muitos-para-muitos e filtros bidirecionais.

## 8. Construcao dos dashboards

**Objetivo do slide:** apresentar como os dashboards foram estruturados para responder a publicos e perguntas diferentes.

**Mensagem principal:** o Power BI foi organizado em duas visoes complementares: uma executiva para leitura rapida do negocio e outra operacional para rotina de demanda, volume, horarios e sazonalidade.

**Evidencias que sustentam a mensagem:**

- O dashboard final possui duas paginas: `Visao Executiva` e `Visao Operacional`.
- A visao executiva usa filtros superiores, KPIs principais, evolucao da receita e graficos de apoio por canal, tipo de sorvete e dia da semana.
- A visao operacional inclui vendas por faixa horaria, receita por faixa horaria, receita por trimestre, volume por tipo de sorvete, receita por dia da semana e evolucao do volume vendido.
- O layout prioriza leitura rapida, separacao clara entre paginas e titulos orientados a negocio.

## 9. Principais descobertas

**Objetivo do slide:** consolidar os achados mais importantes para a tomada de decisao.

**Mensagem principal:** a sorveteria apresenta base comercial relevante, canais equilibrados, alta recorrencia e uma categoria ancora clara, mas tambem pontos de atencao em promocoes e leitura temporal.

**Evidencias que sustentam a mensagem:**

- Receita total: R$ 1.366.105,34.
- Vendas validas: 48.491.
- Unidades vendidas: 149.400.
- Ticket medio: R$ 28,17.
- Clientes unicos: 8.970.
- Canais equilibrados: Parceiro, App e Loja Fisica ficam cada um em torno de um terco da receita.
- Milkshake representa 25,9% da receita e lidera tambem no ranking de produtos.
- Clientes recorrentes representam 97,6% da base analisada.
- Tarde concentra 39,9% das vendas; noite apresenta maior produtividade por slot ativo.
- Promocoes representam 50,1% das vendas, mas apenas 45,4% da receita.

## 10. Investigacao da anomalia pos-22/08/2025

**Objetivo do slide:** explicar a queda abrupta identificada e a decisao analitica adotada.

**Mensagem principal:** a queda de registros apos 22/08/2025 nao foi causada pelo tratamento, modelagem ou dashboard; ela ja existia na fonte original e deve ser tratada como limitacao dos dados.

**Evidencias que sustentam a mensagem:**

- A investigacao comparou `data/processed/vendas_sorvetes_tratado.csv` com `data/raw/vendas_sorvetes.csv`.
- Antes de 22/08/2025, a base tinha aproximadamente 250 registros por dia.
- No dataset bruto, houve 251 registros em 21/08/2025 e 26 registros em 22/08/2025.
- No dataset tratado, houve 243 registros em 21/08/2025 e 25 registros em 22/08/2025.
- Nenhum valor foi corrigido, estimado ou imputado artificialmente.
- Indicadores temporais apos essa data devem ser interpretados com cautela.

## 11. Recomendacoes de negocio

**Objetivo do slide:** traduzir os achados em acoes praticas para crescimento e gestao.

**Mensagem principal:** as oportunidades mais claras estao em aumentar ticket, revisar promocoes, proteger a categoria Milkshake, explorar CRM e ajustar operacao por horario.

**Evidencias que sustentam a mensagem:**

- Revisar politica promocional: vendas com promocao geram ticket medio de R$ 25,55, contra R$ 30,80 sem promocao.
- Trocar desconto amplo por combos, beneficios progressivos e ofertas condicionadas a quantidade minima.
- Tratar Milkshake como categoria ancora, pois responde por 25,9% da receita e lidera o ranking de produtos.
- Explorar o ciclo de recompra: intervalo mediano entre compras de 20 dias.
- Criar campanhas de CRM entre o 15o e o 25o dia apos a ultima compra.
- Diferenciar operacao por horario: tarde como janela de volume e noite como janela de valor.
- Fortalecer gestao omnicanal, considerando que os canais apresentam participacao equilibrada.

## 12. Conclusao

**Objetivo do slide:** fechar a narrativa reforcando o valor do projeto e a qualidade da decisao analitica.

**Mensagem principal:** o projeto transformou uma base transacional em um ativo analitico confiavel, com governanca, modelo dimensional, dashboards e conclusoes acionaveis para o negocio.

**Evidencias que sustentam a mensagem:**

- A fonte bruta foi preservada e as transformacoes ficaram rastreaveis.
- A base final ficou pronta para analises, KPIs e Power BI.
- O modelo dimensional organizou fatos e dimensoes para consumo executivo.
- Os dashboards separaram leitura executiva e operacional.
- A anomalia pos-22/08/2025 foi investigada na origem e documentada sem imputacao artificial.
- O case entrega uma historia completa: problema de negocio, qualidade dos dados, modelagem, visualizacao, achados e recomendacoes.

## Fontes internas utilizadas

- `README.md`
- `docs/regras_tratamento.md`
- `docs/dicionario_dados_processado.md`
- `docs/revisao_nomenclatura_colunas.md`
- `docs/modelagem_powerbi.md`
- `docs/dashboard_powerbi.md`
- `docs/kpis_executivos.md`
- `CHANGELOG.md`
