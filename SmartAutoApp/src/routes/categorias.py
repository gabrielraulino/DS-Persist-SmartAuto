# from fastapi import APIRouter, Depends, HTTPException, Query
# from odmantic import AIOEngine, ObjectId
# from models.veiculo import Veiculo
# from models.categoria import Categoria
# from database.mongo import get_engine
# from typing import List

# router = APIRouter(prefix="/categorias", tags=["Categorias"])

# # Modelo ODMantic para Categoria

# @router.post("/", response_model=Categoria)
# async def create_categoria(
#     categoria: Categoria,
#     engine: AIOEngine = Depends(get_engine)
# ):
#     await engine.save(categoria)
#     return categoria

# @router.get("/", response_model=List[Categoria])
# async def listar_categorias(
#     offset: int = 0,
#     limit: int = Query(default=10, le=100),
#     engine: AIOEngine = Depends(get_engine)
# ):
#     categorias = await engine.find(Categoria, skip=offset, limit=limit)
#     return categorias

# @router.get("/{categoria_id}", response_model=Categoria)
# async def read_categoria(
#     categoria_id: str,
#     engine: AIOEngine = Depends(get_engine)
# ):
#     categoria = await engine.find_one(Categoria, Categoria.id == ObjectId(categoria_id))
#     if not categoria:
#         raise HTTPException(status_code=404, detail="Categoria not found")
#     return categoria

# @router.put("/{categoria_id}", response_model=Categoria)
# async def update_categoria(
#     categoria_id: str,
#     categoria: Categoria,
#     engine: AIOEngine = Depends(get_engine)
# ):
#     db_categoria = await engine.find_one(Categoria, Categoria.id == ObjectId(categoria_id))
#     if not db_categoria:
#         raise HTTPException(status_code=404, detail="Categoria not found")
#     # Atualiza os campos desejados
#     db_categoria.nome = categoria.nome
#     db_categoria.descricao = categoria.descricao
#     await engine.save(db_categoria)
#     return db_categoria

# @router.delete("/{categoria_id}")
# async def delete_categoria(
#     categoria_id: str,
#     engine: AIOEngine = Depends(get_engine)
# ):
#     categoria = await engine.find_one(Categoria, Categoria.id == ObjectId(categoria_id))
#     if not categoria:
#         raise HTTPException(status_code=404, detail="Categoria not found")
#     await engine.delete(categoria)
#     return {"ok": True}

# @router.get("/estatisticas/veiculos", response_model=dict)
# async def estatisticas_veiculos_por_categoria(
#     categoria_id: str,
#     engine: AIOEngine = Depends(get_engine)
# ):
#     pipeline = [
#         {
#             "$match": {
#                 "categoria_id": ObjectId(categoria_id)
#             }
#         },
#         {
#             "$group": {
#                 "_id": "$categoria_id",
#                 "totalVeiculos": {"$sum": 1}
#             }
#         },
#         {
#             "$lookup": {
#                 "from": "categorias",         # Nome da coleção de categorias; verifique se bate com a configuração do seu projeto
#                 "localField": "_id",
#                 "foreignField": "_id",
#                 "as": "categoria_info"
#             }
#         },
#         {
#             "$unwind": "$categoria_info"
#         }
#     ]
#     resultados = [doc async for doc in engine.aggregate(Veiculo, pipeline)]
#     if not resultados:
#         raise HTTPException(status_code=404, detail="Nenhum veículo encontrado para a categoria informada")
#     return resultados[0]