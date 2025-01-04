from fastapi import APIRouter, HTTPException
from http import HTTPStatus
import uuid
from models.funcionario import Funcionario
from utils.file_handler import read_csv, append_csv
from utils.zip_handler import compactar_csv
from utils.hash_handler import calcular_hash_sha256

funcionarios_router = APIRouter(prefix="/funcionarios", tags=["Funcionarios"])
file = "src/storage/funcionarios.csv"
campos = ["id", "usuario", "senha", "nome", "telefone", "funcao"]

funcionarios_data = read_csv(file)  # Carrega os dados do arquivo CSV


@funcionarios_router.get("/zip")
def gerar_zip():
    return compactar_csv(file)


@funcionarios_router.get("/hash")
def gerar_hash():
    return {calcular_hash_sha256(file)}


@funcionarios_router.get("/qtd")
def contar_elementos():
    return {"quantidade de funcionários no csv": len(funcionarios_data)}


@funcionarios_router.get("/")
def listar_funcionarios():
    if funcionarios_data.empty:
        return {"msg": "lista vazia"}
    return funcionarios_data.to_dict(orient="records")


@funcionarios_router.get("/{id}", response_model=Funcionario)
def buscar_funcionario(id: str):
    global funcionarios_data
    funcionario = funcionarios_data[funcionarios_data["id"] == id]
    if funcionario.empty:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Funcionário não encontrado."
        )
    return funcionario.to_dict(orient="records")[0]


@funcionarios_router.post(
    "/", response_model=Funcionario, status_code=HTTPStatus.CREATED
)
def criar_funcionario(funcionario: Funcionario):
    global funcionarios_data
    if funcionario.id is None:
        funcionario.id = uuid.uuid4()
    elif funcionarios_data[funcionarios_data["id"] == funcionario.id].empty:
        raise HTTPException(status_code=400, detail="ID já existe.")
    funcionario_validado = Funcionario.model_validate(funcionario)
    funcionarios_data = append_csv(
        file, campos, funcionario_validado.model_dump(), funcionarios_data
    )
    return funcionario_validado


@funcionarios_router.put("/{id}", response_model=Funcionario)
def atualizar_funcionario(id: str, funcionario: Funcionario):
    global funcionarios_data
    elemento = funcionarios_data[funcionarios_data["id"] == id]
    if elemento.empty:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Funcionário não encontrado."
        )
    if funcionario.id is None:
        funcionario.id = id
    funcionario_validado = Funcionario.model_validate(funcionario)
    funcionarios_data.loc[elemento.index[0]] = funcionario_validado.model_dump()
    funcionarios_data.to_csv(file, index=False)
    return funcionario_validado


@funcionarios_router.delete("/{id}")
def remover_funcionario(id: str):
    global funcionarios_data
    elemento = funcionarios_data[funcionarios_data["id"] == id]
    if elemento.empty:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Funcionário não encontrado."
        )
    index = elemento.index[0]
    funcionarios_data = funcionarios_data.drop(index)
    funcionarios_data.to_csv(file, index=False)
    return {"detail": "Funcionário excluído com sucesso"}
