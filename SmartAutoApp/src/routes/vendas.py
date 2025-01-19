"""
Autor: Antonio Kleberson
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from http import HTTPStatus
from sqlmodel import Session, select
from database.database import get_session
from models.venda import VendaBase, Venda
from models.veiculo import Veiculo
from datetime import date
from typing import List

router = APIRouter(prefix="/vendas", tags=["Vendas"])


@router.get("/", response_model=List[VendaBase])
def listar_vendas(
    offset: int = 0,
    limit: int = Query(default=10, le=100),
    session: Session = Depends(get_session),
):
    return session.exec(select(VendaBase).offset(offset).limit(limit)).all()


@router.post("/", response_model=VendaBase, status_code=HTTPStatus.CREATED)
def criar_venda(
    vendedor_id: int,
    cliente_id: int,
    data: date = date.today(),
    session: Session = Depends(get_session),
):
    
    nova_venda = VendaBase(
    valor= 0,
    vendedor_id= vendedor_id,
    cliente_id= cliente_id,
    data= data)
    session.add(nova_venda)
    session.commit()
    session.refresh(nova_venda)
    return nova_venda.model_dump()


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
