# 📓 Notebooks de Desenvolvimento & Pipeline Databricks

Este diretório contém o notebook oficial do projeto **Voice of Customer Intelligence com RAG**, desenvolvido e validado no ambiente **Databricks**:

---

## 📄 Arquivos

- **[`voice_of_customer.ipynb`](./voice_of_customer.ipynb)**:
  Notebook ponta a ponta contendo todo o ciclo de vida da solução:
  1. **Seção 1: Configuração do Ambiente e Instalação de Dependências** (`sentence-transformers`, `google-genai`, `delta-spark`, `mlflow`).
  2. **Seção 2: Carga e Análise Exploratória dos Dados Brutos da Olist** (Diagnóstico das 99.224 avaliações e eliminação de 57,28% de avaliações sem comentário).
  3. **Seção 3: Enriquecimento Relacional com Metadados (Desafio Adicional)** (Cálculo de `dias_atraso`, flag `atrasou`, tradução e agregação de categorias, consolidação com pedidos, pagamentos e clientes).
  4. **Seção 4: Vetorização (Embeddings) e Persistência no Delta Lake** (Embeddings densos de 384 dimensões via `paraphrase-multilingual-MiniLM-L12-v2` e gravação na tabela `workspace.default.reviews_rag`).
  5. **Seção 5: Mecanismo de Busca Semântica e Filtros de Metadados** (Retriever por similaridade de cosseno com filtros de nota, atraso e categoria).
  6. **Seção 6: Engenharia de Prompt e Integração com LLMs** (Prompt com strictly grounding e citações indexadas `[1]`, `[2]`, com integração ao Google Gemini e Databricks Foundation Models).
  7. **Seção 7: Demonstração Prática e Casos de Teste do Edital** (Execução dos cenários: problemas em notas baixas, defeito/falsificação em informática, elogios/fidelização, e teste de recusa/anti-alucinação com limiar $\cos(\theta) \ge 0.30$).

---

## 🚀 Como Executar no Databricks

1. Importe o arquivo `notebooks/voice_of_customer.ipynb` para o seu workspace no Databricks.
2. Certifique-se de que os dados da Olist estejam em `/Volumes/workspace/default/fase4-ecommerce`.
3. Configure a sua chave da API Gemini nos segredos do Databricks (`dbutils.secrets`) ou via variável de ambiente `GEMINI_API_KEY`.
4. Clique em **Run All** para executar todo o pipeline. A tabela Delta Lake será gravada em `workspace.default.reviews_rag`.
