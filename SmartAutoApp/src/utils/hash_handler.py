"""
Autor : Antonio Kleberson
"""

import hashlib

from fastapi import HTTPException


def calcular_hash_sha256(file_path: str) -> str:
    """
    Calcula o hash SHA256 de um arquivo.

    Args:
        file_path (str): Caminho do arquivo para calcular o hash.

    Returns:
        str: Hash SHA256 do arquivo.
    """
    # verifica se o path é válido
    try:
        with open(file_path, "rb") as file:
            return hashlib.sha256(file.read()).hexdigest()
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Arquivo não encontrado.")
