import uuid
import Vendedor
# import Endereco

class Gerente(Vendedor):
    # def __init__(self, id: uuid.UUID, usuario: str, senha: str, nome: str, endereco: Endereco):
    #     super().__init__(id, usuario, senha, nome, endereco)

    def __init__(self, id: uuid.UUID, usuario: str, senha: str, nome: str):
        super().__init__(id, usuario, senha, nome)

    def inserir_vendedor(self, vendedor: Vendedor) -> None:
        # Lógica para inserir um novo vendedor (ex: salvar em um arquivo CSV)
        print(f"Vendedor {vendedor._nome} inserido pelo Gerente {self._nome}")

# Exemplo de uso da classe
if __name__ == "__main__":
    gerente_id = uuid.uuid4()
    gerente = Gerente(id=gerente_id, usuario="gerente123", senha="senha_segura", nome="Maria Oliveira")
    vendedor_id = uuid.uuid4()
    vendedor = Vendedor(id=vendedor_id, usuario="vendedor123", senha="senha_segura", nome="João Silva")
    gerente.inserir_vendedor(vendedor)
