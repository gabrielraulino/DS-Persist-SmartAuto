# Autor: Antonio Kleberson
from enum import Enum
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlmodel import Session, select
from models.categoria import Categoria
from models.veiculo import CategoriaVeiculo, Veiculo
from database.database import get_session

router = APIRouter(prefix="/veiculos", tags=["Veiculos"])
file = "src/storage/veiculos.csv"
campos = ["id", "marca", "modelo", "ano", "preco", "valor_diaria", "disponivel", "cor"]


@router.post("/", response_model=Veiculo)
def criar_veiculo(veiculo: Veiculo, session: Session = Depends(get_session)):
    session.add(veiculo)
    session.commit()
    session.refresh(veiculo)
    return veiculo


class Ordem(str, Enum):
    ASC = "asc"
    DESC = "desc"


@router.get("/", response_model=list[Veiculo])
def listar_veiculos(
    offset: int = 0,
    limit: int = Query(default=10, le=100),
    session: Session = Depends(get_session),
    disponiveis: bool = True,
):
    if disponiveis:
        return session.exec(
            select(Veiculo).where(Veiculo.disponivel).offset(offset).limit(limit)
        ).all()

    return session.exec(select(Veiculo).offset(offset).limit(limit)).all()


@router.get("/{veiculo_id}", response_model=Veiculo)
def buscar_veiculo(veiculo_id: int, session: Session = Depends(get_session)):
    veiculo = session.get(Veiculo, veiculo_id)
    if not veiculo:
        raise HTTPException(status_code=404, detail="Veículo não encontrado")
    return veiculo


@router.get("/categoria/{categoria}", response_model=list[Veiculo])
def listar_veiculos_por_categoria(
    categoria: str, session: Session = Depends(get_session)
):
    return session.exec(
        select(Veiculo)
        .join(CategoriaVeiculo)
        .join(Categoria)
        .where(Categoria.nome == categoria)
    ).all()


@router.get("/preco/", response_model=list[Veiculo])
def listar_veiculos_por_preco(
    min_preco: float = 0,
    max_preco: float = Query(default=1000000),
    session: Session = Depends(get_session),
):
    return session.exec(
        select(Veiculo).where(Veiculo.preco.between(min_preco, max_preco))
    ).all()


@router.get("/ano/{ano}", response_model=list[Veiculo])
def listar_veiculos_por_ano(ano: int, session: Session = Depends(get_session)):
    return session.exec(select(Veiculo).where(Veiculo.ano == ano)).all()


@router.get("/modelo/{modelo}", response_model=list[Veiculo])
def listar_veiculos_por_modelo(modelo: str, session: Session = Depends(get_session)):
    return session.exec(select(Veiculo).where(Veiculo.modelo == modelo)).all()


@router.put("/{veiculo_id}", response_model=Veiculo)
def atualizar_veiculo(
    veiculo_id: int, veiculo: Veiculo, session: Session = Depends(get_session)
):
    db_veiculo = session.get(Veiculo, veiculo_id)
    if not db_veiculo:
        raise HTTPException(status_code=404, detail="Veículo não encontrado")
    for key, value in veiculo.dict(exclude_unset=True).items():
        setattr(db_veiculo, key, value)
    session.add(db_veiculo)
    session.commit()
    session.refresh(db_veiculo)
    return db_veiculo


@router.delete("/{veiculo_id}")
def remover_veiculo(veiculo_id: int, session: Session = Depends(get_session)):
    veiculo = session.get(Veiculo, veiculo_id)
    if not veiculo:
        raise HTTPException(status_code=404, detail="Veículo não encontrado")
    session.delete(veiculo)
    session.commit()
    return {"ok": True}


@router.post("/{veiculo_id}/categoria/", response_model=Categoria)
def categoria_para_veiculos(
    veiculo_id: int,
    nome_categoria: str,
    descricao: str = None,
    session: Session = Depends(get_session),
):
    categoria_db = session.exec(
        select(Categoria).where(Categoria.nome == nome_categoria)
    ).first()
    if categoria_db:
        categoria = categoria_db
    else:
        categoria = Categoria(nome=nome_categoria, desc=descricao)
        session.add(categoria)
        session.commit()
        session.refresh(categoria)

    # Verificar se a combinação de categoria_id e veiculo_id já existe
    categoria_veiculo_existente = session.exec(
        select(CategoriaVeiculo).where(
            CategoriaVeiculo.categoria_id == categoria.id,
            CategoriaVeiculo.veiculo_id == veiculo_id,
        )
    ).first()

    if categoria_veiculo_existente:
        raise HTTPException(
            status_code=400, detail="A combinação de categoria e veículo já existe"
        )

    categoria_veiculo = CategoriaVeiculo(
        veiculo_id=veiculo_id, categoria_id=categoria.id
    )
    session.add(categoria_veiculo)
    session.commit()
    return categoria.model_dump()
