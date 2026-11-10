"""
Módulo de Guardrail de Segurança Anti-Alucinação ("Cuidado com alucinações").
Implementa a validação estrita de escopo e limiar mínimo de similaridade
semântica de cosseno (cos(θ) >= 0.30) para prevenir respostas enganosas.
"""
import unicodedata
from typing import Dict, List, Optional, Tuple


# Termos que representam explicitamente domínios externos ao e-commerce da Olist
FORBIDDEN_OUT_OF_SCOPE_TERMS = [
    "napoleao", "bonaparte", "cavalo", "bolo", "receita", "futebol", "jogo",
    "presidente", "capital", "previsao do tempo", "tempo amanha", "piada",
    "codigo", "python", "matematica", "quem foi", "quem e", "filme", "musica",
    "quantos anos", "copa do mundo", "biologia", "quimica", "cenoura", "politica",
    "geografia", "historia", "planeta", "universo", "filosofia", "lua", "sol",
    "charada", "signo", "horoscopo", "religiao", "igreja", "biblia", "ator", "atriz",
    "bitcoin", "cripto", "lula", "bolsonaro", "formula 1", "f1", "brasileirao",
]

# Termos que confirmam alinhamento com o ecossistema de compras da Olist
ECOMMERCE_DOMAIN_TERMS = [
    "entrega", "entregador", "atraso", "atrasou", "frete", "prazo", "produto",
    "loja", "lojista", "vendedor", "cliente", "compra", "pedido", "qualidade",
    "defeito", "falsificado", "original", "avaliacao", "nota", "reclamacao",
    "elogio", "recomendo", "sac", "atendimento", "correios", "transportadora",
    "telefonia", "informatica", "relogio", "pagamento", "devolucao", "reembolso",
    "pacote", "embalagem", "danificado", "chegou", "recebi", "olist", "score",
]

DEFAULT_MIN_SIMILARITY_THRESHOLD = 0.30


def normalizar_texto(texto: str) -> str:
    """Remove acentuações e converte para minúsculas."""
    if not texto:
        return ""
    nfkd = unicodedata.normalize("NFKD", texto)
    sem_acento = "".join([c for c in nfkd if not unicodedata.combining(c)])
    return sem_acento.lower().strip()


def verificar_fora_de_escopo(pergunta: str) -> bool:
    """
    Avalia se a pergunta possui intenção claramente fora do escopo de e-commerce Olist.
    """
    q_norm = normalizar_texto(pergunta)

    # 1. Verifica termos expressamente proibidos
    for termo in FORBIDDEN_OUT_OF_SCOPE_TERMS:
        if termo in q_norm:
            return True

    # 2. Verifica ausência total de termos de e-commerce em perguntas com 2+ palavras
    palavras = [p for p in q_norm.split() if len(p) >= 3]
    possui_termo_ecom = any(t in q_norm for t in ECOMMERCE_DOMAIN_TERMS)
    if not possui_termo_ecom and len(palavras) >= 2:
        return True

    return False


def validar_seguranca_guardrail(
    pergunta: str,
    similaridade_maxima: float,
    threshold: float = DEFAULT_MIN_SIMILARITY_THRESHOLD,
) -> Tuple[bool, Optional[str]]:
    """
    Executa a auditoria completa do Guardrail de Segurança:
    1. Verifica desvio de escopo semântico.
    2. Compara a similaridade máxima obtida no Delta Lake contra o corte cos(θ) >= threshold.

    Returns:
        Tuple: (esta_aprovado: bool, mensagem_bloqueio: Optional[str])
    """
    fora_de_escopo = verificar_fora_de_escopo(pergunta)
    abaixo_do_limiar = similaridade_maxima < threshold

    if fora_de_escopo or abaixo_do_limiar:
        motivo = (
            f"🛡️ BLOQUEIO DE SEGURANÇA ATIVADO (Cuidado com alucinações)\n\n"
            f"Com base estritamente no corpus de avaliações reais de clientes da Olist, "
            f"não há informações ou evidências suficientes para responder à pergunta.\n\n"
            f"• Similaridade Máxima Encontrada: cos(θ) = {similaridade_maxima:.3f}\n"
            f"• Limiar Mínimo de Corte: cos(θ) >= {threshold:.2f}\n"
            f"• Restrição de Domínio: O agente opera com recusa preventiva para perguntas "
            f"fora do domínio de compras, pedidos, entregas e atendimento do e-commerce Olist."
        )
        return False, motivo

    return True, None
