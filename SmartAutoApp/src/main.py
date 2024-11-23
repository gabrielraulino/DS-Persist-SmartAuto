"""
Autores : Gabriel Raulino, Antonio Kleberson 
"""

# imports do fastAPI
from fastapi import FastAPI, HTTPException
from routes.funcionarios import funcionarios_router


from routes.clientes import clientes_router


app = FastAPI()


@app.get("/")
def read_root():
    return {"msg": "SmartAutoApp"}


# app.include_router(funcionarios_router)
app.include_router(clientes_router)
