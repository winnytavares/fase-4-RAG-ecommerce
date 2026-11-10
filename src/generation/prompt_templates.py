"""
Templates de engenharia de prompt com ancoragem estrita (Strictly Grounded RAG)
e citações obrigatórias das evidências recuperadas.
"""
from typing import Any, Dict, List


SYSTEM_INSTRUCTION_RAG = """Você é um Analista Sênior de Voice of Customer (VoC) e Inteligência de Negócios da Olist.
Sua tarefa é responder à pergunta do gestor baseando-se ESTRITAMENTE e EXCLUSIVAMENTE nas avaliações reais de clientes fornecidas no Bloco de Evidências abaixo.

REGRAS OBRIGATÓRIAS DE SEGURANÇA (ANTI-ALUCINAÇÃO):
1. NÃO invente, NÃO extrapole e NÃO presuma fatos que não estejam escritos nas evidências.
2. SEMPRE cite o índice numérico da evidência entre colchetes (ex: [1], [2], [3]) ao mencionar qualquer afirmação ou reclamação.
3. Se as evidências fornecidas NÃO responderem à pergunta ou forem insuficientes, responda explicitamente: "Não há informações suficientes nas avaliações recuperadas para responder com segurança a essa pergunta."
4. Estruture a resposta de forma clara, executiva e analítica, incluindo impacto na satisfação e recomendações práticas baseadas apenas nos dados."""


def construir_prompt_rag(pergunta: str, evidencias: List[Dict[str, Any]]) -> str:
    """
    Formata a lista de documentos recuperados em um contexto numerado para o LLM.
    """
    if not evidencias:
        contexto_str = "Nenhuma avaliação relevante recuperada."
    else:
        blocos = []
        for idx, doc in enumerate(evidencias, start=1):
            sim = doc.get("similaridade", 0.0)
            texto = doc.get("documento_rag", "")
            blocos.append(f"[{idx}] (cos(θ)={sim:.3f}) {texto}")
        contexto_str = "\n".join(blocos)

    prompt = f"""{SYSTEM_INSTRUCTION_RAG}

--- EVIDÊNCIAS RECUPERADAS DO DELTA LAKE ---
{contexto_str}

--- PERGUNTA DO GESTOR ---
{pergunta}

--- SÍNTESE ANALÍTICA FUNDAMENTADA ---
"""
    return prompt
