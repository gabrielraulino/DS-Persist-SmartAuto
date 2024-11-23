import hashlib

def calcular_hash_sha256(file_path: str) -> str:
    """
    Calcula o hash SHA256 de um arquivo.

    Args:
        file_path (str): Caminho do arquivo para calcular o hash.

    Returns:
        str: Hash SHA256 do arquivo.
    """
    sha256 = hashlib.sha256()
    try:
        with open(file_path, "rb") as file:
            # Lê o arquivo em blocos para evitar problemas de memória com arquivos grandes
            for bloco in iter(lambda: file.read(4096), b""):
                sha256.update(bloco)
        return sha256.hexdigest()
    except FileNotFoundError:
        raise FileNotFoundError("Arquivo não encontrado.")
