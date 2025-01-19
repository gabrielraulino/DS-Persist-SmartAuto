"""
Autor: Antonio Kleberson
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from http import HTTPStatus
from sqlmodel import Session, select
from database.database import get_session
from models.venda import Venda
from models.veiculo import Veiculo
from datetime import date
from typing import List

router = APIRouter(prefix="/vendas", tags=["Vendas"])


@router.get("/", response_model=List[Venda])
def listar_vendas(
    offset: int = 0,
    limit: int = Query(default=10, le=100),
    session: Session = Depends(get_session),
):
    return session.exec(select(Venda).offset(offset).limit(limit)).all()


@router.post("/", response_model=Venda, status_code=HTTPStatus.CREATED)
def criar_venda(
    veiculo_id: int,
    vendedor_id: int,
    cliente_id: int,
    data: date = date.today(),
    session: Session = Depends(get_session),
):
    veiculo = session.exec(select(Veiculo).where(Veiculo.disponivel and Veiculo.id == veiculo_id)).one()
    if not veiculo: 
          raise HTTPException(status_code=404, detail="Veículo não encontrado")
    setattr(veiculo, "disponivel", False)
    nova_venda = Venda(
    valor= veiculo.preco,
    vendedor_id= vendedor_id,
    cliente_id= cliente_id,
    veiculo_id= veiculo_id,
    data= data)
    session.add(nova_venda)
    session.commit()
    session.refresh(nova_venda)
    return nova_venda.model_dump()


@router.get("/{id}", response_model=Venda)
def buscar_venda(id: int, session: Session = Depends(get_session)):
    venda = session.get(Venda, id)
    if not venda:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Venda não encontrada."
        )
    return venda.model_dump()


@router.put("/{id}", response_model=Venda)
def atualizar_venda(id: int, venda: Venda, session: Session = Depends(get_session)):
    db_venda = session.get(Venda, id)
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
    db_venda = session.get(Venda, id)
    if not db_venda:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Venda não encontrada."
        )
    session.delete(db_venda)
    session.commit()
    return {"detail": "Venda apagada com sucesso"}
