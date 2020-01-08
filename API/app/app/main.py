###################################################################
# Título:      Aplicación Principal FastApi
# Ubicación:   FASTAAPS/API/app/app/main.py
# Descripción: Inicializa y configura la aplicación web FastApi. 
###################################################################

# Dependencias
from fastapi import FastAPI                        # Aplicación principal
from starlette.staticfiles import StaticFiles      # Servicio de acceso a planillas actualizadas

from .licencias_registros.routers import lr_router # Puntos de acceso para Licencias y Registros 
from .db import start_db_client, stop_db_client    # Conexión a la base de datos


app_description ="""Servicio de datos REST-API de la AAPS.\n
Ofrece puntos de acceso a los conjuntos de datos de la AAPS. Los conjuntos de datos actualmente integrados al servicio de datos son:\n
* **Licencias y Registros**: Datos de EPSAs registradas.
"""

# Aplicación principal
app = FastAPI(
    title = "FastAAPS",            # Título para OpenAPI
    description = app_description, # Descripción para OpenAPI
    version = "0.1.0",             # Versión del Servicio para OpenAPI
    openapi_url = "/openapi.json", # URL de acceso al JSON de OpenAPI  
    docs_url = "/openapi",         # URL de la interfaz web Swagger UI
    redoc_url= "/redoc",           # URL de la interfaz web Redoc
)

# Métodos de inicio y cierre de conexiones a la base de datos
app.add_event_handler("startup", start_db_client)
app.add_event_handler("shutdown", stop_db_client)

# Puntos de acceso L&R
app.include_router(lr_router, prefix="/registro", tags=["Licencias y Registros"])

# Acceso a planillas actualizadas
app.mount(
    path = "/sheets",
    app = StaticFiles(directory="sheets"),
    name = "sheets", 
)

# Página de documentación
app.mount(
    path = "/",
    app = StaticFiles(directory="site", html=True),
    name = "site",
)