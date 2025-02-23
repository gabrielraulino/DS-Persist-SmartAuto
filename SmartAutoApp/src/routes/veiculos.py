# Autor: Antonio Kleberson
from http import HTTPStatus
from fastapi import APIRouter, HTTPException, Query
from models.veiculo import Veiculo
from database.mongo import get_engine
from odmantic import ObjectId
router = APIRouter(prefix="/veiculos", tags=["Veiculos"])
# file = "src/storage/veiculos.csv"
# campos = ["id", "marca", "modelo", "ano", "preco", "valor_diaria", "disponivel", "cor"]
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
        return await engine.find(Veiculo, Veiculo.disponivel == True, skip=skip, limit=limit)

    return await engine.find(Veiculo, skip=skip, limit=limit)


# @router.get("/veiculo-com-categoria/", response_model=list[Veiculo])
# async def listar_com_categoria(
#     offset: int = 0,
#     limit: int = Query(default=10, le=100),
#     disponiveis: bool = True,
# ):
#     if disponiveis:
        
#     return (
#         session.exec(
#             select(Veiculo)
#             .options(joinedload(Veiculo.categorias))
#             .offset(offset)
#             .limit(limit)
#         )
#         .unique()
#         .all()
#     )


@router.get("/{veiculo_id}", response_model=Veiculo)
async def buscar_veiculo(_id: ObjectId):
    veiculo = engine.find_one(Veiculo,Veiculo.id == _id )
    if not veiculo:
        raise HTTPException(status_code=404, detail="Veículo não encontrado")
    return veiculo


@router.get("/categoria/{categoria}", response_model=list[Veiculo])
async def listar_veiculos_por_categoria(
    categoria: str
):
    # return await engine.find(Veiculo, Veiculo.categorias.contains(categoria))
    v = await engine.find(Veiculo, Veiculo.categorias.contains(categoria))
    return v
@router.get("/preco/", response_model=list[Veiculo])
async def listar_veiculos_por_preco(
    min_preco: float = 0,
    max_preco: float = Query(default=1000000),
):
    return await engine.find(
      Veiculo,
      Veiculo.preco >= min_preco,
      Veiculo.preco <= max_preco,
      Veiculo.disponivel == True
    )


@router.get("/ano/{ano}", response_model=list[Veiculo])
async def listar_veiculos_por_ano(ano: int):
    return await engine.find(Veiculo, Veiculo.ano == ano)


@router.get("/modelo/{modelo}", response_model=list[Veiculo])
async def listar_veiculos_por_modelo(modelo: str):
    return await engine.find(Veiculo, Veiculo.modelo == modelo)


@router.put("/{veiculo_id}", response_model=Veiculo)
async def atualizar_veiculo(
    veiculo_id: ObjectId, veiculo: Veiculo
):
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


# @router.post(
#     "/categoria/{veiculo_id}", response_model=Veiculo, status_code=HTTPStatus.CREATED
# )
# async def categoria_para_veiculos(
#     veiculo_id: int,
#     nome_categoria: str,
#     descricao: str = None,
# ):
#     categoria = session.exec(
#         select(Categoria).where(Categoria.nome == nome_categoria)
#     ).one_or_none()
#     if categoria == None:
#         categoria = Categoria(nome=nome_categoria, desc=descricao)
#         session.add(categoria)
#         session.commit()
#         session.refresh(categoria)

#     # Verificar se a combinação de categoria_id e veiculo_id já existe
#     if session.exec(
#         select(CategoriaVeiculo).where(
#             CategoriaVeiculo.categoria_id == categoria.id,
#             CategoriaVeiculo.veiculo_id == veiculo_id,
#         )
#     ).first():
#         raise HTTPException(
#             status_code=400, detail="A combinação de categoria e veículo já existe"
#         )

#     categoria_veiculo = CategoriaVeiculo(
#         veiculo_id=veiculo_id, categoria_id=categoria.id
#     )
#     session.add(categoria_veiculo)
#     session.commit()
#     session.refresh(categoria_veiculo)
#     session.refresh(categoria)
#     return categoria
