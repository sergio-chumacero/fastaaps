###################################################################
# Título:      Aplicación Principal FastApi
# Ubicación:   FASTAAPS/AAPS-API/RESTAPI/app/main.py
# Descripción: Inicializa y configura la aplicación web FastApi. 
###################################################################

# Dependencias

from fastapi import FastAPI

# Puntos de acceso para Licencias y Registros 
from .licencias_registros.routers import lr_router

# Conexión a la base de datos
from .db import start_db_client, stop_db_client

# Aplicación principal
app_description ="""Servicio de datos REST-API de la AAPS.

Ofrece puntos de acceso a los conjuntos de datos de la AAPS. Los conjuntos de datos actualmente integrados al servicio de datos son:

* **Licencias y Registros**: Datos de EPSAs registradas.
"""

app = FastAPI(
    title = "FastAAPS",            # Título para OpenAPI
    description = app_description, # Descripción para OpenAPI
    version = "0.1.0",             # Versión del Servicio para OpenAPI
    openapi_url = "/openapi.json", # URL de acceso al JSON de OpenAPI  
    docs_url = "/openapi",         # URL de la interfaz web Swagger UI
    redoc_url= "/redoc",           # URL de la interfaz web Redoc
)

# Incluir puntos de acceso L&R
app.include_router(lr_router, prefix="/registro", tags=["Licencias y Registros"])

# Añadir métodos de inicio y cierre de conexiones a la base de datos
app.add_event_handler("startup", start_db_client)
app.add_event_handler("shutdown", stop_db_client)


