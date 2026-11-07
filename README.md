# Notebooks do Projeto

- **`voice_of_customer.ipynb`**: Notebook principal executado no Databricks contendo:
  - Análise Exploratória de Dados (EDA) e gráficos de distribuição;
  - Limpeza e tratamento de valores ausentes (42.389 avaliações textuais mantidas);
  - Enriquecimento relacional com metadados (cálculo de `dias_atraso`, status de atraso e categorias);
  - Geração de embeddings com `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`;
  - Persistência e indexação na Tabela Delta Lake (`workspace.default.reviews_rag`);
  - Mecanismo de busca semântica por cosseno com limiar anti-alucinação (`min_similarity = 0.30`);
  - Geração com Google Gemini 3.8 Flash e Databricks Llama 3.1 70B;
  - Demonstração prática dos 4 cenários de teste do edital e matriz de insights de negócio.
