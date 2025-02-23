# Autor: Antonio Kleberson
from logging import Logger
from http import HTTPStatus
from typing import Dict
from fastapi import APIRouter, Depends, HTTPException, Query, logger
from models.veiculo import Veiculo
from models.categoria import Categoria
from database.mongo import get_engine
from odmantic import AIOEngine, ObjectId

router = APIRouter(prefix="/veiculos", tags=["Veiculos"])
engine = get_engine()

@router.post("/", response_model=Veiculo, status_code=HTTPStatus.CREATED)
async def criar_veiculo(veiculo: Veiculo):
    await engine.save(veiculo)
    return veiculo


@router.get("/", response_model=list[Veiculo])
async def listar_veiculos(
    skip: int = 0,
    limit: int = Query(default=10, le=100),
    disponiveis: bool = True,
):
    if disponiveis:
        return await engine.find(
            Veiculo, Veiculo.disponivel == True, skip=skip, limit=limit
        )

    return await engine.find(Veiculo, skip=skip, limit=limit)


@router.get("/{veiculo_id}", response_model=Veiculo)
async def buscar_veiculo(_id: ObjectId) -> Veiculo:
    veiculo = engine.find_one(Veiculo, Veiculo.id == _id)
    if not veiculo:
        raise HTTPException(status_code=404, detail="Veículo não encontrado")
    return veiculo


@router.get("/categoria/{categoria}", response_model=list[Veiculo])
async def listar_veiculos_por_categoria(categoria: str):
    # return await engine.find(Veiculo, Veiculo.categorias.contains(categoria))
    c = await engine.find_one(Categoria, Categoria.nome == categoria)
    if not c:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Categoria " + categoria + " não existe",
        )
    return await engine.find(Veiculo, {"categorias.nome": "Sedan"})


@router.get("/preco/", response_model=list[Veiculo])
async def listar_veiculos_por_preco(
    min_preco: float = 0,
    max_preco: float = Query(default=1000000),
):
    return await engine.find(
        Veiculo,
        Veiculo.preco >= min_preco,
        Veiculo.preco <= max_preco,
        Veiculo.disponivel == True,
    )


@router.get("/ano/{ano}", response_model=list[Veiculo])
async def listar_veiculos_por_ano(min: int, max:int):
    return await engine.find(Veiculo, Veiculo.ano >= min and Veiculo.ano <= max)

@router.get("")
async def total_valor_veiculos(engine: AIOEngine = Depends(get_engine)):
    pipeline = [
        { '$match': { 'disponivel': True } },
        {
            '$group': {
                '_id': None,
                'totalPreco': { '$sum': '$preco' }
            }
        }
    ]
    result = await engine.database.get_collection("veiculo").aggregate(pipeline).to_list(length=None)
    if not result:
      return {"Valor total dos veículos": 0.0}
    return {"Valor total dos veículos": result[0]["totalPreco"]}




@router.get("/modelo/{modelo}", response_model=list[Veiculo])
async def listar_veiculos_por_modelo(modelo: str):
    return await engine.find(Veiculo, Veiculo.modelo == modelo)


@router.put("/{veiculo_id}", response_model=Veiculo)
async def atualizar_veiculo(veiculo_id: ObjectId, veiculo: Veiculo):
    db_veiculo = await engine.find_one(Veiculo, Veiculo.id == veiculo_id)
    if not db_veiculo:
        raise HTTPException(status_code=404, detail="Veículo não encontrado")
    for key, value in veiculo.model_dump(exclude_unset=True).items():
        setattr(db_veiculo, key, value)
    await engine.save(veiculo)
    return db_veiculo


@router.delete("/{veiculo_id}")
async def remover_veiculo(veiculo_id: ObjectId):
    veiculo = await engine.find(Veiculo, Veiculo.id == veiculo_id)
    if not veiculo:
        raise HTTPException(status_code=404, detail="Veículo não encontrado")
    engine.delete(veiculo)
    return {"ok": True}


async def buscar_categoria(nome: str) -> Categoria:
    c = await engine.find_one(Categoria, Categoria.nome == nome)
    if not c:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    return c


@router.post("/categoria", response_model=Categoria, status_code=HTTPStatus.CREATED)
async def criar_categoria(categoria: Categoria):
    c = await engine.find_one(Categoria, Categoria.id == categoria.nome)
    if c:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail="Categoria já existe"
        )
    await engine.save(categoria)
    return categoria


@router.get("/categoria/", response_model=list[Categoria])
async def listar_categorias(skip: int = 0, limit: int = Query(default=10, le=100)):
    return await engine.find(Categoria, skip=skip, limit=limit)


@router.post(
    "/categoria/{veiculo_id}", response_model=Veiculo, status_code=HTTPStatus.CREATED
)
async def categoria_para_veiculos(
    veiculo_id: ObjectId,
    nome_categoria: str,
):
    v = await engine.find_one(Veiculo, Veiculo.id == veiculo_id)
    if not v:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Veiculo não encotrado"
        )
    c = await buscar_categoria(nome_categoria)
    if not c:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Categoria não encotrada"
        )
    if c in v.categorias:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Categoria " + c.nome + " já está cadastrada!",
        )
    v.categorias.append(c)
    await engine.save(v)
    return v
