"""
Autor : Gabriel Raulino
"""

from http import HTTPStatus
from fastapi import APIRouter, HTTPException
import uuid
from models.cliente.cliente import Cliente
from utils.file_handler import read_csv, append_csv
from utils.zip_handler import compactar_csv
from utils.hash_handler import calcular_hash_sha256

clientes_router = APIRouter(prefix="/clientes", tags=["Clientes"])
campos = ["id", "nome", "telefone", "email", "endereco"]
file = "src/storage/clientes.csv"
clientes_data = read_csv(file)


@clientes_router.get("/zip")
def gerar_zip():
    return compactar_csv(file)


@clientes_router.get("/hash")
def gerar_hash():
    return {calcular_hash_sha256(file)}


@clientes_router.get("/qtd")
def contar_elementos():
    return {"quantidade de clientes no csv": len(clientes_data)}


@clientes_router.get("/", status_code=HTTPStatus.OK)
def listar():
    if clientes_data.empty:
        return []
    return clientes_data.to_dict(orient="records")


@clientes_router.get("/{id}", response_model=Cliente)
def buscar_funcionario(id: str):
    global clientes_data
    cliente = clientes_data[clientes_data["id"] == id]
    if cliente.empty:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Cliente não encontrado."
        )
    return cliente.to_dict(orient="records")[0]


@clientes_router.post("/", response_model=Cliente, status_code=HTTPStatus.CREATED)
def inserir(cliente: Cliente):
    global clientes_data
    if cliente.id is None:
        cliente.id = uuid.uuid4()
    elif not clientes_data[clientes_data["id"] == cliente.id].empty:
        raise HTTPException(status_code=400, detail="ID já existe.")
    cliente_validado = Cliente.model_validate(cliente)
    clientes_data = append_csv(
        file, campos, cliente_validado.model_dump(), clientes_data
    )
    if cliente.endereco.id == None:
        cliente.endereco.id = uuid.uuid4()
    return cliente_validado


@clientes_router.put("/{id}", response_model=Cliente)
def atualizar(id: str, cliente: Cliente):
    global clientes_data
    elemento = clientes_data[clientes_data["id"] == id]
    if elemento.empty:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Cliente não encontrado."
        )
    if cliente.id is None:
        cliente.id = id
    cliente_validado = Cliente.model_validate(cliente)
    clientes_data.loc[elemento.index[0]] = cliente_validado.model_dump()
    clientes_data.to_csv(file, index=False)
    return cliente_validado


@clientes_router.delete("/{id}")
def excluir(id: str):
    global clientes_data
    elemento = clientes_data[clientes_data["id"] == id]
    if elemento.empty:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Cliente não encontrado."
        )
    clientes_data = clientes_data.drop(elemento.index[0])
    clientes_data.to_csv(file, index=False)
    return {"detail": "Cliente excluído com sucesso"}
