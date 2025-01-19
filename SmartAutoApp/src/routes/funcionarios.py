from fastapi import APIRouter, HTTPException
from http import HTTPStatus
from models.funcionario import Funcionario, Role
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlmodel import Session, select
from sqlalchemy.orm import joinedload
from models.funcionario import Funcionario
from database.database import get_session

router = APIRouter(prefix="/funcionarios", tags=["Funcionarios"])
file = "src/storage/funcionarios.csv"
# campos = ["id", "usuario", "senha", "nome", "telefone", "funcao"]


@router.post("/", response_model=Funcionario)
def create(
    nome: str,
    usuario: str,
    senha: str,
    telefone: str,
    funcao: Role,
    session: Session = Depends(get_session),
):
    funcionario = Funcionario(
        usuario=usuario, senha=senha, nome=nome, telefone=telefone, funcao=funcao
    )
    session.add(funcionario)
    session.commit()
    session.refresh(funcionario)
    return funcionario.model_dump()


@router.get("/", response_model=list[Funcionario])
def listar(
    offset: int = 0,
    limit: int = Query(default=10, le=100),
    session: Session = Depends(get_session),
):
    return session.exec(select(Funcionario).offset(offset).limit(limit)).all()


@router.get("/{id}", response_model=list[Funcionario])
def read(user_id: int, session: Session = Depends(get_session)):
    funcionario = session.get(Funcionario, user_id)
    if not funcionario:
        raise HTTPException(status_code=404, detail="Funcionario not found")
    return funcionario.model_dump()


@router.get("/{nome}", response_model=list[Funcionario])
def search_by_name(nome: str, session: Session = Depends(get_session)):
    funcionarios = session.exec(
        select(Funcionario).where(Funcionario.nome.like(f"%{nome}%"))
    ).all()
    if not funcionarios:
        raise HTTPException(status_code=404, detail="Funcionario not found")
    return funcionarios


@router.get("/role/{funcao}", response_model=list[Funcionario])
def search_by_role(funcao: Role, session: Session = Depends(get_session)):
    funcionarios = session.exec(
        select(Funcionario).where(Funcionario.funcao == funcao)
    ).all()
    if not funcionarios:
        raise HTTPException(status_code=404, detail="Funcionario not found")
    return funcionarios


@router.put("/{id}", response_model=Funcionario)
def update(
    funcionario_id: int,
    nome: str,
    usuario: str,
    senha: str,
    telefone: str,
    funcao: Role,
    session: Session = Depends(get_session),
):
    db_funcionario = session.get(Funcionario, funcionario_id)
    if not db_funcionario:
        raise HTTPException(status_code=404, detail="Funcionario not found")
    funcionario = Funcionario(
        usuario=usuario, senha=senha, nome=nome, telefone=telefone, funcao=funcao
    )
    for key, value in funcionario.model_dump(exclude_unset=True).items():
        setattr(db_funcionario, key, value)
    session.add(db_funcionario)
    session.commit()
    session.refresh(db_funcionario)
    return db_funcionario.model_dump()


@router.delete("/{id}")
def delete(funcionario_id: int, session: Session = Depends(get_session)):
    func = session.get(Funcionario, funcionario_id)
    if not func:
        raise HTTPException(status_code=404, detail="Funcionario not found")
    session.delete(func)
    session.commit()
    return {"ok": True}
