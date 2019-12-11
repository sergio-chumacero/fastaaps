###################################################################
# Título:      Aplicación Celery
# Ubicación:   FASTAAPS/AAPS-DATA/SYNC/app/main.py
# Descripción: 
#   Confifuración de la aplicación Celery y las tareas periódicas. 
###################################################################

# Dependencias
from celery import Celery
import os

# Configuración: Variables de Ambiente
# CELERY_BACKEND_URL = os.environ["CELERY_BACKEND_URL"]     # Guardado de resultados (Mensajes AMQP)
CELERY_PERIOD_LENGTH = os.environ["CELERY_PERIOD_LENGTH"] # Duración de un periodo en segundos
CELERY_TASK_ARGS = os.environ["CELERY_TASK_ARGS"]         # Argumentos para la función periódica   

# Configuración de la aplicación Celery
app = Celery(
    # backend = CELERY_BACKEND_URL, # Guardado de resultados
    include = ["app.tasks"]       # Módulos a importar
)

# Configuración de las tareas periódicas (Celery Beat)
app.conf.beat_schedule = {
    "sync_db": {
        "task": "sync_db",                       # Nombre de la tarea
        "schedule": float(CELERY_PERIOD_LENGTH), # Duración de un periodo
        "args": (CELERY_TASK_ARGS,),             # Argumentos de la tarea
    },
}

# Configuración para el almacenamiento de resultados en MongoDB
app.conf.mongodb_backend_settings = {
    "database": "admin",
    "taskmeta_collection": "resultados",
}