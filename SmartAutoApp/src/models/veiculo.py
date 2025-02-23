from odmantic import Model, Reference

class Veiculo(Model):
    marca: str
    modelo: str
    ano: int
    preco: float
    cor: str
    disponivel: bool
    categorias: list[str] = [] 


# class Veiculo(Veiculo, table=True):
#     venda_id: int | None = Field(default=None, foreign_key="venda.id")
#     categorias: list["Categoria"] = Relationship(link_model=CategoriaVeiculo)
#     venda: "Venda" = Relationship(back_populates="veiculos")
#     locacoes: list["Locacao"] = Relationship(back_populates="veiculo")






