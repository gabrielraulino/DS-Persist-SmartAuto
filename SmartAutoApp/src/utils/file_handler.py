"""
Autor : Gabriel Raulino
"""

import csv
from typing import List, Dict


# Função para ler dados de um arquivo CSV
def read_csv(file_path: str) -> List[Dict[str, str]]:
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
        with open(file_path, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            return [row for row in reader]
    except FileNotFoundError:
        # Se o arquivo não existir, retorna uma lista vazia
        return []


# Função para adicionar uma linha ao arquivo CSV
def append_csv(file_path: str, fieldnames: List[str], row: Dict[str, str]) -> None:
    """
    Autor : Gabriel Raulino

    Adiciona uma linha ao final de um arquivo CSV. Se o arquivo estiver vazio,
    adiciona também o cabeçalho antes de inserir a linha.

    Args:
        file_path (str): O caminho do arquivo CSV a ser escrito.
        fieldnames (List[str]): Lista com os nomes das colunas (cabeçalho do CSV).
        row (Dict[str, str]): Dicionário representando a linha a ser adicionada ao CSV.
    """
    with open(file_path, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        # Se o arquivo estiver vazio, escreve o cabeçalho
        if file.tell() == 0:
            writer.writeheader()
        writer.writerow(row)


# Função para reescrever todo o arquivo CSV com novos dados
def write_csv(
    file_path: str, fieldnames: List[str], rows: List[Dict[str, str]]
) -> None:
    """
    Autor : Gabriel Raulino

    Reescreve todo o arquivo CSV com uma nova lista de linhas. Essa operação
    sobrescreve o conteúdo existente no arquivo.

    Args:
        file_path (str): O caminho do arquivo CSV a ser reescrito.
        fieldnames (List[str]): Lista com os nomes das colunas (cabeçalho do CSV).
        rows (List[Dict[str, str]]): Lista de dicionários, onde cada dicionário representa uma linha do CSV.
    """
    with open(file_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        # Escreve o cabeçalho no arquivo CSV
        writer.writeheader()
        # Escreve todas as linhas fornecidas
        writer.writerows(rows)
