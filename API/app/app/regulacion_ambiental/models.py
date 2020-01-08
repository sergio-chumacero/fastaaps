###################################################################################
# Título:      Modelos de Datos para la Dirección de Regulación Ambiental (SARH)
# Ubicación:   FASTAAPS/AAPS-API/RESTAPI/app/app/regulacion_ambiental/models.py
# Descripción: Define los modelos de datos usados para la validación de datos SARH.
###################################################################################

# Dependencias
from enum import Enum
from typing import List
from pydantic import BaseModel, Field
from datetime import date




# EPSA Registro - Información General
# class ErInformacionGeneral(BaseModel):
#     """
#     Modelo para el campo 'informacion_general' del modelo 'EpsaRegistro'. 
#     """
#     id_siirays : int = Field(
#         ..., 
#         description = "ID de la EPSA en el SIIRAyS. Campo obligatorio. Corresponde a la columna 'id_epsa' de la tabla 'epsa' en el SIIRAyS.",
#     )
#     codigo : str = Field(
#         default = None,
#         description = "Código de la EPSA. Corresponde a la columna 'codigo_epsa' de la tabla 'epsa' en el SIIRAyS.",
#     ) # Observaciones: Por lo general en formato 'EPSA-XXXX', pero existen datos en blanco.
#     sigla : str = Field(
#         default = None,
#         description = "Sigla de la EPSA. Corresponde a la columna 'sigla_epsa' de la tabla 'epsa' en el SIIRAyS.",
#     ) # Observaciones: Por lo general en mayúsculas. Existen datos en blanco.
#     nombre : str = Field(
#         default = None,
#         description = "Nombre de la EPSA. Corresponde a la columna 'nombre_epsa' de la tabla 'epsa' en el SIIRAyS.",
#     ) # Observaciones: Por lo general en mayúsculas.
#     telefonos : str = Field(
#         default = None,
#         description = "Teléfonos de la EPSA. Corresponde a la columna 'telefonos' de la tabla 'epsa' en el SIIRAyS.",
#     ) # Observaciones: Por lo general múltiples números son separados por un guion (-).
#     fax : str = Field(
#         default = None,
#         description = "Fax de la EPSA. Corresponde a la columna 'fax' de la tabla 'epsa' en el SIIRAyS.",
#     ) # Observaciones: Por lo general múltiples números son separados por un guion (-).
#     correo_electronico : str = Field(
#         default = None,
#         description = "Correo electrónico de la EPSA. Corresponde a la columna 'correo_electronico' de la tabla 'epsa' en el SIIRAyS.",
#     )
#     direccion : str = Field(
#         default = None,
#         description = "Dirección de la EPSA. Corresponde a la columna 'direccion' de la tabla 'epsa' en el SIIRAyS.",
#     )
#     web : str = Field(
#         default = None,
#         description = "Página web de la EPSA. Corresponde a la columna 'web' de la tabla 'epsa' en el SIIRAyS.",
#     ) # Observaciones: TODOS los valores son 'N/I'.
#     observacion : str = Field(
#         default = None,
#         description = "Observaciones. Corresponde a la columna 'observacion' de la tabla 'epsa' en el SIIRAyS.",
#     ) # Observaciones: Dos valores encontrados 'N/I' o 'No cuenta con el formulario técnico, solo cuenta con ...'.

#     # Configuración del Modelo
#     class Config:
#         title = "EPSA Registro - Información General"

#         anystr_strip_whitespace = True        # Espacios en blanco al comienzo y final serán removidos
#         validate_all = True                   # Valores por defecto serán validados
#         extra = "ignore"                      # Campos adicionales serán ignorados
#         allow_mutation = True                 # Modelo es mutable (sus propiedades pueden ser cambiadas)
#         use_enum_values = True                # Campos con enumeraciones usarán valores en vez de objetos Enum
#         validate_assignment = True            # Cambios de atributos serán validados
#         allow_population_by_field_name = True # Campos con alias pueden ser especificados por el nombre del campo
