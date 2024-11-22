from fastapi import APIRouter, HTTPException
from uuid import UUID
from typing import List
from models.Funcionario import Funcionario, Role


# from storage.file_handler import append_csv, read_csv
import uuid

funcionarios_router = APIRouter()
