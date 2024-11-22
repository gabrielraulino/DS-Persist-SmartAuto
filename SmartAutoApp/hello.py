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


print(endereco)
print(cliente)
