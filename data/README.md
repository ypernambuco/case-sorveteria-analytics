# Dados

Esta pasta concentra todas as bases utilizadas no projeto, organizadas por camadas de processamento.

## Estrutura

```text
data/
|-- raw/
|-- interim/
`-- processed/
```

## Camadas

### `raw/`

Dados originais recebidos da fonte.
Os arquivos desta camada devem permanecer imutaveis e servir como referência primaria do projeto.

### `interim/`

Dados intermediários gerados durante etapas de limpeza, padronização, enriquecimento, transformação e validação.

### `processed/`

Bases finais consolidadas e preparadas para análises, KPIs, dashboards e consumo no Power BI.

## Regra Principal

Arquivos armazenados em `raw` não devem ser editados diretamente.
Toda transformação deve gerar novos arquivos nas camadas `interim` ou `processed`, garantindo rastreabilidade, reproducibilidade e governança dos dados.
