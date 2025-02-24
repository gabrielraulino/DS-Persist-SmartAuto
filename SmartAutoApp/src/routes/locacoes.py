from fastapi import APIRouter, HTTPException, Query
from http import HTTPStatus
from datetime import date, datetime

from odmantic import ObjectId
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
    vencidas: bool = False
):
    if vencidas:
      return await engine.find(Locacao, Locacao.data_fim < datetime.now() ,skip=offset, limit=limit) 
    
    return await engine.find(Locacao, Locacao.data_fim > datetime.now() ,skip=offset, limit=limit) 
    

# @router.post("/", response_model=Locacao, status_code=HTTPStatus.CREATED)
# async def criar(
#     locacao: Locacao
# ):
#     veiculo = await engine.find_one(Veiculo, Veiculo.id == ObjectId(locacao.veiculo.id) and Veiculo.disponivel == True)
#     if not veiculo:
#         raise HTTPException(HTTPStatus.NOT_FOUND, detail="Veículo não disponível")
#     cliente = await engine.find_one(Cliente, Cliente.id == ObjectId(locacao.cliente.id))
#     if not cliente:
#         raise HTTPException(HTTPStatus.NOT_FOUND, detail="Cliente não encontrado")
#     vendedor = await engine.find_one(Funcionario, Funcionario.id == ObjectId(locacao.vendedor.id))
#     if not vendedor:
#         raise HTTPException(HTTPStatus.NOT_FOUND, detail="Vendedor não encontrado")
#     if not locacao.data_inicio:
#         locacao.data_inicio = date.today()
#     veiculo.disponivel = False
#     locacao.veiculo = veiculo
#     locacao.cliente = cliente
#     locacao.vendedor = vendedor
#     locacao.valor_diaria = veiculo.preco * .01
#     await engine.save(veiculo)
#     await engine.save(locacao)
#     return locacao

@router.post("/", response_model=Locacao, status_code=HTTPStatus.CREATED)
async def criar(
    veiculo_id: ObjectId,
    cliente_id: ObjectId,
    vendedor_id: ObjectId,
    data_fim: datetime,
    data_inicio: datetime = datetime.today(),

):
    veiculo = await engine.find_one(Veiculo, Veiculo.id == veiculo_id and Veiculo.disponivel == True)
    if not veiculo:
        raise HTTPException(HTTPStatus.NOT_FOUND, detail="Veículo não disponível")
    cliente = await engine.find_one(Cliente, Cliente.id == cliente_id)
    if not cliente:
        raise HTTPException(HTTPStatus.NOT_FOUND, detail="Cliente não encontrado")
    vendedor = await engine.find_one(Funcionario, Funcionario.id == vendedor_id)
    if not vendedor:
        raise HTTPException(HTTPStatus.NOT_FOUND, detail="Vendedor não encontrado")
    locacao = Locacao(
      veiculo=veiculo, 
      cliente=cliente, 
      vendedor=vendedor,
      data_inicio=data_inicio, 
      data_fim=data_fim,
      valor_diaria= veiculo.preco * .01,
       )
    await engine.save(veiculo)
    await engine.save(locacao)
    return locacao


@router.get("/{id}", response_model=Locacao)
async def buscar_por_id(id: ObjectId):
    locacao = await engine.find_one(Locacao, Locacao.id == id)
    if not locacao:
        raise HTTPException(HTTPStatus.NOT_FOUND, detail="Locação não encontrada!")
    return locacao


@router.put("/{id}", response_model=Locacao)
async def atualizar(
  id: ObjectId,
  locacao_atualizada: Locacao,
):
  locacao = await engine.find_one(Locacao, Locacao.id == id)
  if not locacao:
    raise HTTPException(HTTPStatus.NOT_FOUND, detail="Locação não encontrada!")

  veiculo = await engine.find_one(Veiculo, Veiculo.id == ObjectId(locacao_atualizada.veiculo.id) and Veiculo.disponivel == True)
  if not veiculo:
    raise HTTPException(HTTPStatus.NOT_FOUND, detail="Veículo não disponível")
  cliente = await engine.find_one(Cliente, Cliente.id == ObjectId(locacao_atualizada.cliente.id))
  if not cliente:
    raise HTTPException(HTTPStatus.NOT_FOUND, detail="Cliente não encontrado")
  vendedor = await engine.find_one(Funcionario, Funcionario.id == ObjectId(locacao_atualizada.vendedor.id))
  if not vendedor:
    raise HTTPException(HTTPStatus.NOT_FOUND, detail="Vendedor não encontrado")

  locacao.veiculo = veiculo
  locacao.cliente = cliente
  locacao.vendedor = vendedor
  locacao.data_inicio = locacao_atualizada.data_inicio or locacao.data_inicio
  locacao.data_fim = locacao_atualizada.data_fim or locacao.data_fim
  locacao.valor_diaria = veiculo.preco * .01

  await engine.save(locacao)
  return locacao


@router.delete("/{id}")
async def remover(
  id: ObjectId,
):
  locacao = await engine.find_one(Locacao, Locacao.id == id)
  if not locacao:
    raise HTTPException(HTTPStatus.NOT_FOUND, detail="Locação não encontrada!")

  veiculo = await engine.find_one(Veiculo, Veiculo.id == locacao.veiculo.id)
  if veiculo:
    veiculo.disponivel = True
    await engine.save(veiculo)

  await engine.delete(locacao)
  return {"detail": "Locação removida com sucesso!"}

@router.get("/soma/")
async def soma():
    pipeline = [
    {
        '$group': {
            '_id': None, 
            'total_valor_locacoes': {
                '$sum': {
                    '$multiply': [
                        {
                            '$dateDiff': {
                                'startDate': '$data_inicio', 
                                'endDate': '$data_fim', 
                                'unit': 'day'
                            }
                        }, '$valor_diaria'
                    ]
                }
            }
        }
    }
]
    result = await engine.database.get_collection("locacao").aggregate(pipeline).to_list()
    return {"Total em locações": result[0]['total_valor_locacoes']}