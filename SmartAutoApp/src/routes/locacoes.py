# Autor: Antonio Kleberson
from fastapi import APIRouter, Depends, HTTPException, Query
from http import HTTPStatus
from datetime import date
from models.locacao import Locacao, LocacaoComposto
from models.veiculo import Veiculo
from models.cliente import Cliente
from models.funcionario import Funcionario
from sqlalchemy.orm import Session
from sqlmodel import select
from database.database import get_session


router = APIRouter(prefix="/locacoes", tags=["Locacoes"])
file = "src/storage/locacoes.csv"
campos = [
    "id",
    "data_inicio",
    "data_fim",
    "valor_diaria",
    "cliente_id",
    "vendedor_id",
    "veiculo_id",
]


@router.get("/", response_model=list[LocacaoComposto])
def listar(
    offset: int = 0,
    limit: int = Query(default=10, le=100),
    session: Session = Depends(get_session),
):
    return session.execute(select(Locacao).offset(offset=offset).limit(limit)).all()


@router.post("/", response_model=Locacao, status_code=HTTPStatus.CREATED)
def criar(
    locacao: Locacao,
    session: Session = Depends(get_session),
):
    veiculo = session.execute(
        select(Veiculo).where(
            Veiculo == locacao.veiculo_id
            and Veiculo.disponivel
            and Veiculo.categorias.any(nome="Locação")
        )
    ).one_or_none()
    if not veiculo:
        raise HTTPException(status_code=404, detail="Veículo não encontrado")
    vendedor = session.execute(
        select(Funcionario).where(Funcionario.id == locacao.vendedor_id)
    ).one_or_none()
    if not vendedor:
        raise HTTPException(status_code=404, detail="Funcionario não encontrado")
    cliente = session.execute(select(Cliente).where(Cliente.id == locacao.cliente_id))
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    session.add(locacao)
    session.commit()
    session.refresh(locacao)
    setattr(veiculo, "disponivel", False)
    return locacao


@router.get("/{id}", response_model=Locacao)
def buscar_por_id():
    pass


@router.put("/{id}", response_model=Locacao)
def atualizar():
    pass


@router.delete("/{id}")
def remover():
    pass
