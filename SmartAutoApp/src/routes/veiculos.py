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
        return session.exec(select(Veiculo).offset(offset).limit(limit)).all()


@router.get("/{veiculo_id}", response_model=Veiculo)
def buscar_veiculo(veiculo_id: int, session: Session = Depends(get_session)):
    veiculo = session.get(Veiculo, veiculo_id)
    if not veiculo:
        raise HTTPException(status_code=404, detail="Veículo não encontrado")
    return veiculo


@veiculos_router.get("/{id}", response_model=Veiculo)
def buscar(id: uuid.UUID):
    global veiculos_data
    veiculo = veiculos_data[veiculos_data["id"] == id]
    if veiculo.empty:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Veículo não encontrado."
        )
    return veiculo.to_dict(orient="records")[0]


@veiculos_router.put("/{id}", response_model=Veiculo)
def atualizar(id: uuid.UUID, veiculo: Veiculo):
    global veiculos_data
    elemento = veiculos_data[veiculos_data["id"] == id]
    if elemento.empty:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Veículo não encontrado."
        )
    if veiculo.id is None:
        veiculo.id = id
    veiculo_validado = Veiculo.model_validate(veiculo)
    veiculos_data.loc[elemento.index[0]] = veiculo_validado.model_dump()
    veiculos_data.to_csv(file, index=False)
    return veiculo_validado


@veiculos_router.delete("/{id}")
def remover(id: uuid.UUID):
    global veiculos_data
    elemento = veiculos_data[veiculos_data["id"] == id]
    if elemento.empty:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="Veículo não encontrado."
        )
    index = elemento.index[0]
    veiculos_data = veiculos_data.drop(index)
    veiculos_data.to_csv(file, index=False)
    return {"detail": "Veículo excluído com sucesso"}
