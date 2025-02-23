from odmantic import Model, Reference, Field
from typing import List, Optional

class Categoria(Model):
    nome: str
    desc: str
    # Se desejar manter uma lista de veículos associados à categoria,
    # pode definir como uma lista (embora a relação seja normalmente unidirecional).
    veiculos: Optional[List["Veiculo"]] = Field(default_factory=list)

    class Config:
        collection = "categorias"

class Veiculo(Model):
    nome: str
    # Utiliza a referência para o modelo Categoria, em vez de armazenar apenas o id.
    categoria: Categoria = Reference()

    class Config:
        collection = "veiculos"
