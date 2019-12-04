############################################################################
# Título:      Puntos de Acceso para Licencias y Registro
# Ubicación:   FASTAAPS/AAPS-API/RESTAPI/app/licencias_registro/routers.py
# Descripción: Implementa los puntos de acceso hacia los datos de
#   Licencias y Registros.
############################################################################

# Dependencias
from fastapi import APIRouter, Path, Query, Body, Depends, HTTPException

from typing import List, Tuple, Union

from .models import EpsaRegistro, epsa_registro_example

from ..db import get_db_client, get_db_name, epsa_registro_collection_name

from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED, 
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND, 
)

from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import DuplicateKeyError, BulkWriteError
import json

lr_router = APIRouter()

# Restaurar Datos de EPSAs registradas
@lr_router.post(
    path = "/restore",
    summary = "Restaurar datos de registro de EPSA.",
    response_model = List[EpsaRegistro],
    response_model_skip_defaults = True,
    response_description = "Respuesta Exitosa - EPSAs Restauradas",
    status_code = HTTP_201_CREATED,
)
async def create_epsas(
    new:  List[EpsaRegistro] = Body(
        default = ...,
        media_type = "application/json",
        title = "Restaurar EPSAs (JSON)",
        example = epsa_registro_example,
    ),
    db_client: AsyncIOMotorClient = Depends(get_db_client),
    db_name: str = Depends(get_db_name),
):
    """
    Restaura datos de EPSAs en el sistema.
    ---
    Acepta un JSON representando múltiples datos de registro de EPSAs que serán ingresadas a la base de datos.
    El archivo JSON debe estar incluido en el contenido del pedido HTTP con el tipo `application/json`.
    Para pasar el proceso de validación, cada EPSA debe encontrarse en el formato descrito por el esquema `EPSA - REGISTRO`.
    ---
    Si el proceso de validación es exitoso y las EPSAs son creadas exitósamente en la base de datos,
    las instancias creadas son retornadas en el contenido de la respuesta.

    Si se producen errores durante el proceso de validación, se devuelve un error específicando el lugar y el tipo del error
    antes de proceder a ingresar el pedido a la base de datos.

    Si se producen errores al ingresar las EPSAs a la base de datos, se devuelven los errores producidos junto con una copia de las
    instancias que sí lograron ingresar exitósamente. 
    
    El proceso de ingreso de múltiples instancias a la base de datos no es ordenado.
    Se intentará ingresar todas las instancias provistas (siempre que hayan pasado el proceso de validación),
    independientes de errores previos.  
    """
    try:
        collection = db_client[db_name][epsa_registro_collection_name]
        await collection.drop()
        insert_many_response = await collection.insert_many(
            [json.loads(epsa.json()) for epsa in new],
            ordered=False,
        )
    except BulkWriteError as e:
        raise HTTPException(
            status_code = HTTP_400_BAD_REQUEST,
            detail = {
                "errores": [we["errmsg"] for we in e.details["writeErrors"]],
                "info": f"Número de EPSAs ingresadas exitósamente: {e.details.get('nInserted','No Determinado')}", 
            },
        )
    return new