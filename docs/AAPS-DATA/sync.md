---
title: Servicio de Sincronización
description: Descripción general del Servicio de Sincronización de Datos del componente AAPS-DATA.
hero: AAPS-DATA - Servicio de Sincronización
---

# AAPS-DATA: Servicio de Sincronización de Datos

## General

El **Servicio de Sincronización de Datos** del componente AAPS-DATA, se encarga de sincronizar los datos del componente con los datos de diversas fuentes externas, principalmente con los datos del sistema SIIRAyS.

![sync](../img/sync.png)


### Fuentes Originales de Datos

Las fuentes originales de los datos de la AAPS son aquellas administradas por sus direcciones, a través de sus planillas excel, sistema SIIRAyS, los archivos georeferenciados o cualquier otro método considerado necesario para el manejo apropiado de sus datos. El sistema FASTAAPS simplemente almacena, distribuye y utiliza estos datos con el fin de facilitar las tareas de los funcionarios de la AAPS.

## Funciones

El servicio de sicronización se encarga de las siguientes funciones:

1. **Sincronización Periódica con el SIIRAyS**: Para asegurar que los datos utilizados por las aplicaciones se encuentren actualizados y repliquen fielmente el estado del SIIRAyS, el servicio de sincronización tiene una función que accesa de manera periódica y automática a la base de datos del sistema SIIRAyS y releva los datos más actuales.

2. **Sincronización a Pedido**: En caso de que sea necesario relizar una actualización a pedido, el servicio de sincronización ofrece esta función a través de su interfaz de monitoreo.

### Propiedades de las Funciones

Para asegurar la consistencia del sistema, requerimos que todas las funciones del servicio de sincronización cumpla dos características fundamentales: Atomicidad e Idempotencia. 

1. **Atomicidad**: Una función atómica es aquella que es aplicada en su totalidad o no es aplicada en lo absoluto. 
 Es decir, al aplicar una función atomica todos sus subprocesos persistentes son aplicados en el orden correcto en el caso exitoso mientras que, en caso de fallar algún subproceso, ninguno de los subprocesos persistentes es aplicado.

En lenguaje simple se puede entender a una función atómica, como una que no deja rastros "a medias". 

2. **Idempotencia**: Con una función idempotente se obtiene el mismo resultado, independientemente de las veces que la función sea repetida. 
 Es decir, aplicar una función idempotente una vez es equivalente a aplicarla dos o más veces. 
 

En caso de extender el serivicio de sincronización añadiendo nuevas funciones, recomendamos fuertemente que las nuevas funciones cumplan con estas dos características.


## Interfaz de Monitoreo

Para transparentar el trabajo realizado por el servicio de sincronización y facilitar su mantenimiento, el servicio de sincronización cuenta con una interfaz de usuario web desde la cual un usuario de apoyo técnico puede monitorear las tareas realizadas y planeadas.

En esta página se muestra también si alguna tarea de sincronización reportó errores, el tipo de error producido y detalles que permitan solucionarlo y prevenir futuras ocurrencias.

A través de esta interfaz de usuario, es posible realizar una **actualización a pedido** de manera manual.

!!!info "Información Técnica"
    La interfaz de monitoreo del servicio de sincronización fue implementada haciendo uso de la librería [Flower](https://flower.readthedocs.io/), la cual es una herramienta de monitoreo para aplicaciones [Celery](http://www.celeryproject.org/).

    Celery, a su vez, es una librería de tareas distribuidas, la cual utilizamos para realizar tareas periódicas de manera automática. Celery hace uso de un *agente de mensajería* (en ingés *message broker*) del tipo [RabbitMQ](https://www.rabbitmq.com/).

    Dentro del servidor de la aplicación, tanto la aplicación Celery, como el agente de mensajería RabbitMQ, se encuentran contenerizados.

    Todos las librerías RabbitMQ, Celery y Flower son del tipo *código abierto*.



## Especificaciones Técnicas

### Tecnologías Utilizadas


