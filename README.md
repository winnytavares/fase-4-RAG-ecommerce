# Voice of Customer Intelligence com RAG (Olist E-Commerce)
## Tech Challenge - Fase 4 | Inteligência Artificial & Retrieval-Augmented Generation

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Databricks](https://img.shields.io/badge/Platform-Databricks%20Lakehouse-orange.svg)](https://databricks.com/)
[![Delta Lake](https://img.shields.io/badge/Storage-Delta%20Lake-00ADD8.svg)](https://delta.io/)
[![HuggingFace](https://img.shields.io/badge/Embeddings-Sentence--Transformers-yellow.svg)](https://huggingface.co/)
[![Google Gemini](https://img.shields.io/badge/LLM-Gemini%203.8%20Flash-4285F4.svg)](https://ai.google.dev/)
[![Meta Llama](https://img.shields.io/badge/LLM-Llama%203.1%2070B-0467DF.svg)](https://www.databricks.com/)

> **Solução corporativa de Voice of Customer (VoC) para análise e exploração de mais de 40 mil avaliações de e-commerce utilizando Retrieval-Augmented Generation (RAG), embeddings multilíngues, enriquecimento relacional com metadados e prevenção estrita de alucinações.**

---

## 📌 1. Visão Geral e Problema de Negócio

No setor de comércio eletrônico, compreender a experiência do consumidor (**Voice of Customer - VoC**) é um pilar estratégico indispensável para retenção de clientes, redução de cancelamentos e aprimoramento de produtos. 

Empresas recebem diariamente milhares de avaliações. Embora indicadores quantitativos (como notas de 1 a 5 estrelas) acompanhem a média de satisfação, a causa raiz dos gargalos operacionais e os motivos de fidelização encontram-se nos **dados não estruturados** (comentários em texto livre). 

Analisar manualmente dezenas de milhares de avaliações é impraticável, demorado e pouco escalável.

### O Desafio
Desenvolver uma solução inteligente baseada em **Retrieval-Augmented Generation (RAG)** sobre a base de dados pública da **Olist** (composta por aproximadamente 100 mil pedidos entre 2016 e 2018), capaz de:
- Transformar textos não estruturados em uma base de conhecimento semântica consultável;
- Responder a perguntas analíticas em linguagem natural com **fundamentação obrigatória em evidências reais**;
- Permitir **rastreabilidade total** das avaliações que sustentam cada insight;
- **Evitar alucinações**, identificando e rejeitando situações em que não há dados suficientes ou a pergunta foge do escopo do e-commerce.

---

## 🏗️ 2. Arquitetura da Solução

O fluxo da solução foi desenhado com foco em modularidade, velocidade de inferência e governança de dados:

```
┌────────────────────────────────────────────────────────────────────────┐
│                      DADOS BRUTOS (OLIST - 8 TABELAS)                  │
│ Reviews (99k) + Pedidos + Itens + Produtos + Pagamentos + Vendedores   │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                   ENGENHARIA & PREPARAÇÃO DE DADOS                     │
│ • Diagnóstico Exploratório (EDA): 56.835 reviews sem texto descartadas │
│ • 42.389 avaliações com conteúdo textual mantidas e desduplicadas      │
│ • Desafio de Metadados: Cálculo de atraso real (dias_atraso e atrasou) │
│ • Agregação relacional de categorias, valores pagos e UF de clientes   │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                  VETORIZAÇÃO & DELTA LAKE LAKEHOUSE                    │
│ • sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2          │
│ • Vetores densos de 384 dimensões (otimizados para Português pt-BR)    │
│ • Persistência transacional ACID: Tabela Delta 'reviews_rag'           │
│ • Validação de schema e consulta via Spark SQL nativo                  │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│            RETRIEVER HÍBRIDO & LIMIAR ANTI-ALUCINAÇÃO (REQ. 4)         │
│ • Vetorização da pergunta do usuário                                   │
│ • Filtros estruturados de Metadados (Score <= 2, Categoria, Atraso)    │
│ • Similaridade por Cosseno vetorizada com NumPy                        │
│ • Threshold Mínimo de Similaridade (min_similarity >= 0.30):           │
│   ──> Se abaixo do limiar: ABORTA LLM e avisa "Sem evidências na base" │
│   ──> Se acima do limiar: Seleciona os Top-K mais relevantes           │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                ENGENHARIA DE PROMPT & GERAÇÃO MULTI-LLM                │
│ • Diretrizes rígidas de Grounding e Persona Especialista em CX         │
│ • Citação obrigatória de fontes [1], [2] com Nota, UF e Categoria      │
│ • Provedores: Google Gemini 3.8 Flash / Databricks Llama 3.1 70B       │
│ • Resposta executiva, auditável e fundamentada nos dados reais         │
└────────────────────────────────────────────────────────────────────────┘
```

---

## ⚙️ 3. Tecnologias e Bibliotecas

| Camada | Tecnologia | Justificativa Técnica |
| :--- | :--- | :--- |
| **Plataforma de Dados** | Databricks Lakehouse & Unity Catalog | Governança unificada de dados, processamento distribuído e Volumes para armazenamento dos CSVs |
| **Armazenamento de Dados** | Delta Lake (`workspace.default.reviews_rag`) | Suporte transacional ACID, versionamento temporal (*time-travel*) e leitura otimizada |
| **Linguagem & Bibliotecas** | Python 3.10+, PySpark, Pandas, NumPy | Limpeza, enriquecimento relacional e operações matriciais de similaridade por cosseno |
| **Análise Exploratória (EDA)** | Matplotlib & Seaborn | Visualização gráfica de distribuição de notas, volumetria e correlações de negócio |
| **Modelo de Embeddings** | `paraphrase-multilingual-MiniLM-L12-v2` | Suporte robusto a mais de 50 idiomas incluindo português coloquial, 384 dimensões e alta velocidade |
| **Framework de Embeddings**| `sentence-transformers` | Vetorização semântica em lote (*batch encoding*) com aceleração por GPU/CPU |
| **Modelo Generativo Principal** | Google Gemini (`gemini-3.8-flash`) | Alta janela de contexto, rapidez de resposta e excelente capacidade de seguir instruções de *grounding* |
| **Modelo Generativo Alternativo**| Databricks Meta Llama 3.1 70B | Suporte corporativo local via Databricks Foundation Model API / MLflow Deployments |

---

## 🔬 4. Decisões Técnicas e Metodológicas

### 4.1. Seleção dos Dados e Tratamento de Nulos
- **Diagnóstico:** A tabela `olist_order_reviews_dataset` continha 99.224 registros brutos.
- **Identificação de Nulos:** **56.835 clientes não escreveram texto**, informando apenas a nota numérica (1 a 5 estrelas).
- **Decisão:** Manter apenas as **42.389 avaliações com conteúdo textual real** (mensagem ou título preenchido) e deduplicar registros por `review_id`. Isso garante que a base de conhecimento RAG seja alimentada exclusivamente por linguagem natural rica.

### 4.2. Desafio Adicional: Metadados e Exploração Contextual
A solução enriqueceu a base com o cruzamento relacional de 8 tabelas do ecossistema Olist:
1. **Cálculo de Atraso de Entrega:** Diferença em dias entre `order_delivered_customer_date` e `order_estimated_delivery_date`. Criou-se a variável booleana `atrasou` e o número inteiro de `dias_atraso`.
2. **Prova de Conceito de Negócio:** Foi comprovado estatisticamente no notebook que **a entrega atrasada derruba a nota média de avaliação de 4.16 para 1.70**, justificando o uso do filtro de atraso para análises de churn.
3. **Categorias e Localização:** Inclusão da categoria do produto traduzida e do estado (UF) do cliente e vendedor.
4. **Formatação do Documento RAG:**
   ```text
   Nota: 1/5 | Categoria: utilidades_domesticas | Entrega: Atrasada 4 dias | Cliente: SP | Título: Atraso recorrente | Comentário: Não é a primeira vez de atraso na entrega, atendente pede prazo extra...
   ```

### 4.3. Escolha do Modelo de Embedding
O modelo `paraphrase-multilingual-MiniLM-L12-v2` foi selecionado porque:
- Foi treinado especificamente para tarefas de paráfrase e busca semântica em mais de 50 idiomas;
- Capta termos sinônimos frequentes no e-commerce brasileiro (ex: *"atrasou"*, *"demora na entrega"*, *"ainda não recebi"*, *"extraviou"*);
- Gera vetores compactos de 384 dimensões, permitindo buscas vetoriais instantâneas em memória sem necessidade de infraestrutura cara de servidores dedicados.

### 4.4. Prevenção de Alucinação e Tratamento de Perguntas sem Evidências (Requisito 4)
Modelos generativos comerciais tendem a alucinar quando perguntados sobre assuntos fora de seu contexto. Para atender rigorosamente ao **Requisito 4 do Edital**:
1. **Threshold Mínimo de Similaridade (`min_similarity = 0.30`):** Se a pergunta tiver similaridade matemática inferior ao limiar com todos os documentos da base (ex: *"Como fazer bolo de cenoura?"*), o sistema **nem chama o modelo generativo**;
2. **Mensagem Clara e Transparente:** O sistema responde imediatamente:
   > *"NÃO FORAM ENCONTRADAS EVIDÊNCIAS SUFICIENTES NA BASE DE AVALIAÇÕES. Motivo: O assunto pesquisado não possui relevância semântica suficiente com os comentários da base ou está fora do escopo de e-commerce da Olist."*
3. **Grounding Rigoroso:** O prompt instrui o modelo a responder exclusivamente com base nas avaliações recuperadas, exigindo citação formal `[1]`, `[2]`.

---

## 📊 5. Demonstração Prática e Casos de Teste do Edital

O notebook executa a validação prática dos 4 cenários estratégicos exigidos pelo desafio:

| Cenário | Pergunta Realizada | Filtro de Metadados | Comportamento do RAG |
| :--- | :--- | :--- | :--- |
| **1. Logística & Atrasos** | *"Quais são as principais reclamações dos clientes sobre atraso na entrega?"* | `nota_maxima=2`, `apenas_atrasados=True` | Recupera 4 avaliações reais de clientes de SP e CE com atrasos de 4 a 33 dias. A LLM cita que a causa raiz é o rastreamento desatualizado e promessas de prazo não cumpridas pelo SAC [1][2][3]. |
| **2. Qualidade por Nicho** | *"O que os clientes relatam sobre defeito, itens falsificados ou qualidade dos produtos?"* | `categoria="informatica"` | Recupera relatos de embalagens violadas não originais [1], produtos que não ligam no primeiro uso [2] e periféricos com suspeita de falsificação [3]. |
| **3. Satisfação & Elogios** | *"Quais aspectos da experiência de compra são mais elogiados pelos clientes satisfeitos?"* | Sem filtro restritivo (`top_k=4`) | Recupera avaliações 5/5 evidenciando entregas antes do prazo e excelente embalagem de proteção [1][2][3]. |
| **4. Anti-Alucinação (Requisito 4)** | *"Como preparar uma receita tradicional de bolo de cenoura com cobertura de chocolate?"* | `min_similarity=0.30` | **Bloqueio preventivo ativado.** O sistema detecta similaridade inferior a 0.30, recusa a geração e informa ausência de evidências na base. **Zero alucinação.** |

---

## 🚀 6. Instruções de Instalação e Execução

### Opção A: Execução no Databricks (Ambiente Oficial)
1. Acesse seu workspace Databricks.
2. Na barra lateral, acesse **Workspace** -> navegue até sua pasta pessoal -> clique em **Import** (Importar).
3. Selecione o arquivo `notebooks/voice_of_customer.ipynb` localizado neste repositório.
4. Certifique-se de que os dados da Olist estejam no caminho `/Volumes/workspace/default/fase4-ecommerce`.
5. Anexe o notebook ao cluster e configure sua chave do Gemini como variável de ambiente ou via Secrets:
   ```python
   import os
   os.environ["GEMINI_API_KEY"] = "sua_chave_aqui"
   ```
6. Clique em **Run All** para executar todo o pipeline, gerar os gráficos, indexar no Delta Lake e rodar os 4 testes.

### Opção B: Execução Local com Jupyter
1. Clone o repositório:
   ```bash
   git clone https://github.com/SEU_USUARIO/olist-voc-intelligence-rag.git
   cd olist-voc-intelligence-rag
   ```
2. Crie e ative o ambiente virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate      # Windows
   ```
3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
4. Exporte a chave de API:
   ```bash
   export GEMINI_API_KEY="sua_chave_aqui"    # Linux/Mac
   $env:GEMINI_API_KEY="sua_chave_aqui"      # Windows PowerShell
   ```
5. Inicie o Jupyter:
   ```bash
   jupyter notebook
   ```

---

## 📁 7. Estrutura do Repositório

```text
├── data/
│   ├── .gitkeep
│   └── README.md                                    # Informações e links para download da base Olist
├── docs/
│   ├── .gitkeep
│   └── README.md                                    # Documentação de apoio e arquitetura
├── notebooks/
│   ├── .gitkeep
│   ├── README.md
│   └── voice_of_customer.ipynb                     # Notebook principal executado com EDA, Delta Lake e RAG
├── src/
│   ├── app/
│   │   ├── __init__.py
│   │   └── main.py                                  # Orquestração do pipeline RAG
│   ├── generation/
│   │   ├── __init__.py
│   │   └── llm.py                                   # Prompt engineering e conectores LLM (Gemini e Llama)
│   ├── indexing/
│   │   ├── __init__.py
│   │   └── embeddings.py                            # Carregamento do Sentence-Transformers e vetorização
│   ├── ingestion/
│   │   ├── __init__.py
│   │   └── load_data.py                             # Tratamento, enriquecimento e cálculo de atrasos
│   ├── retrieval/
│   │   ├── __init__.py
│   │   └── search.py                                # Busca semântica por cosseno e threshold anti-alucinação
│   └── __init__.py
├── .env.example                                     # Modelo para configuração das variáveis de ambiente
├── .gitignore                                       # Filtro de segurança contra tokens e arquivos temporários
├── README.md                                        # Documentação executiva completa da solução
└── requirements.txt                                 # Lista de dependências Python para reprodução
```

---

## 🎥 8. Vídeo de Apresentação

O vídeo está disponível em:

---

## 👥 9. Equipe do Projeto
- **Ana Beatriz Porto Pereira** — RM 372544
- **Jade Ferreira** — RM 373208
- **Felipe Nadal de Oliveira** — RM 372547
- **Winny Tavares** — RM 371471
- **Curso:** Pós-Tech AI / Tech Challenge - Fase 4 - 2026
