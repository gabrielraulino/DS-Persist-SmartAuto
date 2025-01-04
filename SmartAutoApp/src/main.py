"""
Autores : Gabriel Raulino, Antonio Kleberson 
"""

# imports do fastAPI
from fastapi import FastAPI

from routes.clientes import clientes_router
from routes.funcionarios import funcionarios_router
from routes.veiculos import veiculos_router
from routes.locacoes import locacoes_router
from routes.vendas import vendas_router
from routes.modelos import modelos_router


app = FastAPI()


@app.get("/")
def read_root():
    return {"msg": "SmartAutoApp"}


app.include_router(funcionarios_router)
app.include_router(clientes_router)
app.include_router(veiculos_router)
app.include_router(vendas_router)
app.include_router(locacoes_router)
app.include_router(modelos_router)
