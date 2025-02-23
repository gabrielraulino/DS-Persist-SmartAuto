"""
Autores : Gabriel Raulino, Antonio Kleberson
"""

# imports do fastAPI
from fastapi import FastAPI
from routes import funcionarios, veiculos, clientes, locacoes, vendas


app = FastAPI()


@app.get("/")
def read_root():
    return {"msg": "SmartAutoApp"}


app.include_router(funcionarios.router)
app.include_router(clientes.router)
app.include_router(veiculos.router)
app.include_router(vendas.router)
app.include_router(locacoes.router)
