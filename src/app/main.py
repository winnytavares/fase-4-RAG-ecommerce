"""
Orquestrador principal (CLI) do Pipeline Voice of Customer RAG.
Executa busca semântica sobre os dados do Delta Lake, aplica o Guardrail
Anti-Alucinação e gera sínteses fundamentadas com citações.
"""
import argparse
import sys
from pathlib import Path
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(ROOT_DIR))

from src.retrieval.guardrail import validar_seguranca_guardrail
from src.retrieval.search import DeltaVoCRetriever
from src.indexing.embeddings import ReviewEmbedder
from src.generation.llm import VoCAnswerGenerator


def carregar_dados_amostra() -> pd.DataFrame:
    """Carrega o dataset exportado da tabela Delta Lake."""
    csv_path = ROOT_DIR / "data" / "sample_reviews_rag.csv"
    if not csv_path.exists():
        raise FileNotFoundError(f"Arquivo de dados não encontrado em: {csv_path}")
    return pd.read_csv(csv_path)


def executar_pipeline(
    pergunta: str,
    top_k: int = 4,
    nota_max: int = None,
    nota_min: int = None,
    categoria: str = None,
):
    print("=" * 80)
    print(f"🔍 Pergunta: {pergunta}")
    print("=" * 80)

    df_reviews = carregar_dados_amostra()
    print(f"✓ Base carregada: {len(df_reviews)} avaliações reais do Delta Lake.")

    print("✓ Vetorizando pergunta e documentos com paraphrase-multilingual-MiniLM-L12-v2...")
    embedder = ReviewEmbedder()
    query_vec = embedder.encode_query(pergunta)
    doc_embeddings = embedder.encode_documents(
        df_reviews["documento_rag"].tolist(), show_progress=False
    )

    retriever = DeltaVoCRetriever(df_reviews, doc_embeddings)
    evidencias = retriever.buscar(
        query_embedding=query_vec,
        top_k=top_k,
        nota_max=nota_max,
        nota_min=nota_min,
        categoria=categoria,
    )

    sim_max = evidencias[0]["similaridade"] if evidencias else 0.0

    # Validação de Segurança: "Cuidado com alucinações"
    aprovado, motivo_bloqueio = validar_seguranca_guardrail(
        pergunta=pergunta, similaridade_maxima=sim_max
    )

    if not aprovado:
        print("\n" + motivo_bloqueio + "\n")
        return

    print(f"✓ Guardrail aprovado: cos(θ)={sim_max:.3f} >= 0.30")
    print(f"✓ Top-{len(evidencias)} evidências recuperadas:")
    for idx, e in enumerate(evidencias, start=1):
        print(f"   [{idx}] (cos(θ)={e['similaridade']:.3f} | {e['review_score']}★ | {e['categoria']}): {e['documento_rag'][:100]}...")

    print("\n✓ Gerando resposta analítica fundamentada...")
    generator = VoCAnswerGenerator()
    resposta = generator.gerar_resposta(pergunta, evidencias)

    print("\n" + "=" * 80)
    print("📝 RESPOSTA DO AGENTE VoC:")
    print("=" * 80)
    print(resposta)
    print("=" * 80)


def main():
    parser = argparse.ArgumentParser(description="Voice of Customer RAG Pipeline")
    parser.add_argument(
        "--pergunta",
        "-p",
        type=str,
        default="Quais são os principais problemas relatados nas avaliações com nota baixa?",
        help="Pergunta para o agente de CX",
    )
    parser.add_argument("--top_k", "-k", type=int, default=4, help="Número de documentos recuperados")
    parser.add_argument("--nota_max", type=int, default=None, help="Filtrar notas <= valor")
    parser.add_argument("--nota_min", type=int, default=None, help="Filtrar notas >= valor")
    parser.add_argument("--categoria", type=str, default=None, help="Filtrar por categoria")

    args = parser.parse_args()
    executar_pipeline(
        pergunta=args.pergunta,
        top_k=args.top_k,
        nota_max=args.nota_max,
        nota_min=args.nota_min,
        categoria=args.categoria,
    )


if __name__ == "__main__":
    main()
