"""
Autor: Gabriel Raulino
"""

from fastapi import APIRouter, HTTPException
from http import HTTPStatus
import uuid
from typing import List
from datetime import date
from models.venda import Venda
from utils.file_handler import read_csv, append_csv, write_csv

vendas_router = APIRouter()
