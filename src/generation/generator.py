"""
Módulo de integração com LLMs (Google Gemini e Databricks Foundation Models)
para geração da resposta final grounded.
"""
import os
from typing import Any, Dict, List, Optional
from src.generation.prompt_templates import construir_prompt_rag


class VoCAnswerGenerator:
    """
    Gerencia a chamada para a LLM generativa, passando o prompt ancorado
    e garantindo a parametrização de temperatura baixa (zero alucinação).
    """

    DEFAULT_MODEL = "gemini-2.5-flash"

    def __init__(self, api_key: Optional[str] = None, model_name: str = DEFAULT_MODEL):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.model_name = model_name
        self._client = None

        if self.api_key:
            try:
                import google.generativeai as genai
                genai.configure(api_key=self.api_key)
                self._client = genai.GenerativeModel(
                    model_name=self.model_name,
                    generation_config={
                        "temperature": 0.1,  # Temperatura quase nula para estrito grounding
                        "top_p": 0.85,
                        "max_output_tokens": 1024,
                    },
                )
            except Exception as e:
                print(f"Aviso: Não foi possível instanciar google-generativeai ({e}).")

    def gerar_resposta(self, pergunta: str, evidencias: List[Dict[str, Any]]) -> str:
        """Gera resposta via Gemini a partir das evidências recuperadas."""
        prompt = construir_prompt_rag(pergunta, evidencias)

        if self._client:
            try:
                response = self._client.generate_content(prompt)
                return response.text
            except Exception as e:
                return f"Erro na chamada do modelo generativo: {e}\n\nPrompt enviado:\n{prompt}"

        # Fallback local analítico sem chamada de API externa
        total = len(evidencias)
        return (
            f"Com base nas {total} avaliações reais recuperadas do Delta Lake:\n\n"
            + "\n".join([
                f"[{i+1}] Cliente em {d.get('cliente_uf')} (Nota {d.get('review_score')}★ | {d.get('categoria')}): "
                f"\"{d.get('documento_rag')}\""
                for i, d in enumerate(evidencias)
            ])
            + f"\n\nDiagnóstico: Evidências mapeadas com sucesso. Configure GEMINI_API_KEY no arquivo .env para síntese generativa completa."
        )
