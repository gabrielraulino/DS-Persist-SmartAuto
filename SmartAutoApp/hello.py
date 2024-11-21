import uuid
# from src.model.Vendedor import Vendedor
from src.model.Endereco import Endereco
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
        numero="123"
    )
# admin = Vendedor(id=uuid.uuid4(), usuario="admin123", senha="senha_admin", nome="Admin User")

# print(admin)

print(endereco)