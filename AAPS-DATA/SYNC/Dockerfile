###################################################################
# Título:      Dockerfile del Servicio de Sincronización 
# Ubicación:   FASTAAPS/AAPS-DATA/sync/Dockerfile
# Descripción: 
#   Define la imágen base "celery" del servicio de sincronización. 
###################################################################

# Imágen Base: Python 3.8 (DockerHub)
FROM python:3.8.0

# Variables de ambiente: Configuración local de Python
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8 PYTHONUNBUFFERED=1

# Copia de archivos al contenderor (excluyendo .dockerignore)
COPY . /

# Instalación de dependencias de Python
WORKDIR /
RUN pip install --no-cache-dir --requirement requirements.txt
RUN rm requirements.txt
