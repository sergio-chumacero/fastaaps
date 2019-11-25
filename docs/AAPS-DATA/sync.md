---
title: Servicio de Sincronización
description: Descripción general del Servicio de Sincronización de Datos del componente AAPS-DATA.
hero: AAPS-DATA - Servicio de Sincronización
---

# AAPS-DATA: Servicio de Sincronización de Datos

## 1. General

El **Servicio de Sincronización de Datos** del componente AAPS-DATA, se encarga de sincronizar los datos del componente con los datos de diversas fuentes externas, principalmente con los datos del sistema SIIRAyS.

![sync](../img/sync.png)


El [Servicio de Sincronización](/AAPS-DATA/sync), tanto de manera automática periódica como de manera manual a través de la aplicación de control de tareas, se encarga de:

1. Acceder a estos datos, a través de un driver para la base de datos Postgres.

2. Transformar los datos al formato del sistema.

3. Ingresar los datos al sistema FASTAAPS a través del servicio de acceso.

Una vez ingresados al sistema estos datos pueden ser utilizados por las aplicaciones.

![arquitectura_data](../img/sync_data_flow.svg)


## 2. Fuentes Originales de Datos

Las fuentes originales de los datos de la AAPS son aquellas administradas por sus direcciones, a través de sus planillas excel, sistema SIIRAyS, los archivos georeferenciados o cualquier otro método considerado necesario para el manejo apropiado de sus datos. El sistema FASTAAPS simplemente almacena, distribuye y utiliza estos datos con el fin de facilitar las tareas de los funcionarios de la AAPS.

## 3. Funciones

El servicio de sicronización se encarga de las siguientes funciones:

1. **Sincronización Periódica con el SIIRAyS**: Para asegurar que los datos utilizados por las aplicaciones se encuentren actualizados y repliquen fielmente el estado del SIIRAyS, el servicio de sincronización tiene una función que accesa de manera periódica y automática a la base de datos del sistema SIIRAyS y releva los datos más actuales.

2. **Sincronización a Pedido**: En caso de que sea necesario relizar una actualización a pedido, el servicio de sincronización ofrece esta función a través de su interfaz de monitoreo.

### 3.1 Propiedades de las Funciones

Para asegurar la consistencia del sistema, requerimos que todas las funciones del servicio de sincronización cumplan dos características fundamentales: Atomicidad e Idempotencia. Estas propiedades garantizan la consistencia del servicio, evitando entrar en estados inconsistentes y de esta manera reducir errores imprevistos.

1. **Atomicidad**: Una función atómica es aquella que es aplicada en su totalidad o no es aplicada en lo absoluto. 
 Es decir, al aplicar una función atomica todos sus subprocesos persistentes son aplicados en el orden correcto en el caso exitoso mientras que, en caso de fallar algún subproceso, ninguno de los subprocesos persistentes es aplicado.

En lenguaje simple se puede entender a una función atómica, como una que no deja rastros "a medias". 

2. **Idempotencia**: Con una función idempotente se obtiene el mismo resultado, independientemente de las veces que la función sea repetida. 
 Es decir, aplicar una función idempotente una vez es equivalente a aplicarla dos o más veces. 
 

En caso de extender el serivicio de sincronización añadiendo nuevas funciones, recomendamos fuertemente que las nuevas funciones cumplan con estas dos características.


## 4. Tecnologías

A continuación describimos las tecnologías utilizadas para el servicio de sincronización.

### 4.1 Celery & RabbitMQ: Sistema de Tareas Asincrónicas

Celery es una herramienta que permite correr tareas específicas de manera asincrónica, es decir en otro proceso o inclusive en otro servidor dedicado. Normalmente es usado para correr tareas pesadas y de mantenimiento. 

El servicio de sincronización de datos utiliza Celery para correr y manejar las tareas de sincronización con la base de datos del SIIRAyS.

![celery](../img/celery.png)

Celery utiliza procesos del tipo *trabajador* (worker) que están pendientes de tareas que tengan que ser ejecutadas. Para transmitir mensajes a los procesos trabajadores es necesario usar un servicio de mensajería (message broker). Existen distintos serivicios de mensajería como por ejemplo [Redis](https://redis.io/) o una base de datos convencional, pero el sistema FASTAAPS utiliza el servicio de mensajería [RabbitMQ](https://www.rabbitmq.com/), el cual es el más completo en cuanto a funcionalidades de Celery. 


![rabbitmq](../img/rabbitmq.png)



### 4.2 Flower: Interfaz de Monitoreo

Para transparentar el trabajo realizado por el servicio de sincronización y facilitar su mantenimiento, el servicio de sincronización cuenta con una interfaz de usuario web desde la cual un usuario de apoyo técnico puede monitorear las tareas realizadas y planeadas.

En esta página se muestra también si alguna tarea de sincronización reportó errores, el tipo de error producido y detalles que permitan solucionarlo y prevenir futuras ocurrencias.

A través de esta interfaz de usuario, es posible realizar una **actualización a pedido** de manera manual.

!!!info "Información Técnica"
    La interfaz de monitoreo del servicio de sincronización fue implementada haciendo uso de la librería [Flower](https://flower.readthedocs.io/), la cual es una herramienta de monitoreo para aplicaciones [Celery](http://www.celeryproject.org/).

    Celery, a su vez, es una librería de tareas distribuidas, la cual utilizamos para realizar tareas periódicas de manera automática. Celery hace uso de un *agente de mensajería* (en ingés *message broker*) del tipo [RabbitMQ](https://www.rabbitmq.com/).

    Dentro del servidor de la aplicación, tanto la aplicación Celery, como el agente de mensajería RabbitMQ, se encuentran contenerizados.

    Todos las librerías RabbitMQ, Celery y Flower son del tipo *código abierto*.

### 4.3 PsycoPG2: Driver de PostgreSQL

### 4.4 Requests: Cliente HTTP 

## Especificaciones Técnicas

### Tecnologías Utilizadas


