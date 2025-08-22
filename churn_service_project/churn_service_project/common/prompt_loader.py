"""Função reutilizável para carregar prompts de arquivos."""

def load_prompt(file_path: str) -> str:
    """
    Carrega o conteúdo de um arquivo de prompt.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        # Usamos 'app/' como prefixo porque o WORKDIR dentro do contêiner é /app
        full_path = f"app/{file_path}"
        print(f"AVISO: Arquivo de prompt não encontrado em '{file_path}'. Tentando com '{full_path}'")
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            print(f"AVISO: Arquivo de prompt também não encontrado em '{full_path}'. Retornando string vazia.")
            return ""