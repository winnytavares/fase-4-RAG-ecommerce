# 📚 Documentação Técnica do Projeto VoC RAG

Bem-vindo à documentação técnica completa do sistema **Voice of Customer (VoC) Intelligence com RAG**.

---

## 📑 Índice de Documentos

1. **[Arquitetura da Solução RAG](./arquitetura.md)**:
   - Diagrama de fluxo ponta a ponta em Mermaid.
   - Justificativas das decisões técnicas (embeddings, Delta Lake, Guardrail, Gemini).
   - Detalhamento de cada componente.

2. **[Tratamento de Dados e Engenharia de Metadados](./tratamento_dados.md)**:
   - Cronograma exato de quando o tratamento foi realizado.
   - Diagnóstico da volumetria inicial (99.224 ➔ 42.389 reviews com texto).
   - Eliminação de valores ausentes e justificativa do descarte dos 57,28% sem texto.
   - Engenharia de features logísticas (`dias_atraso`, `atrasou`) e tradução de categorias.
   - Estrutura canônica do `documento_rag`.

3. **[Casos de Teste e Avaliação de Evidências](./casos_de_teste_rag.md)**:
   - Cenário 1: Reclamações e notas baixas com citações `[1]`, `[2]`.
   - Cenário 2: Defeito e falsificação com análise de avarias e SAC.
   - Cenário 3: Elogios e fidelização por pontualidade logística.
   - Cenário 4: Teste de recusa e anti-alucinação obrigatório (Napoleão Bonaparte e Receita de Bolo).
