from fastapi import APIRouter, HTTPException
from http import HTTPStatus
import uuid
from models.funcionario import Funcionario
from utils.file_handler import read_csv, append_csv
from utils.zip_handler import compactar_csv
from utils.hash_handler import calcular_hash_sha256
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlmodel import Session, select
from models.funcionario import Funcionario
from database.database import get_session

router = APIRouter(prefix="/funcionarios", tags=["Funcionarios"])
file = "src/storage/funcionarios.csv"
campos = ["id", "usuario", "senha", "nome", "telefone", "funcao"]

funcionarios_data = read_csv(file)  # Carrega os dados do arquivo CSV


# @router.get("/zip")
# def gerar_zip():
#     return compactar_csv(file)


# @router.get("/hash")
# def gerar_hash():
#     return {calcular_hash_sha256(file)}


# @router.get("/qtd")
# def contar_elementos():
#     return {"quantidade de funcionários no csv": len(funcionarios_data)}


@router.get("/", response_model=list[Funcionario])
def listar_funcionarios(
    offset: int = 0,
    limit: int = Query(default=10, le=100),
    session: Session = Depends(get_session),
):
    return session.exec(select(Funcionario).offset(offset).limit(limit)).all()


@router.get("/{funcionario_id}", response_model=Funcionario)
def read_user(user_id: int, session: Session = Depends(get_session)):
    funcionario = session.get(Funcionario, user_id)
    if not funcionario:
        raise HTTPException(status_code=404, detail="Funcionario not found")
    return funcionario


@router.post("/", response_model=Funcionario)
def create_user(funcionario: Funcionario, session: Session = Depends(get_session)):
    session.add(funcionario)
    session.commit()
    session.refresh(funcionario)
    return funcionario


@router.put("/{funcionario_id}", response_model=Funcionario)
def update_user(
    funcionario_id: int, user: Funcionario, session: Session = Depends(get_session)
):
    db_funcionario = session.get(Funcionario, funcionario_id)
    if not db_funcionario:
        raise HTTPException(status_code=404, detail="User not found")
    for key, value in user.dict(exclude_unset=True).items():
        setattr(db_funcionario, key, value)
    session.add(db_funcionario)
    session.commit()
    session.refresh(db_funcionario)
    return db_funcionario


@router.delete("/{funcionario_id}")
def delete_user(funcionario_id: int, session: Session = Depends(get_session)):
    func = session.get(Funcionario, funcionario_id)
    if not func:
        raise HTTPException(status_code=404, detail="Funcionario not found")
    session.delete(func)
    session.commit()
    return {"ok": True}
