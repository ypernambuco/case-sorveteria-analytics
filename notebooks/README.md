# Notebooks

Pasta com os notebooks finais usados na exploração, tratamento e preparação dos dados do Case Sorveteria Analytics.

## Sequencia Final

1. `01_exploracao_inicial.ipynb`: EDA da base bruta, com leitura inicial, estrutura, tipos, nulos, duplicidades e principais pontos de qualidade.
2. `02_tratamento_dados.ipynb`: tratamento, validação, auditoria e preparação da base final para análises e Power BI.

## Boas Praticas

- Ler dados brutos apenas de `data/raw`.
- Salvar dados gerados em `data/interim` ou `data/processed`.
- Documentar regras de tratamento antes de consolidar a base final.
- Evitar regras de negócio escondidas em notebooks; quando amadurecerem, mover para `scripts`.
