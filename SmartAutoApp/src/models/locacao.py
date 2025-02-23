# # Autor: Antonio Kleberson
# from sqlmodel import Relationship, SQLModel, Field
# from datetime import date

# # from typing import TYPE_CHECKING

# # if TYPE_CHECKING:
# #     from models.funcionario import Funcionario
# #     from models.cliente import Cliente
# #     from models.veiculo import Veiculo


# class LocacaoBase(SQLModel):
#     id: int | None = Field(default=None, primary_key=True)
#     data_inicio: date
#     data_fim: date
#     valor_diaria: float


# class Locacao(LocacaoBase, table=True):
#     cliente_id: int = Field(foreign_key="cliente.id")
#     vendedor_id: int = Field(foreign_key="funcionario.id")
#     veiculo_id: int = Field(foreign_key="veiculo.id")
#     vendedor: "Funcionario" = Relationship(back_populates="locacoes")
#     cliente: "Cliente" = Relationship(back_populates="locacoes")
#     veiculo: "Veiculo" = Relationship(back_populates="locacoes")


# class LocacaoComposto(LocacaoBase):
#     vendedor: "Funcionario"
#     cliente: "Cliente"
#     veiculo: "Veiculo"


# from models.cliente import Cliente
# from models.funcionario import Funcionario
# from models.veiculo import Veiculo
