"""
Autor : Gabriel Raulino, Antonio Kleberson
"""

from typing import TYPE_CHECKING, List
from fastapi import APIRouter, HTTPException, Depends, Query
from odmantic import AIOEngine
from models.cliente import Cliente
from database.mongo import get_engine
from models.venda import Venda

if TYPE_CHECKING:
    from models.venda import Venda

router = APIRouter(prefix="/clientes", tags=["Clientes"])


@router.post("/", response_model=Cliente)
async def create_cliente(
    nome: str,
    telefone: str,
    email: str,
    uf: str,
    cidade: str,
    logradouro: str,
    numero: int,
    engine: AIOEngine = Depends(get_engine),
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
    await engine.save(cliente)
    return cliente


@router.get("/", response_model=List[Cliente])
async def listar_clientes(
    offset: int = 0,
    limit: int = Query(default=10, le=100),
    engine: AIOEngine = Depends(get_engine),
):
    clientes = await engine.find(Cliente, skip=offset, limit=limit)
    return clientes


@router.get("/{cliente_id}", response_model=Cliente)
async def read_cliente(cliente_id: str, engine: AIOEngine = Depends(get_engine)):
    cliente = await engine.find_one(Cliente, Cliente.id == cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente not found")
    return cliente


@router.put("/{cliente_id}", response_model=Cliente)
async def update_cliente(
    cliente_id: str,
    nome: str,
    telefone: str,
    email: str,
    uf: str,
    cidade: str,
    logradouro: str,
    numero: int,
    engine: AIOEngine = Depends(get_engine),
):
    cliente = await engine.find_one(Cliente, Cliente.id == cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente not found")
    cliente.nome = nome
    cliente.telefone = telefone
    cliente.email = email
    cliente.uf = uf
    cliente.cidade = cidade
    cliente.logradouro = logradouro
    cliente.numero = numero
    await engine.save(cliente)
    return cliente


@router.delete("/{cliente_id}")
async def delete_cliente(cliente_id: str, engine: AIOEngine = Depends(get_engine)):
    cliente = await engine.find_one(Cliente, Cliente.id == cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente not found")
    await engine.delete(cliente)
    return {"ok": True}


@router.get("/{cliente_id}/vendas", response_model=List[Venda])
async def listar_vendas_cliente(cliente_id: str, engine: AIOEngine = Depends(get_engine)):
    cliente = await engine.find_one(Cliente, Cliente.id == cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente not found")
    vendas = await engine.find(Venda, Venda.cliente_id == cliente_id)
    return vendas
