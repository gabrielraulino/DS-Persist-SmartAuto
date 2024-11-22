from pydantic import BaseModel
import uuid


class Veiculo(BaseModel):
  id: uuid.UUID
