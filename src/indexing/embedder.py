"""
Módulo de geração de embeddings densos multilíngues (384-D) e persistência
da base vetorial para recuperação semântica.
"""
from typing import List, Union
import numpy as np
import pandas as pd


class ReviewEmbedder:
    """
    Encapsula o modelo sentence-transformers para gerar embeddings normalizados
    das avaliações da Olist em português.
    """

    DEFAULT_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

    def __init__(self, model_name: str = DEFAULT_MODEL):
        from sentence_transformers import SentenceTransformer

        self.model_name = model_name
        self.model = SentenceTransformer(model_name)

    def encode_documents(
        self, texts: List[str], batch_size: int = 128, show_progress: bool = True
    ) -> np.ndarray:
        """Gera embeddings L2-normalizados para lista de documentos."""
        embeddings = self.model.encode(
            texts,
            batch_size=batch_size,
            show_progress_bar=show_progress,
            normalize_embeddings=True,
        )
        return np.asarray(embeddings, dtype=np.float32)

    def encode_query(self, query: str) -> np.ndarray:
        """Transforma a pergunta do usuário no espaço vetorial de 384 dimensões."""
        embedding = self.model.encode(
            [query],
            normalize_embeddings=True,
        )[0]
        return np.asarray(embedding, dtype=np.float32)


def salvar_base_indexada(
    df_rag: pd.DataFrame, embeddings: np.ndarray, output_parquet: str
) -> None:
    """Salva o dataframe com a coluna de vetor associada em formato Parquet/Delta."""
    df_out = df_rag.copy()
    df_out["embedding"] = [vec.tolist() for vec in embeddings]
    df_out.to_parquet(output_parquet, index=False)
