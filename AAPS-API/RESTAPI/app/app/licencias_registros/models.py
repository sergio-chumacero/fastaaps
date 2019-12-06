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
          
# Epsa Registro - Documentos de Acreditación
class ErDocumentoAcreditacion(BaseModel):
    """
    Modelo para el campo 'documentos_acreditacion' del modelo 'EpsaRegistro'. 
    """
    tipo : str = Field(
        ..., # Campo requerido
        description = "Tipo del documento de acreditación. Campo requerido. Corresponde a la columna 'tipo_documento_acreditacion' de la tabla 'tipo_acreditacion' en el SIIRAyS.",
    ) # Observaciones: Tres opciones '-', 'Derecho al recurso hidrico' y 'Persona colectiva'. No existen datos en blanco.
    descripcion : str = Field(
        ..., # Campo requerido
        description = "Descripción del documento de acreditación. Campo requerido. Corresponde a la columna 'descripcion_acreditacion' de la tabla 'tipo_acreditacion' en el SIIRAyS.",
    ) # Observaciones: 13 opciones. No existen datos en blanco.

    # Configuración del Modelo
    class Config:
        title = "EPSA Registro - Documento de Acreditación" # Título para JSON-Schema

        anystr_strip_whitespace = True        # Espacios en blanco al comienzo y final serán removidos
        validate_all = True                   # Valores por defecto serán validados
        extra = "ignore"                      # Campos adicionales serán ignorados
        allow_mutation = True                 # Modelo es mutable (sus propiedades pueden ser cambiadas)
        use_enum_values = True                # Campos con enumeraciones usarán valores en vez de objetos Enum
        validate_assignment = True            # Cambios de atributos serán validados
        allow_population_by_field_name = True # Campos con alias pueden ser especificados por el nombre del campo

# Epsa Registro - Información Demográfica de Cobertura
class ErDemografiaCobertura(BaseModel):
    """
    Modelo para el campo 'demografia_cobertura' del modelo 'EpsaRegistro'. 
    """
    localidad : str = Field(
        ..., # Campo requerido
        description = "Nombre de la Localidad. Campo requerido.  Corresponde a la columna 'localidad' de la tabla 'localidad' en el SIIRAyS.",
    ) # Observaciones: Todas las columnas de la tabla 'demografia_cobertura' tienen un valor en 'id_localidad'. El nombre va en mayúsculas.
    poblacion_total : int = Field(
        default = None, # Campo opcional
        description = "Población. Corresponde a la columna 'poblacion_total' de la tabla 'demografia_cobertura' en el SIIRAyS.",
    )
    poblacion_atendida_ap : int = Field(
        default = None, # Campo opcional
        description = "Población atendida con servicio de agua potable. Corresponde a la columna 'poblacion_atendida_ap' de la tabla 'demografia_cobertura' en el SIIRAyS.",
    )
    numero_viviendas_ap : int = Field(
        default = None, # Campo opcional
        description = "Número de viviendas con servicio de agua potable. Corresponde a la columna 'numero_viviendas_ap' de la tabla 'demografia_cobertura' en el SIIRAyS.",
    )
    porcentaje_cobertura_ap : float = Field(
        default = None, # Campo opcional
        description = "Porcentaje de cobertura de agua potable. Corresponde a la columna 'porcentaje_cobertura_ap' de la tabla 'demografia_cobertura' en el SIIRAyS.",
    )
    poblacion_atendida_as : int = Field(
        default = None, # Campo opcional
        description = "Población atendida con servicio de alcantarillado sanitario. Corresponde a la columna 'poblacion_atendida_as' de la tabla 'demografia_cobertura' en el SIIRAyS.",
    )
    numbero_viviendas_as : int = Field(
        default = None, # Campo opcional
        description = "Número de viviendas con servicio de alcantarillado sanitario. Corresponde a la columna 'numero_viviendas_as' de la tabla 'demografia_cobertura' en el SIIRAyS.",
    ) # Observaciones: Nombre del campo en SIIRAyS con error: NUMBERO. Se mantiene por defecto.
    porcentaje_cobertura_ap : float = Field(
        default = None, # Campo opcional
        description = "Porcentaje de cobertura de alcantarillado sanitario. Corresponde a la columna 'porcentaje_cobertura_as' de la tabla 'demografia_cobertura' en el SIIRAyS.",
    )
    porcentaje_cobertura_ptar : float = Field(
        default = None, # Campo opcional
        description = "Porcentaje de cobertura de plantas de tratamiento de aguas residuales. Corresponde a la columna 'porcentaje_cobertura_ptar' de la tabla 'demografia_cobertura' en el SIIRAyS.",
    )

    # Configuración del Modelo
    class Config:
        title = "EPSA Registro - Información Demográfica de Cobertura" # Título para JSON-Schema

        anystr_strip_whitespace = True        # Espacios en blanco al comienzo y final serán removidos
        validate_all = True                   # Valores por defecto serán validados
        extra = "ignore"                      # Campos adicionales serán ignorados
        allow_mutation = True                 # Modelo es mutable (sus propiedades pueden ser cambiadas)
        use_enum_values = True                # Campos con enumeraciones usarán valores en vez de objetos Enum
        validate_assignment = True            # Cambios de atributos serán validados
        allow_population_by_field_name = True # Campos con alias pueden ser especificados por el nombre del campo

# Epsa Registro - Instalación
class ErInstalacion(BaseModel):
    """
    Modelo para el campo 'instalaciones' del modelo 'EpsaRegistro'. 
    """
    tipo : str = Field(
        default = None, # Campo opcional
        description = "Nombre de la instalación. Corresponde a la columna 'tipo_fuente' de la tabla 'tipo_fuente' en el SIIRAyS.",
    ) # Observaciones: Existen instalaciones sin valor en el campo 'tipo'.  
    estado : str = Field(
        default = None, # Campo opcional
        description = "Estado de la instalación. Corresponde a la columna 'estado_fuente' de la tabla 'estado_fuente' en el SIIRAyS.",
    ) # Observaciones: Existen instalaciones sin valor en el campo 'estado'.
    edad : int = Field(
        default = None, # Campo opcional
        description = "Edad de la instalación. Corresponde a la columna 'edad_fuente' de la tabla 'instalacion' en el SIIRAyS.",
    ) # Observaciones: Existen instalaciones sin valor en el campo 'edad'.
    
    # Configuración del Modelo
    class Config:
        title = "EPSA Registro - Instalación" # Título para JSON-Schema

        anystr_strip_whitespace = True        # Espacios en blanco al comienzo y final serán removidos
        validate_all = True                   # Valores por defecto serán validados
        extra = "ignore"                      # Campos adicionales serán ignorados
        allow_mutation = True                 # Modelo es mutable (sus propiedades pueden ser cambiadas)
        use_enum_values = True                # Campos con enumeraciones usarán valores en vez de objetos Enum
        validate_assignment = True            # Cambios de atributos serán validados
        allow_population_by_field_name = True # Campos con alias pueden ser especificados por el nombre del campo

# Epsa Registro - Información Técnica
class ErInformacionTecnica(BaseModel):
    """
    Modelo para el campo 'informacion_tecnica' del modelo 'EpsaRegistro'. 
    """
    numero_conexiones_ap : int = Field(
        default = None, # Campo opcional
        description = "Nombre de la instalación. Corresponde a la columna 'tipo_fuente' de la tabla 'tipo_fuente' en el SIIRAyS.",
    )
    numero_piletas_publicas : int = Field(
        default = None, # Campo opcional
        description = "Estado de la instalación. Corresponde a la columna 'estado_fuente' de la tabla 'estado_fuente' en el SIIRAyS.",
    )
    numero_conexions_as : int = Field(
        default = None, # Campo opcional
        description = "Edad de la instalación. Corresponde a la columna 'edad_fuente' de la tabla 'instalacion' en el SIIRAyS.",
    ) # Observaciones: Error de nombre (CONEXIONS).
    numero_camaras_septicas_domiciliarias : int = Field(
        default = None, # Campo opcional
        description = "Edad de la instalación. Corresponde a la columna 'edad_fuente' de la tabla 'instalacion' en el SIIRAyS.",
    )
    numero_letrinas : int = Field(
        default = None, # Campo opcional
        description = "Edad de la instalación. Corresponde a la columna 'edad_fuente' de la tabla 'instalacion' en el SIIRAyS.",
    )
    numero_banios_publicos : int = Field(
        default = None, # Campo opcional
        description = "Edad de la instalación. Corresponde a la columna 'edad_fuente' de la tabla 'instalacion' en el SIIRAyS.",
    )
    pozo_ciego : int = Field(
        default = None, # Campo opcional
        description = "Edad de la instalación. Corresponde a la columna 'edad_fuente' de la tabla 'instalacion' en el SIIRAyS.",
    )
    numero_conexiones_ap_medidor : int = Field(
        default = None, # Campo opcional
        description = "Edad de la instalación. Corresponde a la columna 'edad_fuente' de la tabla 'instalacion' en el SIIRAyS.",
    )
    dotacion_per_capita : int = Field(
        default = None, # Campo opcional
        description = "Edad de la instalación. Corresponde a la columna 'edad_fuente' de la tabla 'instalacion' en el SIIRAyS.",
    )
    continuidad_servicio_ap : int = Field(
        default = None, # Campo opcional
        description = "Edad de la instalación. Corresponde a la columna 'edad_fuente' de la tabla 'instalacion' en el SIIRAyS.",
    )
    continuidad_servicio_epoca_seca : int = Field(
        default = None, # Campo opcional
        description = "Edad de la instalación. Corresponde a la columna 'edad_fuente' de la tabla 'instalacion' en el SIIRAyS.",
    )
    porcentaje_perdida_red : int = Field(
        default = None, # Campo opcional
        description = "Edad de la instalación. Corresponde a la columna 'edad_fuente' de la tabla 'instalacion' en el SIIRAyS.",
    ) # Observaciones: Columna de porcentajes sólo acepta valores enteros (int) y EPSA con id 4004 tiene un valor de 34023.

    # Configuración del Modelo
    class Config:
        title = "EPSA Registro - Información Técnica" # Título para JSON-Schema

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
    documentos_acreditacion : List[ErDocumentoAcreditacion] = Field(
        default = None,
        description = "Información de los documentos de acreditación de la EPSA. Estos datos corresponden a las tablas 'documento_acreditacion' y 'tipo_acreditacion'."
    ) # Observaciones: Es posible (y común) tener múltiples documentos de acreditación por EPSA.
    demografia_cobertura : List[ErDemografiaCobertura] = Field(
        default = None, # Campo opcional
        description = "Información demográfica de cobertura de la EPSA. Estos datos corresponden a las tablas 'demografia_cobertura' y 'localidad' en el SIIRAyS."
    ) # Observaciones: Es posible que una EPSA tenga múltiples datos de información demográfica de cobertura.
    instalaciones : List[ErInstalacion] = Field(
        default = None, # Campo opcional
        description = "Información de instalaciones. Estos datos corresponden a las tablas 'instalacion', 'tipo_fuente', 'rar' y 'estado_fuente' del SIIRAyS."
    ) # Observaciones: Cualquier permutación de los campos de una instalación pueden estar en blanco.
    informacion_tecnica : ErInformacionTecnica = Field(
        default = None, # Campo opcional
        description = "Información técnica de la EPSA. Estos datos corresponden a las tabla 'informacion_tecnica' del SIIRAyS."
    ) # Observaciones: Algunas EPSA tienen datos de información técnica duplicados. En este caso se toma sólamente uno. 

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
    ],
    "demografia_cobertura": [
        {
            "localidad": "AGUAQUIZA",
            "poblacion_total": 135,
            "poblacion_atendida_ap": 135.0,
            "numero_viviendas_ap": 27.0,
            "porcentaje_cobertura_ap": 100.0,
            "poblacion_atendida_as": None,
            "numbero_viviendas_as": None,
            "porcentaje_cobertura_as": None,
            "porcentaje_cobertura_ptar": None
        }
    ],
    "instalaciones": [
        {
            "tipo": "Fuentes de abastecimiento",
            "estado": "REGULAR",
            "edad": 240.0
        },
        {
            "tipo": "Fuentes de abastecimiento",
            "estado": "BUENO",
            "edad": 48.0
        },
        {
            "tipo": "Tanque de Almacenamiento",
            "estado": "MALO",
            "edad": 240.0
        },
        {
            "tipo": "Red de distribución",
            "estado": "REGULAR",
            "edad": 240.0
        },
        {
            "tipo": "Aduccion",
            "estado": "REGULAR",
            "edad": 240.0
        }
    ],
    "informacion_tecnica": {
        "numero_conexiones_ap": 27.0,
        "numero_piletas_publicas": 2.0,
        "numero_conexions_as": None,
        "numero_camaras_septicas_domiciliarias": None,
        "numero_letrinas": 5.0,
        "numero_banios_publicos": None,
        "pozo_ciego": None,
        "numero_conexiones_ap_medidor": 0.0,
        "dotacion_per_capita": 0.0,
        "continuidad_servicio_ap": 0,
        "continuidad_servicio_epoca_seca": 0.0,
        "porcentaje_perdida_red": 0
    }
}