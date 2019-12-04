###################################################################
# Título:      Conexión entre REST-API y Base de Datos 
# Ubicación:   FASTAAPS/AAPS-API/RESTAPI/app/db.py
# Descripción: Configura la conexión entre la aplicación FastApi y
#   la base de datos MongoDB. 
###################################################################

# Dependencias
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ServerSelectionTimeoutError, DuplicateKeyError
from typing import Optional
import os

# Variables de configuración
MONGO_DB_HOST = os.environ.get("MONGO_DB_HOST")
MONGO_DB_PORT = os.environ.get("MONGO_DB_PORT")
MONGO_DB_USER = os.environ.get("MONGO_DB_USER")
MONGO_DB_PASS = os.environ.get("MONGO_DB_PASS")

# Variables de conexión
MONGO_DB_URL = f"mongodb://{MONGO_DB_USER}:{MONGO_DB_PASS}@{MONGO_DB_HOST}:{MONGO_DB_PORT}"
DB_NAME = "fastaaps"
epsa_registro_collection_name = "epsa_registro"

# Cliente de base de datos
class DataBase():
    client: Optional[AsyncIOMotorClient] = None

# Instancia de cliente de base de datos (única por aplicación)
db = DataBase()

# Inicia la conexión con la base de datos
async def start_db_client() -> None:
    """
    Establece la conexión con la base de datos de MongoDB 
    y garantiza la existencia de los índices necesarios.
    """
    db.client = AsyncIOMotorClient(
        MONGO_DB_URL,
        minPoolSize = 0,
        maxPoolSize = 50,
    )
    
    # index_info = await db.client[DB_NAME][epsa_registro_collection_name].index_information()
    # if "epsa_code" not in index_info.keys():
    #     await db.client[db_name][EPSAS_COLLECTION_NAME].create_index("code", name="epsa_code", unique=True)

# Cierra la conexión con la  base de datos
async def stop_db_client():
    """
    Cierra la conexión con la base de datos MongoDB limpiamente.
    """
    db.client.close()

# Obtener conexión
async def get_db_client() -> AsyncIOMotorClient:
    return db.client

# Obtener nombre de base de datos
def get_db_name():
    return DB_NAME
