from typing import List
import pandas as pd

# from sqlmodel import SQLModel, Session, create_engine
# from src.models.funcionario import Funcionario
from models.cliente import Cliente

# from src.models.veiculo import Veiculo
# from src.models.locacao import Locacao
from src.models.venda import Venda
from datetime import date
# import os


def read_csv(file_path: str) -> pd.DataFrame:
    try:
        df = pd.read_csv(file_path)
    except (FileNotFoundError, pd.errors.EmptyDataError):
        df = pd.DataFrame()
    return df


# Caminhos dos arquivos CSV
clientes_file = "src/storage/clientes.csv"
veiculos_file = "src/storage/veiculos.csv"
funcionarios_file = "src/storage/funcionarios.csv"
locacoes_file = "src/storage/locacoes.csv"
vendas_file = "src/storage/vendas.csv"

# Carregar dados dos arquivos CSV
clientes_data = read_csv(clientes_file)
veiculos_data = read_csv(veiculos_file)
funcionarios_data = read_csv(funcionarios_file)
locacoes_data = read_csv(locacoes_file)
vendas_data = read_csv(vendas_file)


# Atualizar IDs dos clientes
def transforma_id(data: pd.DataFrame):
    for i, _ in enumerate(data.index):
        data.at[i, "id"] = i


veiculos_data.to_csv("src/storage/veiculos.csv", index=False)
