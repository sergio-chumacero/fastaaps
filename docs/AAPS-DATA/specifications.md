---
title: Estándares y Especificaciones de Datos
description: Descripción de los estándares y especificaciones de Datos del componente AAPS-DATA.
hero: AAPS-DATA - Especificaciones
---

# AAPS-DATA: Estándares y Especificaciones de Datos

El sistema FASTAAPS a través de su servicio de acceso web de datos permite a aplicaciones acceder a los datos del sistema.

El formato de intercambio de datos utilizado es JSON, el formato más utilizado a nivel mundial para este tipo de servicios.

!!! info "Acerca de JSON"
    [JSON](http://www.json.org/), cuyas siglas en inglés significan "**J**ava**S**cript **O**bject **N**otation" (en español "notación de objetos JavaScript") es un formato ligero de intercambio de datos ampliamente utilizado en la web. Es fácil de leer para humanos y facil de interpretar para máquinas. Es el formato más utilizado en servicios de acceso de datos REST-API.

## JSON-Schema

Es necesario describir y especificar el formato de los archivos JSON utilizados. Para este fin utilizamos el estándar [JSON-Schema](https://json-schema.org/).

JSON-Schema permite describir el formato de datos JSON que sea facilmente legible por humanos y sirva de documentación. Además, puede ser utilizado para validar datos.

La versión más reciente del estándar a la fecha es [2019-19](https://json-schema.org/specification.html). 

## Fechas

Las fechas en los archivos JSON almacenados y distribuidos por el sistema FASTAAPS, son del tipo **string** (cadenas de texto) y acatan el estándar internacional para la representación de fecha y hora [**ISO 8601**](https://www.w3.org/TR/NOTE-datetime).

Algunos de los formatos del estándar utilizados son los siguientes:

* **Año**: `AAAA` (ejemplo `1997`)
* **Año y Mes**: `AAAA-MM` (ejemplo `1997-07`)
* **Fecha completa**: `AAAA-MM-DD` (ejemplo `1997-07-16`)
* **Fecha completa más hora y minutos**: `AAAA-MM-DDThh:mmTZD` (ejemplo `1997-07-16T19:20+01:00`)
* **Fecha completa más hora, minutos y segundos**: `AAAA-MM-DDThh:mm:ssTZD` (ejemplo `1997-07-16T19:20:30+01:00`)

Donde:

* `AAAA` = Año de cuatro dígitos
* `MM`   = Mes de dos dígitos (01=Enero, etc.)
* `DD`   = Día del mes de dos dígitos (01 a 31)
* `hh`   = Hora de dos dígitos (00 a 23) (am/pm NO permitido)
* `mm`   = Minuto de dos dígitos (00 a 59)
* `ss`   = Segundo de dos dígitos (00 a 59)
* `TZD`  = Zona horaria (Z o +hh:mm o -hh:mm)