"""
Autor : Antonio Kleberson
"""

import zipfile
import os

from fastapi import HTTPException
from fastapi.responses import FileResponse


def compactar_csv(file_path: str):
    """
    Compacta um arquivo CSV em um arquivo ZIP.

    Args:
        file_path (str): Caminho do arquivo CSV a ser compactado.

    Returns:
        str: Caminho do arquivo ZIP gerado.
    """

    # verifica se o path é válido
    if not os.path.isfile(file_path):
        # return {"Arquivo não foi encontrado."}
        raise HTTPException(status_code=404, detail="Arquivo não encontrado.")
    # Define o nome do arquivo ZIP com base no CSV
    zip_file_path = file_path.replace(
        ".csv", ".zip"
    )  # garante que o nome do arquivo fique com o final .zip

    # Cria o arquivo ZIP
    with zipfile.ZipFile(zip_file_path, "w", zipfile.ZIP_DEFLATED) as zip_file:
        # Adiciona o arquivo CSV ao ZIP
        zip_file.write(file_path, os.path.basename(file_path))

    return FileResponse(
        path=zip_file_path,
        media_type="application/zip",
        filename=os.path.basename(zip_file_path),
    )
