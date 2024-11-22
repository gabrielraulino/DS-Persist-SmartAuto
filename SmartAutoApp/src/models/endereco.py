import uuid
from pydantic import BaseModel


class Endereco(BaseModel):
    id: uuid.UUID
    uf: str
    cidade: str
    logradouro: str
    numero: str
