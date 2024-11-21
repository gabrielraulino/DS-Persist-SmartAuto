# imports do fastAPI
from typing import Union
from fastapi import FastAPI

# imports dos models
from pydantic import BaseModel
from src.model.Endereco import Endereco
from src.model.Veiculo import Veiculo
from src.model.Venda import Venda
from src.model.Locacao import Locacao
from src.model.Cliente import Cliente
from src.model.Vendedor import Vendedor
from src.model.Gerente import Gerente
from src.model.Cliente import Cliente

app = FastAPI()


@app.get("/")
def read_root():
    return {"msg": "Hello World"}
