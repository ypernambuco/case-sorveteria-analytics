# Notebooks

Pasta com os notebooks finais usados na exploracao, tratamento e preparacao dos dados do Case Sorveteria Analytics.

## Sequencia Final

1. `01_exploracao_inicial.ipynb`: EDA da base bruta, com leitura inicial, estrutura, tipos, nulos, duplicidades e principais pontos de qualidade.
2. `02_tratamento_dados.ipynb`: tratamento, validacao, auditoria e preparacao da base final para analises e Power BI.

## Boas Praticas

- Ler dados brutos apenas de `data/raw`.
- Salvar dados gerados em `data/interim` ou `data/processed`.
- Documentar regras de tratamento antes de consolidar a base final.
- Evitar regras de negocio escondidas em notebooks; quando amadurecerem, mover para `scripts`.
