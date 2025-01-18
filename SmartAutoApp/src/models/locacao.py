# Autor: Antonio Kleberson
from sqlmodel import SQLModel, Field
from datetime import date


class Locacao(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    data_inicio: date
    data_fim: date
    valor_diaria: float
    cliente_id: int
    vendedor_id: int
    veiculo_id: int
