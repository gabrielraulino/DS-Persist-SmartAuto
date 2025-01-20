"""
Autor: Antonio Kleberson
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from http import HTTPStatus
from sqlmodel import Session, select
from database.database import get_session
from models.cliente import Cliente
from models.funcionario import Funcionario
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
    veiculo = session.get(Veiculo, veiculo_id)
    if not veiculo:
        raise HTTPException(status_code=404, detail="Veículo não encontrado")
    
    vendedor = session.get(Funcionario, vendedor_id)
    if not vendedor:
        raise HTTPException(status_code=404, detail="Vendedor não encontrado")
    
    cliente = session.get(Cliente, cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    
    venda = Venda(data=data, valor=veiculo.preco, vendedor_id=vendedor_id, cliente_id=cliente_id, veiculo_id=veiculo_id)
    session.add(venda)
    session.commit()
    session.refresh(venda)
    return venda


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
        raise HTTPException(status_code=404, detail="Nenhuma venda encontrada com o valor especificado")        
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
    vendas = session.exec(select(Venda).where(Venda.data.between(data_inicial, data_final))).all()
    if not vendas:
        raise HTTPException(status_code=404, detail="Nenhuma venda encontrada no período especificado")
    return vendas