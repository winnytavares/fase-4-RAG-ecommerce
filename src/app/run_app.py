"""
Inicializador local da interface interativa Voice of Customer (VoC) RAG.
"""
import http.server
import socketserver
import webbrowser
from pathlib import Path

PORT = 8501
APP_DIR = Path(__file__).resolve().parent


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(APP_DIR), **kwargs)


def main():
    url = f"http://localhost:{PORT}/voc_agent_ui.html"
    print(f"🚀 Iniciando Interface VoC RAG em: {url}")
    print("Pressione Ctrl+C para encerrar o servidor.")
    
    webbrowser.open(url)
    
    with socketserver.TCPServer(("", PORT), QuietHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Servidor encerrado com sucesso.")


if __name__ == "__main__":
    main()
