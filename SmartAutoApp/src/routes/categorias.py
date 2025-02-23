# Autor: Antonio Kleberson
from fastapi import APIRouter, Depends, HTTPException, Query
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, Field
from bson import ObjectId
from typing import List
import os

# MongoDB connection
MONGO_DETAILS = os.getenv("MONGO_DETAILS", "mongodb://localhost:27017")
client = AsyncIOMotorClient(MONGO_DETAILS)
database = client.smartauto
categoria_collection = database.get_collection("categorias")

router = APIRouter(prefix="/categorias", tags=["Categorias"])

class Categoria(BaseModel):
    id: str = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    nome: str
    descricao: str

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

@router.post("/", response_model=Categoria)
async def create_categoria(categoria: Categoria):
    categoria_dict = categoria.dict(by_alias=True)
    result = await categoria_collection.insert_one(categoria_dict)
    categoria_dict["_id"] = str(result.inserted_id)
    return categoria_dict

@router.get("/", response_model=List[Categoria])
async def listar_categorias(offset: int = 0, limit: int = Query(default=10, le=100)):
    categorias_cursor = categoria_collection.find().skip(offset).limit(limit)
    categorias = await categorias_cursor.to_list(length=limit)
    return categorias

@router.get("/{categoria_id}", response_model=Categoria)
async def read_categoria(categoria_id: str):
    categoria = await categoria_collection.find_one({"_id": ObjectId(categoria_id)})
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoria not found")
    return categoria

@router.put("/{categoria_id}", response_model=Categoria)
async def update_categoria(categoria_id: str, categoria: Categoria):
    update_result = await categoria_collection.update_one(
        {"_id": ObjectId(categoria_id)}, {"$set": categoria.dict(exclude_unset=True)}
    )
    if update_result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Categoria not found")
    updated_categoria = await categoria_collection.find_one({"_id": ObjectId(categoria_id)})
    return updated_categoria

@router.delete("/{categoria_id}")
async def delete_categoria(categoria_id: str):
    delete_result = await categoria_collection.delete_one({"_id": ObjectId(categoria_id)})
    if delete_result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Categoria not found")
    return {"ok": True}
