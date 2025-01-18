# Autor: Gabriel Raulino
from typing import Union
from sqlmodel import SQLModel, Field
from datetime import date


class Venda(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    data: Union[date, None] = None
    valor: float
    vendedor_id: int
    cliente_id: int
    veiculo_id: int
