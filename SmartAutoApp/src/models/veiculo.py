from pydantic import BaseModel
import uuid


class Veiculo(BaseModel):
  id: uuid.UUID
  marca: str
  modelo: str
  ano: int
  preco: float
  valor_diaria: float
  cor: str
  disponivel: bool
