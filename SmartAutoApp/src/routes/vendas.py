from fastapi import APIRouter, HTTPException, Depends, Query
from http import HTTPStatus
from odmantic import AIOEngine, ObjectId
from database.mongo import get_engine  # Função que retorna o AIOEngine configurado
from datetime import datetime
from typing import List
from models.venda import Venda
from models.veiculo import Veiculo
from models.cliente import Cliente
from models.funcionario import Funcionario


router = APIRouter(prefix="/vendas", tags=["Vendas"])
engine = get_engine()


@router.get("/", response_model=List[Venda])
async def listar_vendas(
    offset: int = 0,
    limit: int = Query(default=10, le=100),
    ordem: str = "DESC",
    engine: AIOEngine = Depends(get_engine)
):
    ordem_value = -1 if ordem.upper() == "DESC" else 1
    # vendas = await engine.find(Venda, skip=offset, limit=limit, sort=[("valor", ordem_value)])
    vendas = await engine.find(Venda, skip=offset, limit=limit)
    return vendas

@router.get("/veiculos_venda/", response_model=List[Veiculo])
async def listar_veiculos(
    offset: int = 0,
    limit: int = Query(default=10, le=100),
    engine: AIOEngine = Depends(get_engine)
):
    # Em MongoDB, consultar um campo array com valor "Venda" retorna documentos onde o array contém esse valor.
    veiculos = await engine.find(Veiculo, (Veiculo.disponivel == True), skip=offset, limit=limit)
    return veiculos

@router.post("/", response_model=Venda, status_code=201)
async def criar_venda(
    vendedor_id: str,
    cliente_id: str,
    veiculo_id: ObjectId,
    data: datetime = datetime.today(),
):
    veiculo_obj = await engine.find_one(
        Veiculo,
        (Veiculo.id == veiculo_id)
    )
    if not veiculo_obj:
        raise HTTPException(status_code=404, detail="Veículo não encontrado")
    if not veiculo_obj.disponivel:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Veiculo não disponível")
    
    vendedor_obj = await engine.find_one(Funcionario, Funcionario.id == ObjectId(vendedor_id))
    if not vendedor_obj:
        raise HTTPException(status_code=404, detail="Vendedor não encontrado")
    
    cliente_obj = await engine.find_one(Cliente, Cliente.id == ObjectId(cliente_id))
    if not cliente_obj:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    
    nova_venda = Venda(
        data=data,
        valor=veiculo_obj.preco,
        vendedor=vendedor_obj,
        cliente= cliente_obj,
        veiculo= veiculo_obj
    )
    await engine.save(nova_venda)
    
    # Atualiza o veículo: marca como indisponível e associa a venda recém-criada
    veiculo_obj.disponivel = False
    await engine.save(veiculo_obj)
    
    return nova_venda

@router.get("/{id}", response_model=Venda)
async def buscar_venda(id: str, engine: AIOEngine = Depends(get_engine)):
    venda = await engine.find_one(Venda, Venda.id == ObjectId(id))
    if not venda:
        raise HTTPException(status_code=404, detail="Venda não encontrada.")
    return venda

@router.put("/{id}", response_model=Venda)
async def atualizar_venda(id: str, venda_update: Venda, engine: AIOEngine = Depends(get_engine)):
    venda = await engine.find_one(Venda, Venda.id == ObjectId(id))
    if not venda:
        raise HTTPException(status_code=404, detail="Venda não encontrada.")
    # Atualiza os campos da venda com os dados fornecidos
    venda.data = venda_update.data
    venda.valor = venda_update.valor
    venda.vendedor_id = venda_update.vendedor_id
    venda.cliente_id = venda_update.cliente_id
    venda.veiculo_id = venda_update.veiculo_id
    await engine.save(venda)
    return venda

@router.delete("/{id}")
async def remover_venda(id: str, engine: AIOEngine = Depends(get_engine)):
    venda = await engine.find_one(Venda, Venda.id == ObjectId(id))
    if not venda:
        raise HTTPException(status_code=404, detail="Venda não encontrada.")
    veiculo = await engine.find_one(Veiculo, Veiculo.id == ObjectId(venda.veiculo.id))
    veiculo.disponivel = True
    await engine.save(veiculo)
    await engine.delete(venda)
    return {"detail": "Venda apagada com sucesso"}

@router.get("/valor_minimo/", response_model=List[Venda])
async def listar_vendas_por_valor_minimo(valor_minimo: float, engine: AIOEngine = Depends(get_engine)):
    vendas = await engine.find(Venda, Venda.valor >= valor_minimo, limit=100)
    if not vendas:
        raise HTTPException(status_code=404, detail="Nenhuma venda encontrada com o valor especificado")
    return vendas

@router.get("/data/", response_model=List[Venda])
async def listar_vendas_por_data(
    data_inicial: datetime = datetime.today(),
    data_final: datetime = datetime.today(), 
    engine: AIOEngine = Depends(get_engine)
):
    vendas = await engine.find(Venda, (Venda.data >= data_inicial) & (Venda.data <= data_final), limit=100)
    if not vendas:
        raise HTTPException(status_code=404, detail="Nenhuma venda encontrada no período especificado")
    return vendas

@router.get("/soma_vendas/")
async def soma_vendas():
    pipeline = [
        
    {
        '$group': {
            '_id': None, 
            'totalValor': {
                '$sum': '$valor'
            }
        }
    }

    ]
    result = await engine.database.get_collection("venda").aggregate(pipeline).to_list()
    return {"Valor total em vendas":result[0]['totalValor']}