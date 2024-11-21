from pydantic import BaseModel
import uuid


class Veiculo(BaseModel):
    def __init__(
        self,
        marca: str,
        modelo: str,
    ):
        self
