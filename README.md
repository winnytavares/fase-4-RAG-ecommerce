# Fase 4 - RAG E-commerce (Voice of Customer / VOC)

Projeto de RAG (Retrieval-Augmented Generation) aplicado a e-commerce para análise de Voice of Customer (VOC), recomendações e suporte.


---

##  Estrutura de Pastas

```text
.
├── README.md           # Visão geral e documentação principal do projeto
├── requirements.txt    # Dependências do projeto Python
├── .env.example        # Exemplo de configuração de variáveis de ambiente
├── .gitignore          # Arquivos e diretórios ignorados pelo Git
├── data/               # Diretório de dados (instruções de download, sem datasets brutos)
├── notebooks/          # Exploração de dados (EDA) e experimentos rápidos
├── src/                # Código-fonte principal da aplicação
│   ├── ingestion/      # Limpeza, preparação e criação de documentos
│   ├── indexing/       # Geração de embeddings e banco vetorial
│   ├── retrieval/      # Busca semântica, filtros e reranking
│   ├── generation/     # Prompt engineering, chamadas ao LLM e guardrails
│   └── app/            # Interface da aplicação (CLI, Streamlit ou Gradio)
└── docs/               # Diagramas de arquitetura e exemplos de Q&A
```

---

##  Como Iniciar:

### 1. Clonar o repositório
```bash
git clone https://github.com/winnytavares/fase-4-RAG-ecommerce.git
cd fase-4-RAG-ecommerce
```

### 2. Configurar o ambiente virtual
```bash
python -m venv venv
# Linux / macOS
source venv/bin/activate
# Windows
.\venv\Scripts\activate
```

### 3. Instalar dependências
```bash
pip install -r requirements.txt
```

### 4. Configurar variáveis de ambiente
Copie o arquivo `.env.example` para `.env` e preencha as chaves de API:
```bash
cp .env.example .env
```
