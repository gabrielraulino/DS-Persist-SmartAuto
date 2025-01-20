"""
Autor : Gabriel Raulino, Antonio Kleberson
"""

from typing import TYPE_CHECKING
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlmodel import Session, select
from models.cliente import Cliente
from database.database import get_session

if TYPE_CHECKING:
    from models.venda import Venda

router = APIRouter(prefix="/clientes", tags=["Clientes"])
campos = ["id", "nome", "telefone", "email", "endereco"]
file = "src/storage/clientes.csv"


@router.post("/", response_model=Cliente)
def create_cliente(
    nome: str,
    telefone: str,
    email: str,
    uf: str,
    cidade: str,
    logradouro: str,
    numero: int,
    session: Session = Depends(get_session),
):
    cliente = Cliente(
        nome=nome,
        telefone=telefone,
        email=email,
        uf=uf,
        cidade=cidade,
        logradouro=logradouro,
        numero=numero,
    )
    session.add(cliente)
    session.commit()
    session.refresh(cliente)
    return cliente


@router.get("/", response_model=list[Cliente])
def listar_clientes(
    offset: int = 0,
    limit: int = Query(default=10, le=100),
    session: Session = Depends(get_session),
):
    return session.exec(select(Cliente).offset(offset).limit(limit)).all()


@router.get("/{cliente_id}", response_model=Cliente)
def read_cliente(cliente_id: int, session: Session = Depends(get_session)):
    cliente = session.get(Cliente, cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente not found")
    return cliente


@router.put("/{id}", response_model=Cliente)
def update_cliente(
    cliente_id: int,
    nome: str,
    telefone: str,
    email: str,
    uf: str,
    cidade: str,
    logradouro: str,
    numero: int,
    session: Session = Depends(get_session),
):
    db_cliente = session.get(Cliente, cliente_id)
    if not db_cliente:
        raise HTTPException(status_code=404, detail="Cliente not found")
    cliente = Cliente(
        nome=nome,
        telefone=telefone,
        email=email,
        uf=uf,
        cidade=cidade,
        logradouro=logradouro,
        numero=numero,
    )
    for key, value in cliente.model_dump(exclude_unset=True).items():
        setattr(db_cliente, key, value)
    session.add(db_cliente)
    session.commit()
    session.refresh(db_cliente)
    return db_cliente


@router.delete("/{id}")
def delete_cliente(cliente_id: int, session: Session = Depends(get_session)):
    cliente = session.get(Cliente, cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente not found")
    session.delete(cliente)
    session.commit()
    return {"ok": True}


@router.get("/{cliente_id}/vendas")
def listar_vendas_cliente(cliente_id: int, session: Session = Depends(get_session)):
    cliente = session.get(Cliente, cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente not found")
        
    vendas = session.exec(select(Venda).where(Venda.cliente_id == cliente_id)).all()
    return vendas