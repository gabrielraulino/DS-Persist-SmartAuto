import csv
from typing import List, Dict


# Função para ler dados de um arquivo CSV
def read_csv(file_path: str) -> List[Dict[str, str]]:
    try:
        with open(file_path, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            return [row for row in reader]
    except FileNotFoundError:
        # Se o arquivo não existir, retorna uma lista vazia
        return []


# Função para adicionar uma linha ao arquivo CSV
def append_csv(file_path: str, fieldnames: List[str], row: Dict[str, str]) -> None:
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
    with open(file_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
