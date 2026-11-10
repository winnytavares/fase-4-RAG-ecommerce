"""
Módulo de recuperação semântica (Retriever) com suporte a busca por cosseno
e filtragem dinâmica de metadados (nota, categoria, atraso).
"""
from typing import Any, Dict, List, Optional
import numpy as np
import pandas as pd


class DeltaVoCRetriever:
    """
    Recupera as Top-K avaliações mais relevantes usando produto escalar
    (equivalente à similaridade por cosseno em vetores normalizados).
    """

    def __init__(self, df_reviews: pd.DataFrame, embeddings_matrix: Optional[np.ndarray] = None):
        self.df = df_reviews.reset_index(drop=True)
        if embeddings_matrix is not None:
            self.embeddings = embeddings_matrix
        elif "embedding" in self.df.columns:
            self.embeddings = np.vstack(self.df["embedding"].values).astype(np.float32)
        else:
            self.embeddings = None

    def buscar(
        self,
        query_embedding: np.ndarray,
        top_k: int = 5,
        nota_max: Optional[int] = None,
        nota_min: Optional[int] = None,
        categoria: Optional[str] = None,
        apenas_atrasados: Optional[bool] = None,
    ) -> List[Dict[str, Any]]:
        """
        Executa busca vetorial aplicando previamente filtros relacionais nos metadados.
        """
        if self.embeddings is None:
            raise ValueError("Matriz de embeddings não carregada no Retriever.")

        # Aplica máscara de metadados
        mask = np.ones(len(self.df), dtype=bool)

        if nota_max is not None:
            mask &= (self.df["review_score"] <= nota_max).values
        if nota_min is not None:
            mask &= (self.df["review_score"] >= nota_min).values
        if categoria:
            mask &= self.df["categoria"].str.contains(categoria, case=False, na=False).values
        if apenas_atrasados is not None:
            mask &= (self.df["atrasou"] == apenas_atrasados).values

        indices_filtrados = np.where(mask)[0]
        if len(indices_filtrados) == 0:
            return []

        # Calcula similaridade de cosseno (vetores L2-normalizados => dot product)
        emb_sub = self.embeddings[indices_filtrados]
        similaridades = np.dot(emb_sub, query_embedding)

        # Seleciona Top-K em ordem decrescente de similaridade
        top_local_idx = np.argsort(similaridades)[::-1][:top_k]

        resultados = []
        for idx_local in top_local_idx:
            idx_global = indices_filtrados[idx_local]
            row = self.df.iloc[idx_global]
            resultados.append({
                "similaridade": float(similaridades[idx_local]),
                "review_id": str(row.get("review_id", "")),
                "review_score": int(row.get("review_score", 0)),
                "categoria": str(row.get("categoria", "")),
                "dias_atraso": int(row.get("dias_atraso", 0)),
                "atrasou": bool(row.get("atrasou", False)),
                "cliente_uf": str(row.get("cliente_uf", "")),
                "documento_rag": str(row.get("documento_rag", "")),
            })

        return resultados
