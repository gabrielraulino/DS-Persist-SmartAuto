import uuid

# from src.model.Vendedor import Vendedor
from src.models.endereco import Endereco
from src.models.cliente import Cliente
import pandas as pd

cliente_csv = "./src/storage/clientes.csv"


def main():
    print("Hello from smartautoapp!")


if __name__ == "__main__":
    main()

try:
    df = pd.read_csv(cliente_csv)
except Exception as e:
    df = pd.DataFrame()
endereco = Endereco(
    id=uuid.uuid4(),
    uf="CE",
    cidade="Fortaleza",
    logradouro="Rua das Flores",
    numero="123",
)

# print(admin)
cliente = Cliente(
    id=uuid.uuid4(),
    nome="Gabriel Souza",
    email="gabriel.souza@example.com",
    telefone="123456789",
    endereco=endereco,
)
clientes_df = pd.DataFrame(columns=["id", "nome", "telefone", "email", "endereco"])
novo_cliente = pd.DataFrame(
    [
        {
            "id": cliente.id,
            "nome": cliente.nome,
            "telefone": cliente.telefone,
            "email": cliente.email,
            "endereco": f"{cliente.endereco.logradouro}, {cliente.endereco.numero}, {cliente.endereco.cidade} - {cliente.endereco.uf}",
        }
    ]
)
# clientes_df.append(cliente)
clientes_df = pd.concat([clientes_df, novo_cliente])
# df.to_csv(cliente_csv)
print(clientes_df)
# print(endereco)
# print(cliente)
