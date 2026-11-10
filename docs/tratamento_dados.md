# 🧹 Tratamento de Dados, Preparação e Engenharia de Metadados

Este documento detalha o tratamento de dados realizado na solução, atendendo ao **Requisito 1 (Construção da Base de Conhecimento)** e ao **Desafio Adicional (Metadados e Exploração Contextual)** do Tech Challenge.

---

## ⏱️ Em Qual Momento o Tratamento Foi Realizado?

O tratamento de dados foi executado **logo após a carga das 7 tabelas relacionais brutas e estritamente antes da vetorização/geração de embeddings**. No notebook Databricks, corresponde às **Seções 2 e 3**.

```
[Dados Brutos Olist] ➔ [Tratamento de Nulos & Desduplicação] ➔ [Enriquecimento Relacional] ➔ [Vetorização Delta]
     (Seção 2)                        (Seção 2)                          (Seção 3)                 (Seção 4)
```

---

## 📊 1. Seleção dos Dados e Tratamento de Valores Ausentes

### Diagnóstico da Volumetria Inicial
A base de avaliações brutas (`df_reviews`) continha originalmente **99.224 registros**:

| Condição da Avaliação | Quantidade | Percentual (%) | Justificativa Técnica no Pipeline RAG |
| :--- | :---: | :---: | :--- |
| **Com Texto (Mensagem ou Título)** | **42.389** | **42,72%** | **Mantidas e indexadas:** possuem conteúdo em linguagem natural para extração semântica. |
| **Sem Texto (Apenas Nota Numérica)** | **56.835** | **57,28%** | **Descartadas:** mais da metade dos clientes deram nota de 1 a 5 sem escrever texto. Incluir registros sem texto geraria ruído vetorial e alucinações no LLM. |
| **Total Bruto Original** | **99.224** | **100,00%** | Base total de avaliações da Olist. |

### Desduplicação
Aplicação de `drop_duplicates(subset=['review_id'])` para assegurar que cada avaliação seja vetorizada uma única vez no espaço semântico.

---

## 🧩 2. Enriquecimento Relacional com Metadados (Desafio Adicional)

Para permitir análises contextuais por categoria, atraso de entrega e região, cruzou-se a base textual com as tabelas relacionais:

### A. Tradução e Imputação de Categorias de Produtos
- Cruzamento com `product_category_name_translation.csv` para padronizar nomes em português.
- Tratamento de nulos com imputação de `"não informada"` via `fillna('não informada')`.
- Agregação no grão do pedido (`order_id`) para suportar pedidos com múltiplos itens.

### B. Engenharia de Features Logísticas (Atraso Real)
- Conversão de strings de data para `pd.to_datetime`:
  - `order_delivered_customer_date` (data real da entrega)
  - `order_estimated_delivery_date` (data limite prometida)
- Cálculo matemático dos dias corridos de atraso:
  $$\text{dias\_atraso} = (\text{data\_entrega} - \text{data\_estimada}).\text{days}$$
- Criação da flag booleana `atrasou` (`True` quando entregue após o prazo prometido, `False` quando entregue no prazo ou antecipada).

### C. Consolidação Multitabela
Junção relacional através do `order_id` unificando:
- Dados do Cliente (Estado `customer_state`)
- Dados do Pagamento (Tipo de pagamento e valor total pago)
- Dados do Vendedor (Estado do seller)

---

## 📝 3. Higienização Textual e Construção dos Chunks RAG

### Função `limpar_texto()`
- Remoção de quebras de linha (`\n`, `\r`), tabulações (`\t`) e múltiplos espaços sequenciais utilizando regex:
  ```python
  re.sub(r'\s+', ' ', texto).strip()
  ```

### Estrutura Canônica do Documento (`documento_rag`)
Cada chunk enviado para o modelo de embeddings foi estruturado em um formato canônico que une metadados e texto:

```text
Nota: 1/5 | Categoria: informatica_acessorios | Entrega: Atrasada 4 dias | Cliente: SP | Título: Não recebi | Comentário: O produto anunciado era para ter chegado há quase uma semana e não tenho código de rastreamento.
```

Esse formato permite que o modelo de embeddings aprenda simultaneamente o sentimento do comprador e as circunstâncias operacionais da compra.
