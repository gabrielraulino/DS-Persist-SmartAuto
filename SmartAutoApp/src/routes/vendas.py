"""
Autor: Antonio Kleberson
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from http import HTTPStatus
from sqlalchemy import text
from sqlmodel import Session, select
from database.database import get_session
from models.cliente import Cliente
from models.funcionario import Funcionario
from models.veiculo import Veiculo, Ordem
from models.venda import Venda, VendaComplexa
from datetime import date
from typing import List


router = APIRouter(prefix="/vendas", tags=["Vendas"])


@router.get("/", response_model=list[VendaComplexa])
def listar_vendas(
    offset: int = 0,
    limit: int = Query(default=10, le=100),
    session: Session = Depends(get_session),
    ordem: Ordem = Ordem.DESC,
):
    vendas = session.exec(
        select(Venda)
        .order_by(text(f"venda.valor {ordem.name }"))
        .offset(offset)
        .limit(limit)
    ).all()
    return vendas


@router.post("/", response_model=VendaBase, status_code=HTTPStatus.CREATED)
def criar_venda(
    vendedor_id: int,
    cliente_id: int,
    data: date = date.today(),
    session: Session = Depends(get_session),
):
    veiculo = session.exec(
        select(Veiculo).where(Veiculo.id == veiculo_id and Veiculo.disponivel)
    ).one_or_none()
    if not veiculo:
        raise HTTPException(status_code=404, detail="Veículo não encontrado")

    vendedor = session.exec(
        select(Funcionario).where(Funcionario.id == vendedor_id)
    ).one_or_none()
    if not vendedor:
        raise HTTPException(status_code=404, detail="Vendedor não encontrado")

    cliente = session.exec(
        select(Cliente).where(Cliente.id == cliente_id)
    ).one_or_none()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    venda = Venda(
        data=data,
        valor=veiculo.preco,
        vendedor_id=vendedor_id,
        cliente_id=cliente_id,
        veiculo_id=veiculo_id,
    )
    setattr(veiculo, "disponivel", False)
    session.add(venda)
    session.commit()
    session.refresh(venda)
    return venda


@router.get("/{id}", response_model=VendaBase)
def buscar_venda(id: int, session: Session = Depends(get_session)):
    venda = session.get(VendaBase, id)
    if not venda:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Venda não encontrada."
        )
    return venda.model_dump()


@router.put("/{id}", response_model=VendaBase)
def atualizar_venda(id: int, venda: VendaBase, session: Session = Depends(get_session)):
    db_venda = session.get(VendaBase, id)
    if not db_venda:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Venda não encontrada."
        )
    for key, value in venda.model_dump(exclude_unset=True).items():
        setattr(db_venda, key, value)
    session.add(db_venda)
    session.commit()
    session.refresh(db_venda)
    return db_venda.model_dump()


@router.delete("/{id}")
def remover_venda(id: int, session: Session = Depends(get_session)):
    db_venda = session.get(VendaBase, id)
    if not db_venda:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Venda não encontrada."
        )
    session.delete(db_venda)
    session.commit()
    return {"detail": "Venda apagada com sucesso"}


@router.get("/valor_minimo/", response_model=List[Venda])
def listar_vendas_por_valor_minimo(
    valor_minimo: float,
    session: Session = Depends(get_session),
):
    """
    Retorna todas as vendas com valor maior ou igual ao valor mínimo especificado.
    """
    vendas = session.exec(select(Venda).where(Venda.valor >= valor_minimo)).all()
    if not vendas:
        raise HTTPException(
            status_code=404, detail="Nenhuma venda encontrada com o valor especificado"
        )
    return vendas


@router.get("/data/", response_model=List[Venda])
def listar_vendas_por_data(
    data_inicial: date,
    data_final: date,
    session: Session = Depends(get_session),
):
    """
    Retorna todas as vendas realizadas entre as datas especificadas.
    """
    vendas = session.exec(
        select(Venda).where(Venda.data.between(data_inicial, data_final))
    ).all()
    if not vendas:
        raise HTTPException(
            status_code=404, detail="Nenhuma venda encontrada no período especificado"
        )
    return vendas
