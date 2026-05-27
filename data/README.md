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
Os arquivos desta camada devem permanecer imutaveis e servir como referencia primaria do projeto.

### `interim/`

Dados intermediarios gerados durante etapas de limpeza, padronizacao, enriquecimento, transformacao e validacao.

### `processed/`

Bases finais consolidadas e preparadas para analises, KPIs, dashboards e consumo no Power BI.

## Regra Principal

Arquivos armazenados em `raw` nao devem ser editados diretamente.
Toda transformacao deve gerar novos arquivos nas camadas `interim` ou `processed`, garantindo rastreabilidade, reproducibilidade e governanca dos dados.
