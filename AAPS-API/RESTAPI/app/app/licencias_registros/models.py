############################################################################
# Título:      Modelos de Datos para Licencias y Registro
# Ubicación:   FASTAAPS/AAPS-API/RESTAPI/app/licencias_registro/models.py
# Descripción: Define los modelos de datos de comunicación para
#   Licencias y Registros.
############################################################################

# Dependencias
from enum import Enum
from typing import List
from pydantic import BaseModel, Field
from datetime import date

# EPSA Registro - Información General
class ErInformacionGeneral(BaseModel):
    """
    Modelo para el campo 'informacion_general' del modelo 'EpsaRegistro'. 
    """
    id_siirays : int = Field(
        ..., 
        description = "ID de la EPSA en el SIIRAyS. Campo obligatorio. Corresponde a la columna 'id_epsa' de la tabla 'epsa' en el SIIRAyS.",
    )
    codigo : str = Field(
        default = None,
        description = "Código de la EPSA. Corresponde a la columna 'codigo_epsa' de la tabla 'epsa' en el SIIRAyS.",
    ) # Observaciones: Por lo general en formato 'EPSA-XXXX', pero existen datos en blanco.
    sigla : str = Field(
        default = None,
        description = "Sigla de la EPSA. Corresponde a la columna 'sigla_epsa' de la tabla 'epsa' en el SIIRAyS.",
    ) # Observaciones: Por lo general en mayúsculas. Existen datos en blanco.
    nombre : str = Field(
        default = None,
        description = "Nombre de la EPSA. Corresponde a la columna 'nombre_epsa' de la tabla 'epsa' en el SIIRAyS.",
    ) # Observaciones: Por lo general en mayúsculas.
    telefonos : str = Field(
        default = None,
        description = "Teléfonos de la EPSA. Corresponde a la columna 'telefonos' de la tabla 'epsa' en el SIIRAyS.",
    ) # Observaciones: Por lo general múltiples números son separados por un guion (-).
    fax : str = Field(
        default = None,
        description = "Fax de la EPSA. Corresponde a la columna 'fax' de la tabla 'epsa' en el SIIRAyS.",
    ) # Observaciones: Por lo general múltiples números son separados por un guion (-).
    correo_electronico : str = Field(
        default = None,
        description = "Correo electrónico de la EPSA. Corresponde a la columna 'correo_electronico' de la tabla 'epsa' en el SIIRAyS.",
    )
    direccion : str = Field(
        default = None,
        description = "Dirección de la EPSA. Corresponde a la columna 'direccion' de la tabla 'epsa' en el SIIRAyS.",
    )
    web : str = Field(
        default = None,
        description = "Página web de la EPSA. Corresponde a la columna 'web' de la tabla 'epsa' en el SIIRAyS.",
    ) # Observaciones: TODOS los valores son 'N/I'.
    observacion : str = Field(
        default = None,
        description = "Observaciones. Corresponde a la columna 'observacion' de la tabla 'epsa' en el SIIRAyS.",
    ) # Observaciones: Dos valores encontrados 'N/I' o 'No cuenta con el formulario técnico, solo cuenta con ...'.

    # Configuración del Modelo
    class Config:
        title = "EPSA Registro - Información General"

        anystr_strip_whitespace = True        # Espacios en blanco al comienzo y final serán removidos
        validate_all = True                   # Valores por defecto serán validados
        extra = "ignore"                      # Campos adicionales serán ignorados
        allow_mutation = True                 # Modelo es mutable (sus propiedades pueden ser cambiadas)
        use_enum_values = True                # Campos con enumeraciones usarán valores en vez de objetos Enum
        validate_assignment = True            # Cambios de atributos serán validados
        allow_population_by_field_name = True # Campos con alias pueden ser especificados por el nombre del campo

# EPSA Registro - Representante
class ErRepresentante(BaseModel):
    """
    Modelo para el campo 'representante' del modelo 'EpsaRegistro'. 
    """
    nombre : str = Field(
        default = None,
        description = "Nombre del representante de la EPSA. Corresponde a la columna 'nombre_representante' de la tabla 'representante' en el SIIRAyS.",
    ) # Observaciones: Por lo general en mayúsculas. No existen datos en blanco.
    cargo : str = Field(
        default = None,
        description = "Cargo del representante de la EPSA. Corresponde a la columna 'cargo' de la tabla 'representante' en el SIIRAyS.",
    ) # Observaciones: Por lo general en mayúsculas. Existen datos en blanco.
    telefono : str = Field(
        default = None,
        description = "Teléfono del representante de la EPSA. Corresponde a la columna 'telefono' de la tabla 'representante' en el SIIRAyS.",
    ) # Observaciones: Por lo general múltiples números son separados por un guion (-). Existen datos en blanco.
    celular : str = Field(
        default = None,
        description = "Celular del representante de la EPSA. Corresponde a la columna 'celular' de la tabla 'representante' en el SIIRAyS.",
    ) # Observaciones: Por lo general múltiples números son separados por un guion (-). Existen datos en blanco.
    correo : str = Field(
        default = None,
        description = "Correo del representante de la EPSA. Corresponde a la columna 'correo' de la tabla 'representante' en el SIIRAyS.",
    ) # Observaciones: TODOS en blanco.
    numero_resolucion : str = Field(
        default = None,
        description = "Numero de la RAR. Corresponde a la columna 'numero_resolucion' de la tabla 'rar' en el SIIRAyS.",
    ) # Observaciones: Generalmente en formato 'XXX/20XX' con muchas excepciones como 'AAPS No. XXX/20XX' o 'SISAB No. XXX/20XX'.
    fecha_resolucion : date = Field(
        default = None,
        description = "Fecha de resolución de la RAR. Debe tener formato de fecha AAAA-MM-DD. Corresponde a la columna 'fecha_resolucion' de la tabla 'rar' en el SIIRAyS.",
    ) # Observaciones: Sin datos en blanco.
    descripcion_resolucion : str = Field(
        default = None,
        description = "Descripción de la RAR. Corresponde a la columna 'descripcion_resolucion' de la tabla 'rar' en el SIIRAyS.",
    )
    tipo_contacto : str = Field(
        default = None,
        description = "Tipo del contacto. Corresponde a la columna 'tipo_contacto' de la tabla 'tipo_contacto' en el SIIRAyS.",
    )

    # Configuración del Modelo
    class Config:
        title = "EPSA Registro - Representante"

        anystr_strip_whitespace = True        # Espacios en blanco al comienzo y final serán removidos
        validate_all = True                   # Valores por defecto serán validados
        extra = "ignore"                      # Campos adicionales serán ignorados
        allow_mutation = True                 # Modelo es mutable (sus propiedades pueden ser cambiadas)
        use_enum_values = True                # Campos con enumeraciones usarán valores en vez de objetos Enum
        validate_assignment = True            # Cambios de atributos serán validados
        allow_population_by_field_name = True # Campos con alias pueden ser especificados por el nombre del campo


# EPSA Registro - Ubicación
class ErUbicacion(BaseModel):
    """
    Modelo para el campo 'ubicacion' del modelo 'EpsaRegistro'. 
    """
    codigo_ine : str = Field(
        default = None,
        description = "Código INE de la localidad. Corresponde a la columna 'codigo_ine' de la tabla 'localidad' en el SIIRAyS.",
    ) # Observaciones: Dos opciones 'cod-ine' y 'cod-aaps'. No existen datos en blanco ni duplicados.
    cod_departamento : str = Field(
        default = None,
        description = "Código del departamento donde se ubica la localidad. Corresponde a la columna 'cod_departamento' de la tabla 'localidad' en el SIIRAyS.",
    ) # Observaciones: Opciones 01-09. No existen datos en blanco.
    departamento : str = Field(
        default = None,
        description = "Nombre del departamento donde se ubica la localidad. Corresponde a la columna 'departamento' de la tabla 'localidad' en el SIIRAyS.",
    ) # Observaciones: Opciones de departamento en mayúsculas. No existen datos en blanco.
    cod_provincia : str = Field(
        default = None,
        description = "Código de la provincia donde se ubica la localidad. Corresponde a la columna 'cod_provincia' de la tabla 'localidad' en el SIIRAyS.",
    ) # Observaciones: Opciones de 27 códigos de provincias. No existen datos en blanco.
    provincia : str = Field(
        default = None,
        description = "Nombre de la provincia donde se ubica la localidad. Corresponde a la columna 'provincia' de la tabla 'localidad' en el SIIRAyS.",
    ) # Observaciones: Opciones de provincias en mayúsculas. No existen datos en blanco.
    cod_municipio : str = Field(
        default = None,
        description = "Código del municipio donde se ubica la localidad. Corresponde a la columna 'cod_municipio' de la tabla 'localidad' en el SIIRAyS.",
    ) # Observaciones: Opciones de 374 códigos de municipio en formato XXXXX. No existen datos en blanco.
    municipio : str = Field(
        default = None,
        description = "Nombre del municipio donde se ubica la localidad. Corresponde a la columna 'municipio' de la tabla 'localidad' en el SIIRAyS.",
    ) # Observaciones: Opciones de municipio en mayúsculas. No existen datos en blanco.
    cod_comunidad : str = Field(
        default = None,
        description = "Código de la comunidad correspondiente a la localidad. Corresponde a la columna 'cod_comunidad' de la tabla 'localidad' en el SIIRAyS.",
    ) # Observaciones: Opciones de 305 códigos de comunidad en formato XXXXXX. No existen datos en blanco.
    comunidad : str = Field(
        default = None, 
        description = "Nombre de la comunidad correspondiente a la localidad. Corresponde a la columna 'comunidad' de la tabla 'localidad' en el SIIRAyS.",
    ) # Observaciones: Opciones de 2716 comunidades en mayúsculas. No existen datos en blanco.
    latitud : str = Field(
        default = None,
        description = "Latitud de la localidad. Corresponde a la columna 'latitud' de la tabla 'localidad' en el SIIRAyS.",
    ) # Observaciones: TODOS los datos en blanco.
    longitud : str = Field(
        default = None,
        description = "Longitud de la localidad. Corresponde a la columna 'longitud' de la tabla 'localidad' en el SIIRAyS.",
    ) # Observaciones: TODOS los datos en blanco.
    localidad : str = Field(
        default = None,
        description = "Nombre de la localidad. Corresponde a la columna 'localidad' de la tabla 'localidad' en el SIIRAyS.",
    ) # Observaciones: Opciones de 2721 localidades en mayúsculas. No existen datos en blanco.

    # Configuración del Modelo
    class Config:
        title = "EPSA Registro - Ubicación" # Título para JSON-Schema

        anystr_strip_whitespace = True        # Espacios en blanco al comienzo y final serán removidos
        validate_all = True                   # Valores por defecto serán validados
        extra = "ignore"                      # Campos adicionales serán ignorados
        allow_mutation = True                 # Modelo es mutable (sus propiedades pueden ser cambiadas)
        use_enum_values = True                # Campos con enumeraciones usarán valores en vez de objetos Enum
        validate_assignment = True            # Cambios de atributos serán validados
        allow_population_by_field_name = True # Campos con alias pueden ser especificados por el nombre del campo
          

# EPSA Registro
class EpsaRegistro(BaseModel):
    informacion_general : ErInformacionGeneral = Field(
        default = None,
        description = "Información General de la EPSA. Estos datos corresponden a la tabla epsa' en el SIIRAyS.",
    ) # Observaciones: Un objeto por EPSA.
    representante : List[ErRepresentante] = Field(
        default = None,
        description = "Información del representante legal la EPSA. Estos datos corresponden a las tablas 'representante', 'rar' y 'tipo_contacto' en el SIIRAyS.",
    ) # Observaciones: Posiblemente múltiples objetos por EPSA.
    ubicacion : List[ErUbicacion] = Field(
        default = None,
        description = "Información de la ubicación geográfica EPSA. Estos datos corresponden a las tablas 'ubicacion' y 'localidad' en el SIIRAyS.",
    ) # Observaciones: Posiblemente múltiples objetos por EPSA.

    class Config:
        title = "EPSA Registro"

        anystr_strip_whitespace = True        # Espacios en blanco al comienzo y final serán removidos
        validate_all = True                   # Valores por defecto serán validados
        extra = "ignore"                      # Campos adicionales serán ignorados
        allow_mutation = True                 # Modelo es mutable (sus propiedades pueden ser cambiadas)
        use_enum_values = True                # Campos con enumeraciones usarán valores en vez de objetos Enum
        validate_assignment = True            # Cambios de atributos serán validados
        allow_population_by_field_name = True # Campos con alias pueden ser especificados por el nombre del campo

epsa_registro_example = {
    "informacion_general": {
        "id_siirays": 2016,
        "codigo": "EPSA-0498",
        "sigla": "COAG",
        "nombre": "COMUNIDAD AGUAQUIZA",
        "telefonos": "6933095",
        "fax": "6933095",
        "correo_electronico": None,
        "direccion": "Escuela Franz Tamayo",
        "web": "N/I",
        "observacion": "N/I"
    },
    "representante": [
        {
            "nombre": "DIONISIO LÓPEZ COPA",
            "cargo": None,
            "telefono": None,
            "celular": "6933095",
            "correo": None,
            "numero_resolucion": "262/2008",
            "fecha_resolucion": "2008-08-01",
            "descripcion_resolucion": "",
            "tipo_contacto": "Presidente"
        }
    ],
    "ubicacion": [
        {
            "codigo_ine": "cod-ine",
            "cod_departamento": "05",
            "departamento": "POTOSI",
            "cod_provincia": "09",
            "provincia": "NOR LIPEZ",
            "cod_municipio": "050901",
            "municipio": "COLCHA K",
            "cod_comunidad": "cod_comunidad",
            "comunidad": "AGUAQUIZA",
            "latitud": "0",
            "longitud": "0",
            "localidad": "AGUAQUIZA"
        }
    ],
    "documentos_acreditacion": [
        {
            "tipo": "Persona colectiva",
            "descripcion": "Fotocopia de actas"
        },
        {
            "tipo": "Derecho uso al recurso hidrico",
            "descripcion": "Acuerdo de partes"
        },
        {
            "tipo": "Derecho uso al recurso hidrico",
            "descripcion": "Fotocopia de actas"
        }
    ]
}