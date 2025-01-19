# Autor: Antonio Kleberson
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlmodel import select
from models import Categoria
from database import get_session

# Vendas Routes (Atualizar)
# Veiculos Routes (Consultas)

router = APIRouter()

@router.get("/", response_model=list[Categoria])
def listar_categorias(
    offset: int = 0,
    limit: int = Query(default=10, le=100),
    session: Session = Depends(get_session),
):
    return session.exec(select(Categoria).offset(offset).limit(limit)).all()

@router.get("/{categoria_id}", response_model=Categoria)
def read_categoria(categoria_id: int, session: Session = Depends(get_session)):
    categoria = session.get(Categoria, categoria_id)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoria not found")
    return categoria.model_dump()

@router.post("/", response_model=Categoria)
def create_categoria(
    nome: str,
    descricao: str,
    session: Session = Depends(get_session),
):
    categoria = Categoria(nome=nome, descricao=descricao)
    session.add(categoria)
    session.commit()
    session.refresh(categoria)
    return categoria.model_dump()

@router.put("/{categoria_id}", response_model=Categoria)
def update_categoria(
    categoria_id: int, categoria: Categoria, session: Session = Depends(get_session)
):
    db_categoria = session.get(Categoria, categoria_id)
    if not db_categoria:
        raise HTTPException(status_code=404, detail="Categoria not found")
    for key, value in categoria.model_dump(exclude_unset=True).items():
        setattr(db_categoria, key, value)
    session.add(db_categoria)
    session.commit()
    session.refresh(db_categoria)
    return db_categoria.model_dump()

@router.delete("/{categoria_id}")
def delete_categoria(categoria_id: int, session: Session = Depends(get_session)):
    categoria = session.get(Categoria, categoria_id)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoria not found")
    session.delete(categoria)
    session.commit()
    return {"ok": True}
