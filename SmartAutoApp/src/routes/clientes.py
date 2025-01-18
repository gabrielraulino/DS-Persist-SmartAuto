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


@clientes_router.put("/{id}", response_model=Cliente)
def atualizar(id: uuid.UUID, cliente: Cliente):
    global clientes_data
    elemento = clientes_data[clientes_data["id"] == str(id)]
    if elemento.empty:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Cliente não encontrado."
        )
    if cliente.id is None:
        cliente.id = id
    cliente_validado = Cliente.model_validate(cliente)
    clientes_data.loc[elemento.index[0]] = cliente_validado.model_dump()
    clientes_data.to_csv(file, index=False)
    return cliente_validado


@clientes_router.delete("/{id}")
def excluir(id: uuid.UUID):
    global clientes_data
    elemento = clientes_data[clientes_data["id"] == id]
    if elemento.empty:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Cliente não encontrado."
        )
    clientes_data = clientes_data.drop(elemento.index[0])
    clientes_data.to_csv(file, index=False)
    return {"detail": "Cliente excluído com sucesso"}
