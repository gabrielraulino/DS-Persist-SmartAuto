from odmantic import Model
from models.categoria import Categoria

class Veiculo(Model):
    marca: str
    modelo: str
    ano: int
    preco: float
    cor: str
    disponivel: bool
    categorias: list[Categoria] = [] 









