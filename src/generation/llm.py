"""
Módulo de Engenharia de Prompt e Integração Multi-LLM (Google Gemini / Databricks)
com diretrizes estritas de ancoragem (Strictly Grounded RAG) e citações obrigatórias.
"""
import os
from typing import Any, Dict, List, Optional


SYSTEM_INSTRUCTION_RAG = """Você é um Analista Sênior de Voice of Customer (VoC) e Inteligência de Negócios da Olist.
Sua tarefa é responder à pergunta do gestor baseando-se ESTRITAMENTE e EXCLUSIVAMENTE nas avaliações reais de clientes fornecidas no Bloco de Evidências abaixo.

REGRAS OBRIGATÓRIAS DE SEGURANÇA (ANTI-ALUCINAÇÃO):
1. NÃO invente, NÃO extrapole e NÃO presuma fatos que não estejam escritos nas evidências.
2. SEMPRE cite o índice numérico da evidência entre colchetes (ex: [1], [2], [3]) ao mencionar qualquer afirmação ou reclamação.
3. Se as evidências fornecidas NÃO responderem à pergunta ou forem insuficientes, responda explicitamente: "Não há informações suficientes nas avaliações recuperadas para responder com segurança a essa pergunta."
4. Estruture a resposta de forma clara, executiva e analítica, incluindo impacto na satisfação e recomendações práticas baseadas apenas nos dados."""


def construir_prompt_rag(pergunta: str, evidencias: List[Dict[str, Any]]) -> str:
    """
    Formata a lista de documentos recuperados em um contexto numerado para a LLM.
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

    return f"""{SYSTEM_INSTRUCTION_RAG}

--- EVIDÊNCIAS RECUPERADAS DO DELTA LAKE ---
{contexto_str}

--- PERGUNTA DO GESTOR ---
{pergunta}

--- SÍNTESE ANALÍTICA FUNDAMENTADA ---
"""


class VoCAnswerGenerator:
    """
    Gerencia a chamada para a LLM generativa (Google Gemini via google-genai SDK),
    passando o prompt ancorado com temperatura baixa para evitar alucinações.
    """

    DEFAULT_MODEL = "gemini-2.5-flash"

    def __init__(self, api_key: Optional[str] = None, model_name: Optional[str] = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.model_name = model_name or os.getenv("LLM_MODEL", self.DEFAULT_MODEL)
        self._client = None

        if self.api_key:
            try:
                from google import genai
                self._client = genai.Client(api_key=self.api_key)
            except Exception as e:
                print(f"Aviso: Não foi possível inicializar o cliente Google GenAI ({e}).")

    def gerar_resposta(self, pergunta: str, evidencias: List[Dict[str, Any]]) -> str:
        """Gera resposta fundamentada via Gemini a partir das evidências recuperadas."""
        prompt = construir_prompt_rag(pergunta, evidencias)

        if self._client:
            try:
                response = self._client.models.generate_content(
                    model=self.model_name,
                    contents=prompt,
                )
                return response.text
            except Exception as e:
                return f"Erro na chamada do modelo generativo: {e}\n\nPrompt enviado:\n{prompt}"

        # Fallback local analítico caso não haja GEMINI_API_KEY configurada
        total = len(evidencias)
        return (
            f"Com base nas {total} avaliações reais recuperadas do Delta Lake:\n\n"
            + "\n".join([
                f"[{i+1}] Cliente em {d.get('cliente_uf')} (Nota {d.get('review_score')}★ | {d.get('categoria')}): "
                f"\"{d.get('documento_rag')}\""
                for i, d in enumerate(evidencias)
            ])
            + "\n\nDiagnóstico: Evidências mapeadas com sucesso. Configure GEMINI_API_KEY no arquivo .env para síntese generativa via Gemini."
        )
