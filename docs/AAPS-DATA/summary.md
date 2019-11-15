---
title: Resúmen
description: Resúmen ejecutivo del componente AAPS-DATA
hero: AAPS-DATA - Resúmen Ejecutivo
---

# AAPS-DATA: Resúmen Ejecutivo

Bienvenido a la documentación del componente de almacenamiento de datos *AAPS-DATA*!

## General

El sistema [**AAPS-DATA**](./summary.md) ...

* Almacena y Maneja los conjuntos de datos utilizados por el sistema [**FastAAPS**](../README.md).

* Sus bases de datos están optimizadas para responder a los pedidos realizados al servicio de datos del componente [**AAPS-API**](../AAPS-API/summary.md).

* Se encarga de leer los datos del sistema **SIIRAyS** y sincronizarlos con la base de datos de las aplicaciones.

![arquitectura_data](../img/arquitectura_data.svg)

## Conjuntos de Datos

Los conjuntos de datos hacia los cuales actualmente el sistema ofrece puntos de acceso son:

* **Dirección de Seguimiento Regulatorio**: Variables e Indicadores de las EPSAs reguladas.
* **Dirección de Regulación Ambiental**: Sistemas de Autoabastecimiento de Recursos Hídricos (SARH).
* **Jefatura de Licencias y Registros**: EPSAs registradas.
* **Datos georeferenciados**: Áreas de Prestación de Servicio, Fuentes de Abastecimiento, Tanques de Almacenamiento.

Los datos que ingresan al sistema AAPS-DATA son capturados de distintas fuentes: Del sistema SIIRAyS, de archivos georeferenciados y
tablas mantenidas por funcionarios de la institución.