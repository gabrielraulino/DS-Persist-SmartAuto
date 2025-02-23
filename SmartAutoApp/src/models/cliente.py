from odmantic import Model

class Cliente(Model):
    nome: str
    telefone: str
    email: str
    uf: str
    cidade: str
    logradouro: str
    numero: int

