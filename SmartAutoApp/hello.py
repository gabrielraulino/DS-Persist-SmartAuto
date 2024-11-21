import uuid

# from src.model.Vendedor import Vendedor
from src.model.Endereco import Endereco
from src.model.Cliente import Cliente


def main():
    print("Hello from smartautoapp!")


if __name__ == "__main__":
    main()

# vendedor = Vendedor(id=12312456, usuario="vendedor123", senha="senha_segura", nome="João Silva")
# print(vendedor._id)
endereco = Endereco(
    id=uuid.uuid4(),
    uf="CE",
    cidade="Fortaleza",
    logradouro="Rua das Flores",
    numero="123",
)
# admin = Vendedor(id=uuid.uuid4(), usuario="admin123", senha="senha_admin", nome="Admin User")

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
