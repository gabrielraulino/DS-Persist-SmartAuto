from fastapi import APIRouter, Depends, HTTPException, Query
from http import HTTPStatus
from datetime import date, datetime

from odmantic import AIOEngine, ObjectId
from models.locacao import Locacao
from models.veiculo import Veiculo
from models.cliente import Cliente
from models.funcionario import Funcionario
from database.mongo import get_engine


router = APIRouter(prefix="/locacoes", tags=["Locacoes"])

engine = get_engine()
@router.get("/", response_model=list[Locacao])
async def listar(
    offset: int = 0,
    limit: int = Query(default=10, le=100),
):

    return await engine.find(Locacao, skip=offset, limit=limit) 


@router.post("/", response_model=Locacao, status_code=HTTPStatus.CREATED)
async def criar(
    locacao: Locacao,
    engine: AIOEngine = Depends(get_engine)
):
    veiculo = await engine.find_one(Veiculo, Veiculo.id == ObjectId(locacao.veiculo.id) and Veiculo.disponivel == True)
    if not veiculo:
        raise HTTPException(HTTPStatus.NOT_FOUND, detail="Veículo não disponível")
    cliente = await engine.find_one(Cliente, Cliente.id == ObjectId(locacao.cliente.id))
    if not cliente:
        raise HTTPException(HTTPStatus.NOT_FOUND, detail="Cliente não encontrado")
    vendedor = await engine.find_one(Funcionario, Funcionario.id == ObjectId(locacao.vendedor.id))
    if not vendedor:
        raise HTTPException(HTTPStatus.NOT_FOUND, detail="Vendedor não encontrado")
    if not locacao.data_inicio:
        locacao.data_inicio = date.today()
    veiculo.disponivel = False
    locacao.veiculo = veiculo
    locacao.cliente = cliente
    locacao.vendedor = vendedor
    locacao.valor_diaria = veiculo.preco * .15
    await engine.save(veiculo)
    await engine.save(locacao)
    return locacao


# @router.get("/{id}", response_model=Locacao)
# def buscar_por_id():
#     pass


# @router.put("/{id}", response_model=Locacao)
# def atualizar():
#     pass


# @router.delete("/{id}")
# def remover():
#     pass
