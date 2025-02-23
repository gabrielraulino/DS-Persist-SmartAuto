"""
Autor: Antonio Kleberson
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from http import HTTPStatus
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from datetime import date
from bson import ObjectId
from typing import List

router = APIRouter(prefix="/vendas", tags=["Vendas"])

# MongoDB client and database
client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client.smart_auto

class Venda(BaseModel):
    data: date
    valor: float
    vendedor_id: str
    cliente_id: str
    veiculo_id: str

class VendaComplexa(Venda):
    id: str

class Veiculo(BaseModel):
    id: str
    categorias: List[str]
    disponivel: bool
    preco: float

class Cliente(BaseModel):
    id: str

class Funcionario(BaseModel):
    id: str

@router.get("/", response_model=List[VendaComplexa])
async def listar_vendas(
    offset: int = 0,
    limit: int = Query(default=10, le=100),
    ordem: str = "DESC",
):
    ordem = -1 if ordem == "DESC" else 1
    vendas = await db.vendas.find().sort("valor", ordem).skip(offset).limit(limit).to_list(length=limit)
    return vendas

@router.get("/veiculos_venda/", response_model=List[Veiculo])
async def listar_veiculos(
    offset: int = 0,
    limit: int = Query(default=10, le=100),
):
    veiculos = await db.veiculos.find({"categorias": "Venda", "disponivel": True}).skip(offset).limit(limit).to_list(length=limit)
    return veiculos

@router.post("/", response_model=Venda, status_code=HTTPStatus.CREATED)
async def criar_venda(
    vendedor_id: str,
    cliente_id: str,
    veiculo_id: str,
    data: date = date.today(),
):
    veiculo = await db.veiculos.find_one({"_id": ObjectId(veiculo_id), "categorias": "Venda", "disponivel": True})
    if not veiculo:
        raise HTTPException(status_code=404, detail="Veículo não encontrado")

    vendedor = await db.funcionarios.find_one({"_id": ObjectId(vendedor_id)})
    if not vendedor:
        raise HTTPException(status_code=404, detail="Vendedor não encontrado")

    cliente = await db.clientes.find_one({"_id": ObjectId(cliente_id)})
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")

    venda = {
        "data": data,
        "valor": veiculo["preco"],
        "vendedor_id": vendedor_id,
        "cliente_id": cliente_id,
        "veiculo_id": veiculo_id,
    }
    result = await db.vendas.insert_one(venda)
    await db.veiculos.update_one({"_id": ObjectId(veiculo_id)}, {"$set": {"disponivel": False, "venda_id": result.inserted_id}})
    venda["_id"] = str(result.inserted_id)
    return venda

@router.get("/{id}", response_model=Venda)
async def buscar_venda(id: str):
    venda = await db.vendas.find_one({"_id": ObjectId(id)})
    if not venda:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Venda não encontrada.")
    return venda

@router.put("/{id}", response_model=Venda)
async def atualizar_venda(id: str, venda: Venda):
    result = await db.vendas.update_one({"_id": ObjectId(id)}, {"$set": venda.dict(exclude_unset=True)})
    if result.matched_count == 0:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Venda não encontrada.")
    venda = await db.vendas.find_one({"_id": ObjectId(id)})
    return venda

@router.delete("/{id}")
async def remover_venda(id: str):
    result = await db.vendas.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Venda não encontrada.")
    return {"detail": "Venda apagada com sucesso"}

@router.get("/valor_minimo/", response_model=List[Venda])
async def listar_vendas_por_valor_minimo(valor_minimo: float):
    vendas = await db.vendas.find({"valor": {"$gte": valor_minimo}}).to_list(length=100)
    if not vendas:
        raise HTTPException(status_code=404, detail="Nenhuma venda encontrada com o valor especificado")
    return vendas

@router.get("/data/", response_model=List[Venda])
async def listar_vendas_por_data(data_inicial: date, data_final: date):
    vendas = await db.vendas.find({"data": {"$gte": data_inicial, "$lte": data_final}}).to_list(length=100)
    if not vendas:
        raise HTTPException(status_code=404, detail="Nenhuma venda encontrada no período especificado")
    return vendas
