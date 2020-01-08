###################################################################
# Título:      Tareas de Celery
# Ubicación:   FASTAAPS/AAPS-DATA/SYNC/app/tasks.py
# Descripción: 
#   Tareas de la aplicación Celery:
#     - Recuperación de datos de la base de datos del SIIRAyS
#     - Transformación de los datos al formato JSON
#     - Ingreso de estos datos al sistema FASTAAPS vía su REST-API
###################################################################

# Dependencias
from .main import app         # Aplicación principal Celery
import os                     # Manejo de sistema operativo
from os.path import join, exists
import time                   # Manejo de tiempo
from datetime import datetime # Manejo de objetos Fecha/Hora
import json                   # Manejo de archivos en formato JSON
import csv                    # Manejo de archivos en formato CSV
import psycopg2 as pg         # Driver de PostgreSQL
from celery.utils.log import get_task_logger # Herramienta de registro (logger)
import requests               # Cliente HTTP

# Configuración: Variables de Ambiente 
PGDB_HOST = os.environ.get("PGDB_HOST") # Dirección URL del daemon PostgreSQL
PGDB_PORT = os.environ.get("PGDB_PORT") # Puerto donde escucha el daemon PostgreSQL 
PGDB_USER = os.environ.get("PGDB_USER") # Nombre de usuario de la base de datos
PGDB_PASS = os.environ.get("PGDB_PASS") # Contraseña del usuario
PGDB_NAME = os.environ.get("PGDB_NAME") # Nombre de la base de datos

# Inicialización de herramienta de registro
logger = get_task_logger(__name__)

# Dirección del directorio actual + directorio para csv's
curr_dir = os.getcwd()
datasets_dir_name = "sheets"

if not exists(join(curr_dir,datasets_dir_name)):
    os.makedirs(join(curr_dir,datasets_dir_name))

# Funciones de apoyo
def list_cursor_to_data(cursor=None, data=None, cols=None, key=None, db_tag=None):
    """
    Agrega los datos de un 'cursor' a los datos de EPSA como lista de objetos.
    """
    if not (cursor or data or cols or key or db_tag):
        return
    with open(join(curr_dir,datasets_dir_name,f"{key}_{db_tag}.csv"), "w+", newline="", encoding="utf-8") as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(cols)

        for row in cursor:
            epsa_obj = data.get(row[0])
            if not epsa_obj: continue
            obj = {cn:val for cn,val in zip(cols[1:],row[1:]) if val}
            if key in epsa_obj.keys():
                epsa_obj[key].append(obj)
            else:
                epsa_obj[key] = [obj]
            
            csv_writer.writerow(row) 

def dict_cursor_to_data(cursor=None, data=None, cols=None, key=None, db_tag=None):
    """
    Agrega los datos de un 'cursor' a los datos de EPSA como objeto.
    """
    if not (cursor or data or cols or key or db_tag):
        return
    with open(join(curr_dir,datasets_dir_name,f"{key}_{db_tag}.csv"), "w+", newline="", encoding="utf-8") as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(cols)

        for row in cursor:
            epsa_obj = data.get(row[0])
            if not epsa_obj: continue
            epsa_obj[key] = {cn:val for cn,val in zip(cols[1:],row[1:]) if val} 

            csv_writer.writerow(row)

def str_cursor_to_data(cursor=None, data=None, key=None, db_tag=None):
    """
    Agrega los datos de un 'cursor' a los datos de EPSA como texto.
    """
    if not (cursor or data or key or db_tag):
        return
    with open(join(curr_dir,datasets_dir_name,f"{key}_{db_tag}.csv"), "w+", newline="", encoding="utf-8") as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(["id_epsa",key])
        
        for row in cursor:
            epsa_obj = data.get(row[0])
            if not epsa_obj: continue
            epsa_obj[key] = row[1]

            csv_writer.writerow(row)

def plain_list_cursor_to_data(cursor=None, data=None, key=None, db_tag=None):
    """
    Agrega los datos de un 'cursor' a los datos de EPSA como una lista plana.
    """
    if not (cursor or data or key or db_tag):
        return
    with open(join(curr_dir,datasets_dir_name,f"{key}_{db_tag}.csv"), "w+", newline="", encoding="utf-8") as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(["id_epsa",key])

        for row in cursor:
            epsa_obj = data.get(row[0])
            if not epsa_obj: continue
            if key in epsa_obj.keys():
                epsa_obj[key].append(row[1])
            else:
                epsa_obj[key] = [row[1]]
            
            csv_writer.writerow(row)

# Establece una conección con el servidor PostgreSQL
def init_db_connection():
    """
    Establece y retorna una conexión con la base de datos PostgreSQL.
    Reporta las propiedades de la conexión a la base de datos y la versión de PostgreSQL.
    """
    db_connection = None
    cursor = None
    try:
        db_connection = pg.connect(
            host = PGDB_HOST,
            port = PGDB_PORT,
            user = PGDB_USER,
            password = PGDB_PASS,
            database = PGDB_NAME,
        )
        logger.info("Propiedades de la conexión:\n")
        logger.info(json.dumps(
            db_connection.get_dsn_parameters(),
            indent = 2,
            ensure_ascii = False,
        ))
        cursor = db_connection.cursor()
        cursor.execute("SELECT version();")
        record = cursor.fetchone()
        logger.info(f"Versión PostgreSQL: {record}\n")
    except (Exception, pg.Error) as error:
        logger.error(f"Error al establecer de la conexión. {error}\n")
    finally:
        if cursor: 
            cursor.close()
    return db_connection

# Recuperar datos generales de EPSA
def retrieve_epsa(connection, result_obj, db_tag):
    """
    Recupera datos de las tablas 'epsa' y 'rar' y retorna datos de EPSA base.
    """
    # Columnas SIIRAyS
    epsa_cols = [
        "id_epsa", "codigo_epsa", "sigla_epsa",
        "nombre_epsa", "telefonos", "fax",
        "correo_electronico", "direccion", "web", 
        "observacion"
    ]
    
    # Tablas y Columnas para la consulta SQL
    epsa_select = ",".join([f"epsa.{col}" for col in epsa_cols])
    
    # Nombres de atributos FASTAAPS
    cols = [
        "id_siirays", "codigo", "sigla",
        "nombre", "telefonos", "fax",
        "correo_electronico", "direccion", "web",
        "observacion"
    ]
    epsa_data = {}
    cursor = None
    try:
        # Ejecutar consulta SQL: Recuperar datos
        cursor = connection.cursor()
        cursor.execute(f"""SELECT {epsa_select} 
        FROM epsa
        """)
        
        with open(join(curr_dir,datasets_dir_name,f"informacion_general_{db_tag}.csv"),"w+",newline="",encoding="utf-8") as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(cols)
            for row in cursor:
                epsa_data[row[0]] = {"informacion_general": {col:val for col,val in zip(cols,row) if val}}
                csv_writer.writerow(row)
        
        result_obj["epsa"] = "ok" 
    except (Exception, pg.Error) as e:
        logger.error(f"Error al recuperar datos de la tabla 'epsa'. {e}\n")
        result_obj["epsa"] = "error"
    finally:
        if cursor:
            cursor.close()
    return epsa_data

# Recuperar datos de Representante Legal
def retrieve_representante(connection, epsa_data, result_obj, db_tag):
    """
    Recupera datos de las tabla "representante", "rar", "tipo_contacto" y los añade a los datos de EPSA base. 
    """
    # Nombres de columnas SIIRAyS
    representante_cols = ["id_epsa", "nombre_representante","cargo","telefono", "celular","correo"]
    rar_cols = ["numero_resolucion","fecha_resolucion","descripcion_resolucion"]
    tipo_contacto_cols = ["tipo_contacto"]
    
    # Tablas y Columnas para la consulta SQL
    representante_select = ",".join(
        [f"representante.{col}" for col in representante_cols] +
        [f"rar.{col}" for col in rar_cols] +
        [f"tipo_contacto.{col}" for col in tipo_contacto_cols]
    )
    # Nombres de atributos FASTAAPS
    cols = [
        "id_epsa","nombre","cargo","telefono","celular","correo",
        "numero_resolucion","fecha_resolucion","descripcion_resolucion",
        "tipo_contacto",
    ]
    try:
        # Ejecutar consulta SQL: Recuperar datos
        cursor = connection.cursor()
        cursor.execute(f"""SELECT {representante_select}
        FROM representante
        LEFT OUTER JOIN rar ON representante.id_rar = rar.id_rar
        LEFT OUTER JOIN tipo_contacto ON representante.id_tipo_contacto = tipo_contacto.id_tipo_contacto
        """)

        list_cursor_to_data(cursor=cursor, data=epsa_data, cols=cols, key="representante", db_tag=db_tag)
    
        result_obj["representante"] = "ok"
    except (Exception, pg.Error) as e:
        logger.error(f"Error al recuperar datos de la tabla 'representante'. {e}\n")
        result_obj["representante"] = "error"
    finally:
        if cursor:
            cursor.close()

# Recuperar datos de Ubicación Geográfica
def retrieve_ubicacion(connection, epsa_data, result_obj, db_tag):
    """
    Recupera datos de las tablas "ubicacion" y "localidad" y los añade a los datos de EPSA  base. 
    """
    # Nombres de columnas SIIRAyS y atributos FASTAAPS
    ubicacion_cols = ["id_epsa"]
    localidad_cols = [
        "codigo_ine","cod_departamento","departamento","cod_provincia","provincia",
        "cod_municipio","municipio","cod_comunidad","comunidad","latitud","longitud","localidad",
    ]
    
    # Tablas y Columnas para la consulta SQL
    ubicacion_select = ",".join(
        [f"ubicacion.{col}" for col in ubicacion_cols] + 
        [f"localidad.{col}" for col in localidad_cols]
    )
    try:
        # Ejecutar consulta SQL: Recuperar datos
        cursor = connection.cursor()
        cursor.execute(f"""SELECT {ubicacion_select}
        FROM ubicacion LEFT OUTER JOIN localidad ON ubicacion.id_localidad = localidad.id_localidad
        """)

        cols = ubicacion_cols + localidad_cols
        list_cursor_to_data(cursor=cursor, data=epsa_data, cols=cols, key="ubicacion", db_tag=db_tag)
        
        result_obj["ubicacion"] = "ok"
    except (Exception, pg.Error) as error:
        logger.error(f"Error al recuperar datos de las tablas 'ubicacion' y 'localidad'. {error}\n")
        result_obj["ubicacion"] = "error"
    finally:
        if cursor:
            cursor.close()

# Recuperar datos de Estatus Jurídico 
def retrieve_estatus_juridico(connection, epsa_data, result_obj, db_tag):
    """
    Recupera datos de las tablas "entidad" y "estatus_juridico" y los añade a los datos de EPSA  base. 
    """
    # Nombres de columnas SIIRAyS y atributos FASTAAPS
    estatus_juridico_cols = ["id_epsa","numero_resolucion","fecha_resolucion"]
    entidad_cols = ["nombre_entidad","sigla_entidad","direccion","telefonos","fax","web","correo_electronico"]
    # Tablas y Columnas para la consulta SQL
    estatus_juridico_select = ",".join(
        [f"estatus_juridico.{col}" for col in estatus_juridico_cols] + 
        [f"entidad.{col}" for col in entidad_cols]
    )
    try:
        # Ejecutar consulta SQL: Recuperar datos
        cursor = connection.cursor()
        cursor.execute(f"""SELECT {estatus_juridico_select}
        FROM estatus_juridico LEFT OUTER JOIN entidad ON estatus_juridico.id_entidad = entidad.id_entidad
        """)
        
        cols = estatus_juridico_cols + entidad_cols
        dict_cursor_to_data(cursor=cursor, data=epsa_data, cols=cols, key="estatus_juridico", db_tag=db_tag)
        
        result_obj["estatus_juridico"] = "ok"
    except (Exception, pg.Error) as error:
        logger.error(f"Error al recuperar datos de las tablas 'estatus_juridico' y 'entidad'. {error}\n")
        result_obj["estatus_juridico"] = "error"
    finally:
        if cursor:
            cursor.close()

# Recuperar datos de Documentos de Acreditación          
def retrieve_documento_acreditacion(connection, epsa_data, result_obj, db_tag):
    """
    Recupera datos de las tablas "documento_acreditacion" y "tipo_acreditacion" y los añade a los datos de EPSA base.
    """
    # Nombres de columnas en SIIRAyS
    documento_acreditacion_cols = ["id_epsa"]
    tipo_acreditacion_cols = ["tipo_documento_acreditacion","descripcion_acreditacion"]
    # Tablas y Columnas para la consulta SQL
    documento_acreditacion_select = ",".join(
        [f"documento_acreditacion.{col}" for col in documento_acreditacion_cols] +
        [f"tipo_acreditacion.{col}" for col in tipo_acreditacion_cols]
    )
    # Nombres de columnas en FASTAAPS
    cols = ["id_epsa","tipo","descripcion"]
    try:
        # Ejecutar consulta SQL: Recuperar datos
        cursor = connection.cursor()
        cursor.execute(f"""SELECT {documento_acreditacion_select}
        FROM documento_acreditacion
        LEFT OUTER JOIN tipo_acreditacion ON documento_acreditacion.id_tipo_acreditacion = tipo_acreditacion.id_tipo_acreditacion 
        """)

        list_cursor_to_data(cursor=cursor, data=epsa_data, cols=cols, key="documentos_acreditacion", db_tag=db_tag)

        result_obj["documento_acreditacion"] = "ok"
    except (Exception, pg.Error) as error:
        logger.error(f"Error al recuperar datos de las tablas 'documento_acreditacion' y 'tipo_acreditacion'. {error}\n")
        result_obj["documento_acreditacion"] = "error"
    finally:
        if cursor:
            cursor.close()

# Recuperar datos demográficos de Cobertura 
def retrieve_demografia_cobertura(connection, epsa_data, result_obj, db_tag):
    """
    Recupera datos de la tabla 'demografia_cobertura' y 'localidad' y los añade a los datos de EPSA base.
    """
    # Nombres de las columnas en SIIRAyS
    demografia_cobertura_cols = [
        "id_epsa","poblacion_total",
        "poblacion_atendida_ap","numero_viviendas_ap","porcentaje_cobertura_ap",
        "poblacion_atendida_as","numero_viviendas_as","porcentaje_cobertura_as",
        "porcentaje_cobertura_ptar",
    ]
    localidad_cols = ["localidad"]
    # Tablas y Columnas para la consulta SQL
    demografia_cobertura_select = ",".join(
        [f"demografia_cobertura.{col}" for col in demografia_cobertura_cols] +
        [f"localidad.{col}" for col in localidad_cols]
    )
    # Nombres de columnas en FASTAAPS
    cols = [
        "id_epsa","poblacion_total",
        "poblacion_atendida_ap","numero_viviendas_ap","porcentaje_cobertura_ap",
        "poblacion_atendida_as","numbero_viviendas_as","porcentaje_cobertura_as",
        "porcentaje_cobertura_ptar", "localidad"
    ]
    try:
        # Ejecutar consulta SQL: Recuperar datos
        cursor = connection.cursor()
        cursor.execute(f"""SELECT {demografia_cobertura_select}
        FROM demografia_cobertura LEFT OUTER JOIN localidad ON demografia_cobertura.id_localidad = localidad.id_localidad
        """)

        list_cursor_to_data(cursor=cursor, data=epsa_data, cols=cols, key="demografia_cobertura", db_tag=db_tag)
        
        result_obj["demografia_cobertura"] = "ok"
    except (Exception, pg.Error) as error:
        logger.error(f"Error al recuperar datos de las tablas 'demografia_cobertura' y 'localidad'. {error}\n")
        result_obj["demografia_cobertura"] = "error"
    finally:
        if cursor:
            cursor.close()

# Recuperar datos de Instalaciones
def retrieve_instalacion(connection, epsa_data, result_obj, db_tag):
    """
    Recupera datos de las tablas 'instalacion', 'tipo_fuente' y 'estado_fuente'
    y los añade a los datos de EPSA base.
    """
    # Nombres de las columnas en SIIRAyS
    instalacion_cols = ["id_epsa","id_instalacion","edad_fuente"]
    tipo_fuente_cols = ["descripcion_tipo_fuente"]
    estado_fuente_cols = ["estado_fuente"]
    
    # Tablas y Columnas para la consulta SQL
    instalacion_select = ",".join(
        [f"instalacion.{col}" for col in instalacion_cols] +
        [f"tipo_fuente.{col}" for col in tipo_fuente_cols] +
        [f"estado_fuente.{col}" for col in estado_fuente_cols]
    )
    # Nombres de columnas SIIRAyS y atributos FASTAAPS
    cols = ["id_epsa","id_instalacion","edad","tipo", "estado",]
    try:
        # Ejecutar consulta SQL: Recuperar datos
        cursor = connection.cursor()
        cursor.execute(f"""SELECT {instalacion_select}
        FROM instalacion
        LEFT OUTER JOIN tipo_fuente ON instalacion.id_tipo_fuente = tipo_fuente.id_tipo_fuente
        LEFT OUTER JOIN estado_fuente ON instalacion.id_estado_fuente = estado_fuente.id_estado_fuente
        """)
        
        list_cursor_to_data(cursor=cursor, data=epsa_data, cols=cols, key="instalaciones", db_tag=db_tag)

        result_obj["instalacion"] = "ok"
    except (Exception, pg.Error) as error:
        logger.error(f"Error al recuperar datos de las tablas 'instalacion', 'tipo_fuente', 'estado_fuente'. {error}\n")
        result_obj["instalacion"] = "error"
    finally:
        if cursor:
            cursor.close()

# Recuperar datos de Fuentes de Financiamiento
def retrieve_fuente_financiamiento(connection, epsa_data, result_obj, db_tag):
    """
    Recupera datos de las tablas 'instalacion_fuente_financiamiento' y 'fuente_financiamiento'
    y los añade a los datos de EPSA base.
    """
    # Nombres de las columnas en SIIRAyS
    instalacion_fuente_financiamiento_cols = ["id_epsa","id_instalacion","porcentaje_credito","porcentaje_donacion","porcentaje_aporte_propio","porcentaje_otros"]
    fuente_financiamiento_cols = ["fuente_financiamiento","descripcion_fuente_financiamien"]
    
    # Tablas y Columnas para la consulta SQL
    fuente_financiamiento_select = ",".join(
        [f"instalacion_fuente_financiamiento.{col}" for col in instalacion_fuente_financiamiento_cols] +
        [f"fuente_financiamiento.{col}" for col in fuente_financiamiento_cols]
    )
    # Nombres de columnas SIIRAyS y atributos FASTAAPS
    cols = [
        "id_epsa","id_instalacion","porcentaje_credito", "porcentaje_donacion", "porcentaje_aporte_propio", "porcentaje_otros",
        "nombre","descripcion",
    ]
    try:
        # Ejecutar consulta SQL: Recuperar datos
        cursor = connection.cursor()
        cursor.execute(f"""SELECT {fuente_financiamiento_select}
        FROM instalacion_fuente_financiamiento LEFT OUTER JOIN fuente_financiamiento
        ON instalacion_fuente_financiamiento.id_fuente_financiamiento = fuente_financiamiento.id_fuente_financiamiento
        """)
        
        with open(join(curr_dir,datasets_dir_name,f"fuente_financiamiento_{db_tag}.csv"), "w+", newline="", encoding="utf-8") as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(cols)
        
            for row in cursor:
                epsa_obj = epsa_data.get(row[0])
                if not (epsa_obj and "instalaciones" in epsa_obj.keys()): continue

                for instalacion in epsa_obj["instalaciones"]:
                    id_instalacion = instalacion.get("id_instalacion")                
                    if not (id_instalacion and id_instalacion == row[1]): continue
                    instalacion["fuente_financiamiento"] = {cn:val for cn,val in zip(cols[2:],row[2:]) if not val is None}
                
                csv_writer.writerow(row)
        
        result_obj["fuente_financiamiento"] = "ok"
    except (Exception, pg.Error) as error:
        logger.error(f"Error al recuperar datos de las tablas 'instalacion_fuente_financiamiento' y 'fuente_financiamiento'. {error}\n")
        result_obj["fuente_financiamiento"] = "error"
    finally:
        if cursor:
            cursor.close()

# Recuperar datos de Información Técnica
def retrieve_informacion_tecnica(connection, epsa_data, result_obj, db_tag):
    """
    Recupera datos de las tabla 'informacion_tecnica' y los añade a los datos de EPSA base.
    """
    # Nombres de columnas SIIRAyS y atributos FASTAAPS
    cols = [
        "id_epsa","numero_conexiones_ap","numero_piletas_publicas","numero_conexions_as",
        "numero_camaras_septicas_domiciliarias", "numero_letrinas","numero_banios_publicos",
        "pozo_ciego","numero_conexiones_ap_medidor","dotacion_per_capita","continuidad_servicio_ap",
        "continuidad_servicio_epoca_seca","porcentaje_perdida_red",
    ]
    # Columnas para la consulta SQL
    informacion_tecnica_select = ",".join([f"informacion_tecnica.{col}" for col in cols])
    try:
        # Ejecutar consulta SQL: Recuperar datos
        cursor = connection.cursor()
        cursor.execute(f"SELECT {informacion_tecnica_select} FROM informacion_tecnica")
        
        dict_cursor_to_data(cursor=cursor, data=epsa_data, cols=cols, key="informacion_tecnica", db_tag=db_tag)

        result_obj["informacion_tecnica"] = "ok"
    except (Exception, pg.Error) as error:
        logger.error(f"Error al recuperar datos de las tabla 'informacion_tecnica'. {error}\n")
        result_obj["informacion_tecnica"] = "error"
    finally:
        if cursor:
            cursor.close()

# Recuperar datos de Problemas de Contaminación de Fuentes
def retrieve_problemas_contaminacion(connection, epsa_data, result_obj, db_tag):
    """
    Recupera datos de las tabla 'problemas_contaminacion' y los añade a los datos de EPSA base.
    """
    # Nombres de columnas SIIRAyS y atributos FASTAAPS
    problemas_contaminacion_cols = ["id_epsa","descripcion"]
    
    # Tablas y Columnas para la consulta SQL
    problemas_contaminacion_select = ",".join([f"problemas_contaminacion.{col}" for col in problemas_contaminacion_cols])
    
    try:
        # Ejecutar consulta SQL: Recuperar datos
        cursor = connection.cursor()
        cursor.execute(f"SELECT {problemas_contaminacion_select} FROM problemas_contaminacion")

        str_cursor_to_data(cursor=cursor, data=epsa_data, key="problemas_contaminacion", db_tag=db_tag)
        
        result_obj["problemas_contaminacion"] = "ok"
    except (Exception, pg.Error) as error:
        logger.error(f"Error al recuperar datos de la tabla 'problemas_contaminacion'. {error}\n")
        result_obj["problemas_contaminacion"] = "error"
    finally:
        if cursor:
            cursor.close()

# Recuperar datos de Sistemas de Agua Potable
def retrieve_sistema_ap(connection, epsa_data, result_obj, db_tag):
    """
    Recupera datos de las tablas 'sistema_ap' y 'tipo_sistema_ap' y los añade a los datos de EPSA base.
    """
    # Nombres de columnas SIIRAyS
    sistema_ap_cols = ["id_epsa"]
    tipo_sistema_ap_cols = ["descripcion_tipo_sistema_ap"]
    
    # Tablas y Columnas para la consulta SQL
    sistema_ap_select = ",".join(
        [f"sistema_ap.{col}" for col in sistema_ap_cols] +
        [f"tipo_sistema_ap.{col}" for col in tipo_sistema_ap_cols]
    )
    try:
        # Ejecutar consulta SQL: Recuperar datos
        cursor = connection.cursor()
        cursor.execute(f"""SELECT {sistema_ap_select} 
        FROM sistema_ap LEFT OUTER JOIN tipo_sistema_ap
        ON sistema_ap.id_tipo_sistema_ap = tipo_sistema_ap.id_tipo_sistema_ap 
        """)
        
        plain_list_cursor_to_data(cursor=cursor, data=epsa_data, key="sistema_ap", db_tag=db_tag)

        result_obj["sistema_ap"] = "ok"
    except (Exception, pg.Error) as error:
        logger.error(f"Error al recuperar datos de las tablas 'sistema_ap' y 'tipo_sistema_ap'. {error}\n")
        result_obj["sistema_ap"] = "error"
    finally:
        if cursor:
            cursor.close()

# Recuperar datos de Tratamiento de Aguas Residuales
def retrieve_tratamiento_agua_residual(connection, epsa_data, result_obj, db_tag):
    """
    Recupera datos de las tablas 'tratamiento_agua_residual' y 'tipo_tratamiento_ar' y los añade a los datos de EPSA base.
    """
    # Nombres de columnas SIIRAyS
    tratamiento_agua_residual_cols = ["id_epsa","cantidad","instalada","operada","anio_inicio","coordenada_x","coordenada_y","coordenada_z","zona_utm"]
    tipo_tratamiento_ar_cols = ["descripcion_tratamiento"]
    
    # Tablas y Columnas para la consulta SQL
    tratamiento_agua_residual_select = ",".join(
        [f"tratamiento_agua_residual.{col}" for col in tratamiento_agua_residual_cols] +
        [f"tipo_tratamiento_ar.{col}" for col in tipo_tratamiento_ar_cols]
    )
    # Nombres de los atributos en FASTAAPS
    cols = ["id_epsa","cantidad","instalada","operada","anio_inicio","coordenada_x","coordenada_y","coordenada_z","zona_utm","tipo"]
    try:
        # Ejecutar consulta SQL: Recuperar datos
        cursor = connection.cursor()
        cursor.execute(f"""SELECT {tratamiento_agua_residual_select} 
        FROM tratamiento_agua_residual LEFT OUTER JOIN  tipo_tratamiento_ar
        ON tratamiento_agua_residual.id_tipo_tratamiento_ar = tipo_tratamiento_ar.id_tipo_tratamiento_ar 
        """)
        
        list_cursor_to_data(cursor=cursor, data=epsa_data, cols=cols, key="tratamiento_agua_residual", db_tag=db_tag)

        result_obj["tratamiento_agua_residual"] = "ok"
    except (Exception, pg.Error) as error:
        logger.error(f"Error al recuperar datos de las tablas 'tratamiento_agua_residual' y 'tipo_tratamiento_ar'. {error}\n")
        result_obj["tratamiento_agua_residual"] = "error"
    finally:
        if cursor:
            cursor.close()

# Recuperar datos de Tuberías 
def retrieve_tecnica_tuberia(connection, epsa_data, result_obj, db_tag):
    """
    Recupera datos de las tablas 'tecnica_tuberia', 'localidad', 'sector' y 'material_tuberia'
    y los añade a los datos de EPSA base.
    """
    # Nombres de columnas SIIRAyS
    tecnica_tuberia_cols = ["id_epsa","longitud_total"]
    localidad_cols = ["localidad"]
    sector_cols = ["sector"]
    material_tuberia_cols = ["material_tuberia"]
    
    # Tablas y Columnas para la consulta SQL
    tecnica_tuberia_select = ",".join(
        [f"tecnica_tuberia.{col}" for col in tecnica_tuberia_cols] +
        [f"localidad.{col}" for col in localidad_cols] +
        [f"sector.{col}" for col in sector_cols] +
        [f"material_tuberia.{col}" for col in material_tuberia_cols]
    )
    # Nombres de los atributos en FASTAAPS
    cols = ["id_epsa","longitud_total","localidad","sector","material"]
    try:
        # Ejecutar consulta SQL: Recuperar datos
        cursor = connection.cursor()
        cursor.execute(f"""SELECT {tecnica_tuberia_select} 
        FROM tecnica_tuberia
        LEFT OUTER JOIN localidad ON tecnica_tuberia.id_localidad = localidad.id_localidad
        LEFT OUTER JOIN sector ON tecnica_tuberia.id_sector = sector.id_sector
        LEFT OUTER JOIN material_tuberia ON tecnica_tuberia.id_material_tuberia = material_tuberia.id_material_tuberia
        """)

        list_cursor_to_data(cursor=cursor, data=epsa_data, cols=cols, key="tecnica_tuberia", db_tag=db_tag)

        result_obj["tecnica_tuberia"] = "ok"
    except (Exception, pg.Error) as error:
        logger.error(f"Error al recuperar datos de las tablas 'tecnica_tuberia', 'localidad', 'sector' y 'material_tuberia'. {error}\n")
        result_obj["tecnica_tuberia"] = "error"
    finally:
        if cursor:
            cursor.close()

# Recuperar datos de Sistema de Alcantarillado
def retrieve_tecnica_as(connection, epsa_data, result_obj, db_tag):
    """
    Recupera datos de las tablas 'tecnica_as' y 'opcion_tecnica' y los añade a los datos de EPSA base.
    """
    # Nombres de columnas SIIRAyS
    tecnica_as_cols = ["id_epsa"]
    opcion_tecnica_cols = ["opcion_tecnica"]
    
    # Tablas y Columnas para la consulta SQL
    tecnica_as_select = ",".join(
        [f"tecnica_as.{col}" for col in tecnica_as_cols] +
        [f"opcion_tecnica.{col}" for col in opcion_tecnica_cols]
    )
    try:
        # Ejecutar consulta SQL: Recuperar datos
        cursor = connection.cursor()
        cursor.execute(f"""SELECT {tecnica_as_select} 
        FROM tecnica_as LEFT OUTER JOIN opcion_tecnica
        ON tecnica_as.id_opcion_tecnica = opcion_tecnica.id_opcion_tecnica
        """)
        
        str_cursor_to_data(cursor=cursor, data=epsa_data, key="tecnica_as", db_tag=db_tag) 
    
        result_obj["tecnica_as"] = "ok"
    except (Exception, pg.Error) as error:
        logger.error(f"Error al recuperar datos de las tablas 'tecnica_as' y 'opcion_tecnica'. {error}\n")
        result_obj["tecnica_as"] = "error"
    finally:
        if cursor:
            cursor.close()

# Recuperar datos de Descarga de Alcantarillado Sanitario
def retrieve_descarga_ar(connection, epsa_data, result_obj, db_tag):
    """
    Recupera datos de las tablas 'descarga_ar' y 'cuerpo_receptor' y los añade a los datos de EPSA base.
    """
    # Nombres de columnas SIIRAyS
    descarga_ar_cols = ["id_epsa","nombre_cuerpo_receptor","coordenada_x","coordenada_y","zona_utm"]
    cuerpo_receptor_cols = ["cuerpo_receptor"]
    
    # Tablas y Columnas para la consulta SQL
    descarga_ar_select = ",".join(
        [f"descarga_ar.{col}" for col in descarga_ar_cols] +
        [f"cuerpo_receptor.{col}" for col in cuerpo_receptor_cols]
    )
    # Nombres de los atributos en FASTAAPS
    cols = ["id_epsa","cuerpo_receptor","coordenada_x","coordenada_y","zona_utm","tipo_cuerpo_receptor"]
    try:
        # Ejecutar consulta SQL: Recuperar datos
        cursor = connection.cursor()
        cursor.execute(f"""SELECT {descarga_ar_select} 
        FROM descarga_ar LEFT OUTER JOIN cuerpo_receptor
        ON descarga_ar.id_cuerpo_receptor = cuerpo_receptor.id_cuerpo_receptor
        """)
        
        list_cursor_to_data(cursor=cursor, data=epsa_data, cols=cols, key="descarga_ar", db_tag=db_tag)
        
        result_obj["descarga_ar"] = "ok"
    except (Exception, pg.Error) as error:
        logger.error(f"Error al recuperar datos de las tablas 'descarga_ar' y 'cuerpo_receptor'. {error}\n")
        result_obj["descarga_ar"] = "error"
    finally:
        if cursor:
            cursor.close()

# Recuperar datos de Funcionarios
def retrieve_funcionarios(connection, epsa_data, result_obj, db_tag):
    """
    Recupera datos de las tablas 'funcionarios' y 'tipo_funcionario' y los añade a los datos de EPSA base.
    """
    # Nombres de columnas SIIRAyS
    funcionarios_cols = ["id_epsa","numero_funcionarios"]
    tipo_funcionario_cols = ["tipo_funcionario"]
    
    # Tablas y Columnas para la consulta SQL
    funcionarios_select = ",".join(
        [f"funcionarios.{col}" for col in funcionarios_cols] +
        [f"tipo_funcionario.{col}" for col in tipo_funcionario_cols]
    )
    # Nombres de los atributos en FASTAAPS
    cols = ["id_epsa","numero_funcionarios","tipo_funcionario"]
    try:
        # Ejecutar consulta SQL: Recuperar datos
        cursor = connection.cursor()
        cursor.execute(f"""SELECT {funcionarios_select} 
        FROM funcionarios LEFT OUTER JOIN tipo_funcionario
        ON funcionarios.id_tipo_funcionario = tipo_funcionario.id_tipo_funcionario
        """)
        
        list_cursor_to_data(cursor=cursor, data=epsa_data, cols=cols, key="funcionarios", db_tag=db_tag)
        
        result_obj["funcionarios"] = "ok"
    except (Exception, pg.Error) as error:
        logger.error(f"Error al recuperar datos de las tablas 'funcionarios' y 'tipo_funcionario'. {error}\n")
        result_obj["funcionarios"] = "error"
    finally:
        if cursor:
            cursor.close()

# Recuperar datos de Ingresos
def retrieve_ingresos(connection, epsa_data, result_obj, db_tag):
    """
    Recupera datos de las tablas 'ingresos', 'tipo_ingreso' y 'periodo_pago'
    y los añade a los datos de EPSA base.
    """
    # Nombres de columnas SIIRAyS
    ingresos_cols = ["id_epsa","monto","observacion"]
    tipo_ingreso_cols = ["concepto"]
    periodo_pago_cols = ["periodo_pago"]
    
    # Tablas y Columnas para la consulta SQL
    ingresos_select = ",".join(
        [f"ingresos.{col}" for col in ingresos_cols] +
        [f"tipo_ingreso.{col}" for col in tipo_ingreso_cols] +
        [f"periodo_pago.{col}" for col in periodo_pago_cols]
    )
    # Nombres de los atributos en FASTAAPS
    cols = ["id_epsa","monto","observacion","concepto","periodo_pago"]
    try:
        # Ejecutar consulta SQL: Recuperar datos
        cursor = connection.cursor()
        cursor.execute(f"""SELECT {ingresos_select} 
        FROM ingresos
        LEFT OUTER JOIN tipo_ingreso ON ingresos.id_tipo_ingreso = tipo_ingreso.id_tipo_ingreso
        LEFT OUTER JOIN periodo_pago ON ingresos.id_periodo_pago = periodo_pago.id_periodo_pago
        """)
        
        list_cursor_to_data(cursor=cursor, data=epsa_data, cols=cols, key="ingresos", db_tag=db_tag)
        
        result_obj["ingresos"] = "ok"
    except (Exception, pg.Error) as error:
        logger.error(f"Error al recuperar datos de las tablas 'ingresos' y 'tipo_ingreso'. {error}\n")
        result_obj["ingresos"] = "error"
    finally:
        if cursor:
            cursor.close()

# Recuperar datos de Identificación de Problemas
def retrieve_identificacion_problemas(connection, epsa_data, result_obj, db_tag):
    """
    Recupera datos de las tablas 'identificacion_problemas' y 'tipo_sistema_problema'
    y los añade a los datos de EPSA base.
    """
    # Nombres de columnas SIIRAyS
    identificacion_problemas_cols = ["id_epsa","descripcion","efecto","acciones_actuales"]
    tipo_sistema_problema_cols = ["descripcion_tipo_problema"]
    
    # Tablas y Columnas para la consulta SQL
    identificacion_problemas_select = ",".join(
        [f"identificacion_problemas.{col}" for col in identificacion_problemas_cols] +
        [f"tipo_sistema_problema.{col}" for col in tipo_sistema_problema_cols]
    )
    # Nombres de los atributos en FASTAAPS
    cols = ["id_epsa","descripcion","efecto","acciones_actuales","tipo_problema"]
    try:
        # Ejecutar consulta SQL: Recuperar datos
        cursor = connection.cursor()
        cursor.execute(f"""SELECT {identificacion_problemas_select} 
        FROM identificacion_problemas LEFT OUTER JOIN tipo_sistema_problema
        ON identificacion_problemas.id_tipo_problema = tipo_sistema_problema.id_tipo_problema
        """)
        
        list_cursor_to_data(cursor=cursor, data=epsa_data, cols=cols, key="identificacion_problemas", db_tag=db_tag)

        result_obj["identificacion_problemas"] = "ok"
    except (Exception, pg.Error) as error:
        logger.error(f"Error al recuperar datos de las tablas 'identificacion_problemas' y 'tipo_sistema_problema'. {error}\n")
        result_obj["identificacion_problemas"] = "error"
    finally:
        if cursor:
            cursor.close()

# Recuperar datos de Identificación de Problemas
def retrieve_requerimiento_desarrollo(connection, epsa_data, result_obj, db_tag):
    """
    Recupera datos de las tablas 'requerimiento_desarrollo' y 'tipo_requerimiento'
    y los añade a los datos de EPSA base.
    """
    # Nombres de columnas SIIRAyS
    requerimiento_desarrollo_cols = ["id_epsa","descripcion"]
    tipo_requerimiento_cols = ["descripcion_tipo_requerimiento"]
    
    # Tablas y Columnas para la consulta SQL
    requerimiento_desarrollo_select = ",".join(
        [f"requerimiento_desarrollo.{col}" for col in requerimiento_desarrollo_cols] +
        [f"tipo_requerimiento.{col}" for col in tipo_requerimiento_cols]
    )
    # Nombres de los atributos en FASTAAPS
    cols = ["id_epsa","descripcion","tipo"]
    try:
        # Ejecutar consulta SQL: Recuperar datos
        cursor = connection.cursor()
        cursor.execute(f"""SELECT {requerimiento_desarrollo_select} 
        FROM requerimiento_desarrollo LEFT OUTER JOIN tipo_requerimiento
        ON requerimiento_desarrollo.id_tipo_requerimiento= tipo_requerimiento.id_tipo_requerimiento
        """)
        
        list_cursor_to_data(cursor=cursor, data=epsa_data, cols=cols, key="requerimiento_desarrollo", db_tag=db_tag)
        
        result_obj["requerimiento_desarrollo"] = "ok"
    except (Exception, pg.Error) as error:
        logger.error(f"Error al recuperar datos de las tablas 'requerimiento_desarrollo' y 'tipo_requerimiento'. {error}\n")
        result_obj["requerimiento_desarrollo"] = "error"
    finally:
        if cursor:
            cursor.close()

# Limpia los datos de EPSA base
def clean_epsa_data(epsa_data, result_obj):
    """
    Limpia y valida los datos antes de enviarlos al componente AAPS-API. 
    """
    # Remueve ids almacenados de manera temporal en el proceso "retrieve_instalacion".
    for epsa_id,epsa in epsa_data.items():
        if not "instalaciones" in epsa.keys(): continue
        for instalacion in epsa["instalaciones"]:
            if "id_instalacion" in instalacion.keys():
                del instalacion["id_instalacion"]
            if "fuente_financiamiento" in instalacion.keys():
                if "id_instalacion" in instalacion["fuente_financiamiento"]:
                    del instalacion["fuente_financiamiento"]["id_instalacion"]
    
    # Remueve los ids de EPSA usados para construir los datos en los procesos previos.
    result_obj["limpieza_datos"] = "ok"
    return list(epsa_data.values())

# Exporta los datos al servicio REST-API
def export_data(epsa_data, result_obj, db_tag):
    """
    Exporta los datos recuperados vía HTTP en formato JSON al servicio REST-API.
    """
    # try:
    post_data = json.dumps(
        epsa_data,
        ensure_ascii = False,
        default=str
    ).encode("utf-8")

    response = requests.post(
        f"http://fastapi:80/registro/restore?db_tag={db_tag}",
        data=post_data,
    )
    if response.status_code == 201:
        result_obj["exportacion"] = "ok"
    else:
        result_obj["exportacion"] = response.json()
        logger.error(response.json())
    # except Exception as error:
    #     logger.error(f"Error al exportar los datos. {error}\n")
    #     result_obj["exportacion"] = "error"

# Tarea de sincronización con la base de datos del SIIRAyS
@app.task(
    bind=True,      # La función tiene acceso a las propiedades del objeto (self)
    name="sync_db", # Nombre de la tarea
)
def sync_db(self, request_type):
    """
    Recupera datos de la base de datos PostgreSQL del SIIRAyS.
    Transforma estos datos al formato JSON usado por el REST-API.
    Alimenta los datos al componente AAPS-API.

    Parametros:
    request_type (str): Tipo de pedido al trabajador de Celery.
        Puede ser 'periodic' o 'user'.
        Si es 'periodic', significa que la tarea la inició el planificador periódico (Celery Beat).
        En este caso, los datos se almacenarán en la base de datos "sincronizada".
        Si es 'user', significa que la tarea fue iniciada por pedido de un usuario.
        En este caso los datos se almacenarán en la base de datos de "backup".  

    Retorna: Un JSON con una llave para cada subtarea y el valor indica si la subtarea fue realizada
        exitosamente ('ok') o si se produjó un error ('error'). 
    """
    if request_type == 'user':
        db_tag = 'backup'
    else:
        db_tag = 'sync'

    logger.info("Tarea de sincronización iniciada.\n")
    
    db_connection = None
    epsa_data = []
    result = {}

    db_connection = init_db_connection()    
    epsa_data = retrieve_epsa(db_connection, result, db_tag)    
    retrieve_representante(db_connection, epsa_data, result, db_tag)    
    retrieve_ubicacion(db_connection, epsa_data, result, db_tag)
    retrieve_estatus_juridico(db_connection, epsa_data, result, db_tag)    
    retrieve_documento_acreditacion(db_connection, epsa_data, result, db_tag)
    retrieve_demografia_cobertura(db_connection, epsa_data, result, db_tag)
    retrieve_instalacion(db_connection, epsa_data, result, db_tag)
    retrieve_fuente_financiamiento(db_connection, epsa_data, result, db_tag)
    retrieve_informacion_tecnica(db_connection, epsa_data, result, db_tag)
    retrieve_problemas_contaminacion(db_connection, epsa_data, result, db_tag)    
    retrieve_sistema_ap(db_connection, epsa_data, result, db_tag)    
    retrieve_tratamiento_agua_residual(db_connection, epsa_data, result, db_tag)    
    retrieve_tecnica_tuberia(db_connection, epsa_data, result, db_tag)    
    retrieve_tecnica_as(db_connection, epsa_data, result, db_tag)
    retrieve_descarga_ar(db_connection, epsa_data, result, db_tag)    
    retrieve_funcionarios(db_connection, epsa_data, result, db_tag)    
    retrieve_ingresos(db_connection, epsa_data, result, db_tag)    
    retrieve_identificacion_problemas(db_connection, epsa_data, result, db_tag)    
    retrieve_requerimiento_desarrollo(db_connection, epsa_data, result, db_tag)    
    epsa_data = clean_epsa_data(epsa_data, result)    
    export_data(epsa_data, result, db_tag)

    if db_connection:
        db_connection.close()
    
    result["numero_epsas"] = len(epsa_data)

    return result