"""
Autores : Gabriel Raulino, Antonio Kleberson
"""

# imports do fastAPI
from fastapi import FastAPI
from contextlib import asynccontextmanager
from database.database import create_db_and_tables
from routes import categorias, funcionarios, veiculos, clientes, vendas, locacoes


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
def read_root():
    return {"msg": "SmartAutoApp"}


app.include_router(funcionarios.router)
app.include_router(clientes.router)
app.include_router(veiculos.router)
app.include_router(categorias.router)
app.include_router(vendas.router)
app.include_router(locacoes.router)
