from fastapi import APIRouter, HTTPException
from uuid import UUID
from typing import List
from models.cliente import Cliente
from models.endereco import Endereco
from storage.file_handler import append_csv, read_csv
import uuid

clientes_router = APIRouter()

# Persistência dos clientes utilizando armazenamento em CSV
