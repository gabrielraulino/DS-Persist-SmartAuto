# Autor: Antonio Kleberson
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlmodel import Session, select
from models.veiculo import Veiculo
from database.database import get_session

router = APIRouter(prefix="/veiculos", tags=["Veiculos"])
file = "src/storage/veiculos.csv"
campos = ["id", "marca", "modelo", "ano", "preco", "valor_diaria", "disponivel", "cor"]


@router.get("/", response_model=list[Veiculo])
def listar_veiculos(
    offset: int = 0,
    limit: int = Query(default=10, le=100),
    session: Session = Depends(get_session),
    disponiveis: bool = True,
):
    if disponiveis:
        return session.exec(select(Veiculo).where(Veiculo.disponivel).offset(offset).limit(limit)).all()
    
    return session.exec(select(Veiculo).offset(offset).limit(limit)).all()
    


@router.get("/{veiculo_id}", response_model=Veiculo)
def buscar_veiculo(veiculo_id: int, session: Session = Depends(get_session)):
    veiculo = session.get(Veiculo, veiculo_id)
    if not veiculo:
        raise HTTPException(status_code=404, detail="Veículo não encontrado")
    return veiculo


@router.post("/", response_model=Veiculo)
def criar_veiculo(veiculo: Veiculo, session: Session = Depends(get_session)):
    session.add(veiculo)
    session.commit()
    session.refresh(veiculo)
    return veiculo


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
