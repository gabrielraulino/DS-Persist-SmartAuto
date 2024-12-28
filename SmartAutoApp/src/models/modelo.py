from pydantic import BaseModel
import uuid
from typing import Union


class Modelo(BaseModel):
    id: Union[uuid.UUID, None] = None
    nome: str
