from typing import TYPE_CHECKING, List
from fastapi import APIRouter, HTTPException, Depends, Query
from odmantic import AIOEngine, ObjectId
from models.cliente import Cliente
from database.mongo import get_engine
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
    # Converter a string para ObjectId para a consulta correta
    cliente = await engine.find_one(Cliente, Cliente.id == ObjectId(cliente_id))
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
    # Converter a string para ObjectId para a consulta correta
    cliente = await engine.find_one(Cliente, Cliente.id == ObjectId(cliente_id))
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
    # Converter a string para ObjectId para a consulta correta
    cliente = await engine.find_one(Cliente, Cliente.id == ObjectId(cliente_id))
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente not found")
    await engine.delete(cliente)
    return {"ok": True}


@router.get("/{cliente_id}/vendas", response_model=List[Venda])
async def listar_vendas_cliente(cliente_id: str, engine: AIOEngine = Depends(get_engine)):
    # Converter a string para ObjectId para localizar o cliente
    cliente = await engine.find_one(Cliente, Cliente.id == ObjectId(cliente_id))
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente not found")
    # Converter também para ObjectId, se o campo cliente_id em Venda for armazenado como ObjectId
    vendas = await engine.find(Venda, Venda.cliente_id == ObjectId(cliente_id))
    return vendas


@router.get("/vendas/periodo", response_model=List[dict])
async def clientes_vendas_periodo(
    start_date: str,  # Formato esperado: ISO (ex.: "2023-01-01T00:00:00")
    end_date: str,    # Formato esperado: ISO (ex.: "2023-01-31T23:59:59")
    engine: AIOEngine = Depends(get_engine)
):
    pipeline = [
        {
            "$match": {
                "data": {"$gte": start_date, "$lte": end_date}
            }
        },
        {
            "$group": {
                "_id": "$cliente_id",
                "totalVendas": {"$sum": "$valor"},
                "numVendas": {"$sum": 1},
                "mediaVendas": {"$avg": "$valor"}
            }
        },
        {
            "$lookup": {
                "from": "cliente",             # Nome da coleção de clientes; verifique se corresponde à sua configuração
                "localField": "_id",
                "foreignField": "_id",
                "as": "cliente_info"
            }
        },
        {
            "$unwind": "$cliente_info"
        }
    ]
    stats_cursor = engine.aggregate(Venda, pipeline)
    resultados = [doc async for doc in stats_cursor]
    if not resultados:
        raise HTTPException(status_code=404, detail="Nenhum cliente com vendas no período especificado")
    return resultados
