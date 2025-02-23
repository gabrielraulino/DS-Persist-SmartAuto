# # Autor: Gabriel Raulino
# from typing import TYPE_CHECKING
# from sqlmodel import SQLModel, Field, Relationship
# from datetime import date

# if TYPE_CHECKING:
#     from .cliente import Cliente
#     from .funcionario import Funcionario
#     from .veiculo import Veiculo


# class VendaBase(SQLModel):
#     id: int = Field(default=None, primary_key=True)
#     data: date | None = None
#     valor: float


# class Venda(VendaBase, table=True):
#     vendedor_id: int = Field(foreign_key="funcionario.id")
#     cliente_id: int = Field(foreign_key="cliente.id")
#     vendedor: "Funcionario" = Relationship(back_populates="vendas")
#     cliente: "Cliente" = Relationship(back_populates="vendas")
#     veiculos: list["Veiculo"] = Relationship(back_populates="venda")


# class VendaComplexa(VendaBase):
#     vendedor: "Funcionario"
#     cliente: "Cliente"
#     veiculos: list["Veiculo"]


# from .cliente import Cliente
# from .funcionario import Funcionario
# from .veiculo import Veiculo
