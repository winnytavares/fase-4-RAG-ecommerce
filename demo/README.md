# 🌐 Interface Web Interativa — Agente VoC RAG

Esta pasta disponibiliza a aplicação web interativa completa ([`voc_agent_ui.html`](./voc_agent_ui.html)) para teste imediato da solução **Voice of Customer (VoC) Intelligence com RAG**, já alimentada com **1.200 avaliações reais** exportadas do Databricks Delta Lake (`workspace.default.reviews_rag`).

---

## ▶️ Como Acessar e Rodar em 1 Clique (Online no Navegador)

Não é necessário instalar Python nem clonar o repositório para testar a interface. Clique diretamente no link abaixo para abrir a aplicação funcionando ao vivo:

👉 **[Abrir Interface Web VoC RAG no Navegador (Execução Imediata)](https://raw.githack.com/winnytavares/fase-4-RAG-ecommerce/main/demo/voc_agent_ui.html)**

*(Link alternativo via GitHub HTML Preview: [Abrir via htmlpreview.github.io](https://htmlpreview.github.io/?https://github.com/winnytavares/fase-4-RAG-ecommerce/blob/main/demo/voc_agent_ui.html))*

---

## 💻 Como Rodar Localmente no Computador

1. Baixe o arquivo [`voc_agent_ui.html`](./voc_agent_ui.html) (botão *Download raw file* no canto superior direito do arquivo no GitHub).
2. Dê um duplo clique no arquivo salvo para abri-lo diretamente no Google Chrome, Edge ou Firefox.
3. *(Opcional)* Com Python instalado, execute na raiz do projeto:
   ```bash
   python src/app/run_app.py
   ```

---

## 🧪 Funcionalidades Disponíveis na Tela

- **Filtros de Metadados:** Slider de **Top-K (1 a 6 documentos)**, **Filtro por Categoria** (57 categorias reais da Olist) e **Filtro por Nota (Score ≤ 2 ou Score ≥ 4)**.
- **Cenários de Teste Rápidos:**
  - *Principais Problemas (Notas Baixas)*
  - *Defeito e Falsificação*
  - *Elogios & Fidelização*
- **Guarda-Corpo Anti-Alucinação (`🛡️ Cuidado com alucinações`):**
  - Botões dedicados *Teste de Recusa 1: Napoleão Bonaparte* e *Teste de Recusa 2: Receita de Bolo* demonstrando bloqueio imediato para perguntas fora do escopo ou com $\cos(\theta) < 0.30$.
- **Aba "Tabela Delta (1.200 Reviews)":** Explorador interativo com busca em tempo real e paginação das 1.200 avaliações reais.
