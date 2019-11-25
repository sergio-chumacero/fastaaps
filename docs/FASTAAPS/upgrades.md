---
title: Mejoras de los Sistemas Previos
description: Descripción de los cambios realizados a los sistemas implementados en consultorías previas.
hero: FASTAAPS - Mejoras
---

# Mejoras de los Sistemas Previos

En esta sección describimos los cambios más importantes realizados a los sistemas implementados en consultorías previas.

## 1. Estructura General: Arquitectura Basada en Servicios

## 2. Contenerización

El sistema AAPS-API previo estaba instalado en los servidores de la institución de manera directa. Las tecnologías necesarias para su funcionamiento eran instaladas de manera manual o a través de un *script* automático que se conectaba con el servidor y corría los comandos necesarios para la instalación.

Este método es suficiente para una aplicación simple, pero a medida que el sistema crece y se añaden más componentes, los problemas de dependencias y orquestación de servicios requieren de soluciones más sustentables.

Para la nueva arquitectura basada en servicios se utiliza se utiliza contenedores [Docker](https://www.docker.com/). Docker es una plataforma que permite a los desarrolladores empaquetar y correr aplicaciones vía interfaces estandarizadas. 

![docker](../img/docker.png)

Al utilizar Docker, cada servicio es ejecutado en un proceso aislado, eliminando así problemas de dependencias. Además, el uso de contenedores Docker para la puesta en producción reduce el trabajo de instalación y el uso de scripts de instalación.

Para más información con respecto a la contenerización de servicios en el sistema FASTAAPS, véase la sección [Tecnologías de Contenerización](/FASTAAPS/docker).
