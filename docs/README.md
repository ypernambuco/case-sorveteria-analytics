# Documentação

Pasta para briefing, premissas, regras de negócio, dicionário de dados e materiais de referência.

Os materiais da apresentação executiva foram centralizados em `presentation/`.

## Arquivos

- `case_sorveteria.pptx`: documento de referência do case.
- `PROJECT_BRIEF.md`: contexto e escopo inicial do projeto.
- `dicionario_dados_inicial.md`: dicionário preliminar criado a partir da exploração inicial.
- `dicionario_dados_processado.md`: dicionário da base final tratada para Power BI e KPIs.
- `dashboard_powerbi.md`: registro do dashboard Power BI final, incluindo páginas, visuais, métricas, layout, cores, ajustes manuais feitos no Power BI e limitação identificada na base após 22/08/2025.
- `regras_tratamento.md`: regras aplicadas na limpeza, validação e preparação da base analítica.
- `revisao_nomenclatura_colunas.md`: análise crítica dos nomes das colunas da base processada para Power BI e DAX.

## Exportação em PDF

A apresentação `presentation/apresentacao_case_sorveteria.md` já está preparada para exportação via Marp, com front matter habilitado e slides separados por `---`.

Para gerar a versão em PDF localmente, use:

```powershell
npx @marp-team/marp-cli presentation/apresentacao_case_sorveteria.md --pdf -o presentation/apresentacao_case_sorveteria.pdf
```
