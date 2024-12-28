"""
Autor : Gabriel Raulino
"""

import csv
from typing import List, Dict
import pandas as pd


# Função para ler dados de um arquivo CSV
def read_csv(file_path: str) -> pd.DataFrame:
    """
    Autor : Gabriel Raulino

    Lê os dados de um arquivo CSV e retorna uma lista de dicionários,
    onde cada dicionário representa uma linha do CSV.

    Args:
        file_path (str): O caminho do arquivo CSV a ser lido.

    Returns:
        List[Dict[str, str]]: Lista de dicionários com os dados do CSV.
    """
    try:
        df = pd.read_csv(file_path)
    except (FileNotFoundError, pd.errors.EmptyDataError):
        df = (
            pd.DataFrame()
        )  # Inicializa com DataFrame vazio se o arquivo não for encontrado
    return df


# Função para adicionar uma linha ao arquivo CSV
def append_csv(
    file_path: str, fieldnames: List[str], row: Dict[str, str], dataframe: pd.DataFrame
):
    """
    Autor : Gabriel Raulino

    Adiciona uma linha ao final de um arquivo CSV.

    Args:
        file_path (str): O caminho do arquivo CSV a ser escrito.
        row (Dict[str, str]): Dicionário representando a linha a ser adicionada ao CSV.
    """
    new_row = pd.DataFrame([row])
    # Adiciona a nova linha ao DataFrame em memória
    dataframe = pd.concat([dataframe, new_row], ignore_index=True)

    with open(file_path, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        # Se o arquivo estiver vazio, escreve o cabeçalho
        if file.tell() == 0:
            writer.writeheader()
        writer.writerow(row)
    return dataframe


# Função para reescrever todo o arquivo CSV com novos dados
def write_csv(file_path: str, rows: List[Dict[str, str]]) -> None:
    """
    Autor : Gabriel Raulino

    Reescreve todo o arquivo CSV com uma nova lista de linhas. Essa operação
    sobrescreve o conteúdo existente no arquivo.

    Args:
        file_path (str): O caminho do arquivo CSV a ser reescrito.
        rows (List[Dict[str, str]]): Lista de dicionários, onde cada dicionário representa uma linha do CSV.
    """
    df = pd.DataFrame(rows)
    df.to_csv(file_path, index=False)


def count_elements(file_path: str) -> int:
    try:
        df = pd.read_csv(file_path)
        return len(df)
    except Exception:
        return 0
