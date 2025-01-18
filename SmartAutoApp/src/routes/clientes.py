"""
Autor : Gabriel Raulino
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from sqlmodel import Session, select
from models.cliente import Cliente
from database.database import get_session

router = APIRouter(prefix="/clientes", tags=["Clientes"])
campos = ["id", "nome", "telefone", "email", "endereco"]
file = "src/storage/clientes.csv"


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


@router.post("/", response_model=Cliente)
def create_cliente(cliente: Cliente, session: Session = Depends(get_session)):
    session.add(cliente)
    session.commit()
    session.refresh(cliente)
    return cliente


@router.put("/{cliente_id}", response_model=Cliente)
def update_cliente(
    cliente_id: int, cliente: Cliente, session: Session = Depends(get_session)
):
    db_cliente = session.get(Cliente, cliente_id)
    if not db_cliente:
        raise HTTPException(status_code=404, detail="Cliente not found")
    for key, value in cliente.model_dump(exclude_unset=True).items():
        setattr(db_cliente, key, value)
    session.add(db_cliente)
    session.commit()
    session.refresh(db_cliente)
    return db_cliente


@router.delete("/{cliente_id}")
def delete_cliente(cliente_id: int, session: Session = Depends(get_session)):
    cliente = session.get(Cliente, cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente not found")
    session.delete(cliente)
    session.commit()
    return {"ok": True}
