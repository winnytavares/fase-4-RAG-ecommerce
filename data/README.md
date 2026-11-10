# 📊 Estrutura de Dados & Amostras do Delta Lake

Este diretório contém as especificações dos dados utilizados no projeto **Voice of Customer Intelligence com RAG** e uma amostra representativa exportada da tabela Delta Lake para testes e reprodução local.

---

## 🗂️ Arquivos Disponíveis

- **[`sample_reviews_rag.csv`](./sample_reviews_rag.csv)**:
  Amostra real de **1.200 avaliações tratadas e enriquecidas**, exportadas diretamente da tabela Delta Lake oficial do projeto (`workspace.default.reviews_rag`).

### Dicionário de Dados de `sample_reviews_rag.csv`:

| Campo | Tipo | Descrição | Exemplo |
| :--- | :--- | :--- | :--- |
| `review_id` | String | Identificador único da avaliação do cliente | `d4c35b01aca52ab12caf4f18b9e771e0` |
| `review_score` | Integer | Nota de avaliação atribuída pelo cliente (1 a 5 estrelas) | `1` |
| `categoria` | String | Categoria do produto traduzida para português | `informatica_acessorios` |
| `dias_atraso` | Integer | Dias corridos de atraso em relação à data estimada (valores negativos indicam entrega adiantada) | `4` (atraso) ou `-12` (no prazo) |
| `atrasou` | Boolean | Flag indicando se houve descumprimento do prazo estimado | `true` ou `false` |
| `cliente_uf` | String | Sigla da Unidade Federativa (estado) do consumidor | `SP`, `RJ`, `MG` |
| `documento_rag` | String | Documento canônico estruturado utilizado na vetorização e recuperação | `Nota: 1/5 \| Categoria: informatica...` |

---

## 📦 Base Completa da Olist (Kaggle)

Para reprocessar a base bruta de 100 mil pedidos desde o início:
1. Baixe o dataset público da Olist no Kaggle:
   - 🔗 [Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce/data)
2. As tabelas originais utilizadas na ingestão relacional são:
   - `olist_order_reviews_dataset.csv` (99.224 linhas)
   - `olist_orders_dataset.csv` (99.441 linhas)
   - `olist_order_items_dataset.csv` (112.650 linhas)
   - `olist_products_dataset.csv` (32.951 linhas)
   - `olist_order_payments_dataset.csv` (103.886 linhas)
   - `olist_customers_dataset.csv` (99.441 linhas)
   - `olist_sellers_dataset.csv` (3.095 linhas)
   - `product_category_name_translation.csv` (71 categorias)
3. No Databricks, essas tabelas são carregadas a partir de Volumes do Unity Catalog (`/Volumes/workspace/default/fase4-ecommerce`).
