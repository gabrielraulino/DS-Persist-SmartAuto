from fastapi import APIRouter, Depends, HTTPException, Query
from http import HTTPStatus
from models.funcionario import Funcionario, Role
from database.mongo import get_engine
from odmantic import AIOEngine, ObjectId

router = APIRouter(prefix="/funcionarios", tags=["Funcionarios"])
file = "src/storage/funcionarios.csv"
# campos = ["id", "usuario", "senha", "nome", "telefone", "funcao"]

engine = get_engine()
@router.post("/", response_model=Funcionario)
async def create(
    funcionario : Funcionario
) -> Funcionario:
    await engine.save(funcionario)
    return funcionario


@router.get("/", response_model=list[Funcionario])
async def listar(
    offset: int = 0,
    limit: int = Query(default=10, le=100),
):
    funcionarios = await engine.find(Funcionario, skip=offset, limit=limit)
    return funcionarios

@router.get("/{id}", response_model=Funcionario)
async def read(_id: ObjectId):
    funcionario = await engine.find_one(Funcionario, Funcionario.id == _id)
    if not funcionario:
        raise HTTPException(status_code=404, detail= "Funcionario not found")
    return funcionario


@router.get("/search/{name}", response_model=list[Funcionario])
async def search_by_name(name: str, engine: AIOEngine = Depends(get_engine)):
    funcionarios = await engine.find(Funcionario, Funcionario.nome.match(name))
    if not funcionarios:
        raise HTTPException(status_code=404, detail="Funcionário não encontrado")
    return funcionarios

@router.get("/role/{funcao}", response_model=list[Funcionario])
async def search_by_role(funcao: Role):
    return await engine.find(Funcionario, Funcionario.funcao == funcao)

@router.put("/{id}", response_model=Funcionario)
async def update(
    _id: ObjectId, funcionario: dict
):
    user = await engine.find_one(Funcionario, Funcionario.id == _id)
    if not user:
        raise HTTPException(status_code=404, detail="Funcionario not found")
    for key, value in funcionario.items():
        setattr(user, key, value)
    await engine.save(user)
    return user.model_dump()


@router.delete("/{id}")
async def delete(funcionario_id: ObjectId):
    user = await engine.find_one(Funcionario, Funcionario.id == funcionario_id)
    if not user:
        raise HTTPException(status_code=404, detail="Funcionario not found")
    await engine.delete(user)
    return {"message": "User deleted"}
