---
title: Docker - Contenerización de Servicios
description: Descripción general de tecnologías de contenerización y contenedores en producción del sistema FASTAAPS.
hero: FASTAAPS - Docker & Contenerización
---

# Docker: Tecnologías de Contenerización

![docker](../img/docker.png)

## Información General: ¿Qué es y para qué sirve Docker?

Docker es una plataforma que permite a los desarrolladores empaquetar y correr aplicaciones de manera estándar. 

Docker está basado en tecnologías de virtualización a nivel de sistema operativo que empaqueta software en sus propios entornos virtuales denominados *contenedores*. A diferencia de una *máquina virtual*, un contenedor es más eficiente y ligero porque no replica una máquina física abstracta, sino que simplemente replica un sistema operativo abstracto. De esta manera se puede correr muchos más contenedores en un mismo servidor que maquinas virtuales gozando de las ventajas de aislar cada aplicación en su entorno individual.

Un contenedor Docker es un proceso aislado que corre en el entorno del usuario del sistema operativo y comparte el núcleo (kernel) del sistema con otros procesos. Múltiples contenedores pueden correr en la misma máquina, cada uno corriendo su aplicación en un proceso aislado.

La ventaja de utilizar tecnologías de contenerización para los servicios en producción son:

1. **Bajo índice de acoplamiento (loose coupling)**: Al aislar cada aplicación en su propio entorno virtual, estas son independientes las unas de las otras. Las dependencias de una no interfieren con las dependencias de las otras. Por ejemplo, múltiples servicios del sistema FASTAAPS requieren de una instalación de Python y al aislarlos en sus propios contenedores es posible que cada servicio tenga su propia instalación de Python, posiblemente con distintas versiones, librerías de código instaladas y variables de entorno. 


2. **Consistencia y Replicabilidad (replicablity)**: Al definir explícitamente las dependencias de una aplicación, podemos garantizar que las aplicaciones funcionarán de igual manera en cualquier entorno, sea este de desarrollo o de producción.

3. **Facilidad de escalabilidad (scalability)**: Al tener la posibilidad de crear y replicar aplicaciones contenerizadas facilmente, es posible incrementar o reducir el número de copias de un servicio en distintos de acuerdo a su uso.  

Una desventaja del uso de contenedores es la complejidad de interconexión y monitoreo de servicios. Por suerte, existen tecnologías maduras de manejo y orquestración de servicios contenerizados como [Kubernetes](https://kubernetes.io/).  

## Servicios Contenerizados dentro del Sistema FASTAAPS

Un contenedor es creado de una *imágen base* que describe todas sus dependencias y su proceso de instalación. Estas imágenes nos dan la capacidad de crear servicios de manera reproducible y predecible, independientemente de las características particulares de la máquina.

A continuación listamos las imágenes creadar para los distintos servicios del sistema FASTAAPS:


Servicio  | Componente    | Tecnología Utilizada | Descripción 
------------ | ------------- | ------------         |  ---------
Servicio de Sincronización de datos  | AAPS-DATA |  Celery | Corre y Administra tareas de sincronización de datos.   
Agente de Mensajería | AAPS-DATA  | RabbitMQ | Maneja una fila de mensajes (en inglés message queue). Usado por el servicio de sincronización. 

## Archivos Docker de los Servicios

El *archivo de Docker* (en inglés *Dockerfile*) contiene todas las instrucciones necesarias para construir la imágen del contenedor y a su vez sirve de documentación técnica. Estos archivos describen la aplicación y sus dependencias. 

Docker ejecuta las instrucciones de un archivo Docker para contruir la imágen base.

A continuación incluímos los archivos docker que construyen las imágenes base usadas por los servicios del sistema.

