"""
Módulo de limpeza, tratamento de valores ausentes e engenharia de features
para preparação da base de conhecimento VoC (Olist).
"""
import re
from typing import Tuple
import pandas as pd


def limpar_texto(texto: str) -> str:
    """Remove múltiplos espaços, tabulações e quebras de linha de um comentário."""
    if not isinstance(texto, str):
        return ""
    return re.sub(r"\s+", " ", texto).strip()


def filtrar_avaliacoes_com_texto(df_reviews: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Filtra apenas avaliações com comentário ou título preenchido e remove duplicatas.
    Descarta avaliações com apenas nota numérica (ruído para busca semântica RAG).

    Returns:
        Tuple contendo (df_reviews_com_texto, df_diagnostico_texto)
    """
    total_bruto = len(df_reviews)

    df_com_texto = df_reviews[
        df_reviews["review_comment_message"].notna() |
        df_reviews["review_comment_title"].notna()
    ].drop_duplicates(subset=["review_id"]).copy()

    total_com_texto = len(df_com_texto)
    total_sem_texto = total_bruto - total_com_texto

    df_diagnostico = pd.DataFrame({
        "Condicao": [
            "Com Texto (Mensagem ou Título)",
            "Sem Texto (Apenas Nota Numérica)",
            "Total Bruto"
        ],
        "Quantidade": [total_com_texto, total_sem_texto, total_bruto],
        "Percentual (%)": [
            round((total_com_texto / total_bruto) * 100, 2) if total_bruto > 0 else 0.0,
            round((total_sem_texto / total_bruto) * 100, 2) if total_bruto > 0 else 0.0,
            100.0,
        ],
    })

    return df_com_texto, df_diagnostico


def calcular_atraso_logistico(df_orders: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula o atraso real em dias corridos comparando data de entrega
    efetiva vs data estimada prometida ao comprador.
    """
    df = df_orders.copy()
    df["order_delivered_customer_date"] = pd.to_datetime(
        df["order_delivered_customer_date"], errors="coerce"
    )
    df["order_estimated_delivery_date"] = pd.to_datetime(
        df["order_estimated_delivery_date"], errors="coerce"
    )

    df["atrasou"] = (
        df["order_delivered_customer_date"] > df["order_estimated_delivery_date"]
    ).fillna(False)

    df["dias_atraso"] = (
        (df["order_delivered_customer_date"] - df["order_estimated_delivery_date"]).dt.days
    ).fillna(0).astype(int)

    return df


def construir_documentos_rag(df_consolidado: pd.DataFrame) -> pd.DataFrame:
    """
    Constrói o documento textual canônico ('documento_rag') combinando a voz do cliente
    com os metadados relacionais enriquecidos (nota, categoria, atraso, UF).
    """
    docs = []
    for _, row in df_consolidado.iterrows():
        title = limpar_texto(row.get("review_comment_title", ""))
        msg = limpar_texto(row.get("review_comment_message", ""))
        score = int(row.get("review_score", 0))

        cats = row.get("categorias", [])
        if isinstance(cats, list) and len(cats) > 0:
            cat_str = ", ".join(str(c) for c in cats)
            primeira_cat = str(cats[0])
        else:
            cat_str = "não informada"
            primeira_cat = "não informada"

        atrasou = bool(row.get("atrasou", False))
        dias_atraso = int(row.get("dias_atraso", 0))
        status_entrega = f"Atrasada {dias_atraso} dias" if atrasou else "No prazo"
        cliente_uf = str(row.get("customer_state") or "N/A")

        texto_rag = (
            f"Nota: {score}/5 | Categoria: {cat_str} | "
            f"Entrega: {status_entrega} | Cliente: {cliente_uf}"
        )
        if title:
            texto_rag += f" | Título: {title}"
        if msg:
            texto_rag += f" | Comentário: {msg}"

        docs.append({
            "review_id": str(row.get("review_id", "")),
            "order_id": str(row.get("order_id", "")),
            "review_score": score,
            "categoria": primeira_cat,
            "atrasou": atrasou,
            "dias_atraso": dias_atraso,
            "cliente_uf": cliente_uf,
            "documento_rag": texto_rag,
        })

    return pd.DataFrame(docs)
