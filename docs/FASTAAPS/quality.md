---
title: Estándares de Calidad de Código
description: Descripción de lso estándares de calidad de código utilizados para el código fuente del sistema FASTAAPS.
hero: FASTAAPS - Cálidad de Código
---

# Estándares de Calidad de Código

!!! quote "Calidad"
    "Calidad significa hacer las cosas bien, aún cuando nadie esté mirando." 
    
    .- Henry Ford 

El sistema FASTAAPS tiene una arquitectura orientada a servicios y se adhiere a los [12 factores de aplicaciones como servicio](https://12factor.net/). Estos factores son principios de diseño que buscan las siguientes propiedades deseables para un sistema:

* Minimización de costos y esfuerzos para administradores y nuevos desarrolladores.
* Máxima **portabilidad** entre ambientes de trabajo.
* Adecuado para el uso de tecnologías cloud.
* Adecuado para los paradigmas de **integración contínua** y **desarrollo ágil**.
* Es fácilmente **escalable** sin necesitar cambios drásticos de estructura. 

A continuación describimos brevemente los factores, las ventajas de seguir estas guías de diseño y cómo se tomaron en consideración los factores durante el desarrollo e implementación del sistema FASTAAPS.

## Factor 1: Un solo Repositorio de Código Fuente Versionado

La aplicación utiliza un sistema de control de versión como Git o Mercurial y todo el código fuente de la aplicación es almacenado en un solo repositorio.

Ventajas de usar un sistema de control de verión:

* **Colaboración**: Permite añadir contribuciones de múltiples desarrolladores.
* **Versatilidad**: Permite mantener distintas versiones del código para distintas entornos de trabajo (desarrollo, prueba, producción). 
* **Accesibilidad**: Hace al código fuente más accesible al equipo. La accesibilidad del código es fundamental para ser considerado *código abierto*.
* **Automatización**: Las plataformas de maenjo de código modernas como Github además se integran bien con herramientas de integración contínua.

Ventajas de usar un repositorio único:

* **Facilidad de Uso** y Reuso del código fuente. 
* **Simplicidad** de la estructura del proyecto. 

Todo el código del sistema FASTAAPS es almacenado en un respositorio de Github:

[https://github.com/sergio-chumacero/fastaaps/](https://github.com/sergio-chumacero/fastaaps/)

La estructura del código es detallada en la sección [estructura del código fuente](FASTAAPS/codebase).

## Factor 2: Aislamiento y Declaración Explícita de Dependencias

La aplicación declara las dependencias de sus componentes de manera explícita y aislada.

Ventajas del aislamiento de dependencias:

* **Bajo índice de acoplamiento** entre componentes: Al tener sus dependencias aisladas, los componentes no interfieren de manera negativa unos con otros.

* **Especialización** de los componentes: Como consecuencia del bajo índice de acoplamiento, cada componente puede usar tecnologías especializadas para sus funciones, a diferencia de usar una herramienta general no optimizada para todas sus funciones. 

Ventajas de la declaración explícita de dependencias:

* **Consistencia**: Al no depender de dependencias implícitas, los servicios garantizan sus funcionamientos en diversos entornos de trabajo sin correr el riesgo de que una de sus dependencias no sea cumplida. 

* **Documentación**: Además de ser usados para la construcción de los componentes, los archivos de declaración de dependencias sirven de documentación confiable.

* **Replicabilidad**: Con las dependencias explícitamente declaradas, un desarrollador puede replicar fácilmente el ambiente de desarrollo de la aplicación. 


El uso de contenedores Docker en la implementación de los servicios del sistema garantiza el aislamiento de dependencias en el sistema FASTAAPS.

Los documentos que definen de manera explícita las dependencias de cada servicio son los archivos Docker utilizados para la construcción de las imágenes base. Otros documentos usados con este fin son los documentos de dependencias de Python `requirements.txt` usados por el gestor de paquetes `pip`.

Los métodos de contenerización son descritos en detalle en la sección de [contenerización](FASTAAPS/docker). 

## Factor 3: Configuración Guardada en Variables de Ambiente

La configuración de la aplicación es guardada en variables de ambiente y no en el código fuente.

La configuración de una aplicación es todo aquello que vaya a cambiar entre distintos entornos de trabajo. Ejemplos de configuración son credenciales, detalles de acceso a servicios externos (como bases de datos), direcciones IP y URLs entre otras.

Ventajas:

* **Consistencia** del código fuente: Al separar estríctamente la configuración del código fuente, el código fuente requiere de menos modificaciones para funcionar en distintos entornos de trabajo.

* **Colaboración**: Al no guardar credenciales en el código este puede ser publicado sin comprometer la seguridad del sistema. Esta propiedad es fundamental para poder publicar el código fuente como *código abierto*.

* **Facilidad de uso**: Las variables de ambiente pueden ser modificadas con facilidad. Un administrador o desarrollador externo que deba cambiar la configuración de la aplciación no debería tener que modificar el código fuente.

En el sistema FASTAAPS la configuración usada por los componentes es guardada en variables de ambiente en los contenedores Docker. Para facilitar la modificación de estas variables de configuración, las variables son agrupadas en archivos del tipo `.env`.

## Factor 4: Servicios de Apoyo como Recursos Adjuntos

La aplicación no hace distinción entre servicios de apoyo externos e internos

Un servicio de apoyo es cualquier servicio que la aplicación requira para su funcionamiento normal, por ejemplo bases de datos, agentes de mensajería o servicios de mail. Los servicios de apoyo pueden ser externos (por ejemplo servicios cloud)  o internos, es decir manejados por el mismo sistema (por ejemplo la base de datos del sistema).

Ventajas:

* **Facilidad de uso**: Al no diferenciar entre servicios externos e internos, se elimina la complejidad de identificar ambos grupos y verificar su funcionamiento.

* **Flexibilidad**: Al no especificar los detalles de los servicios en el código de la aplicación es posible intercambiar y extender los servicios de apoyo con mayor flexibilidad.

Los recursos de apoyo del sistema FASTAAPS son por ejemplo el agente de mesarjería RabbitMQ utilizado por el [servicio de sincronización](/AAPS-DATA/sync) o la base de datos MongoDB de la [base de datos especializada](/AAPS-DATA/db). El código de los componentes que hacen uso de estos servicios sólo requieren de credenciales y detalles de conexíon.

## Factor 5: Separación entre Construcción y Ejecución

Los procesos de construcción y ejecución de la aplición están fuertemente separados.

El proceso de construcción de la aplicación consiste en transformar el código fuente y la configuración de la aplicación en un archivo ejecutable, mientras que el proceso de ejecución consiste en correr este archivo en el ambiente de producción.

Ventajas:

* **Consistencia**: Al separar estos dos procesos, la modificación del código fuente no afecta la ejecución de la aplicación y la aplicación no es capaz de modificar el código fuente.

* **Seguridad**: Si el código se encuentra con control de veriones, es posible volver, en caso de emergencia a una versión previa de la aplicación recreando el archivo ejecutable de una versión anterior.

* **Colaboración**: La seguridad del punto anterior facilita la colaboración de múltiples desarrolladores.

Los contenedores Docker usados por el sistema FASTAAPS son versiones ejecutables creadas en base a imágenes base que incluye el código fuente de la aplicación.

Los métodos de contenerización son descritos en detalle en la sección de [contenerización](FASTAAPS/docker).


## Factor 6: Procesos Independientes y Libres de Estado

La aplicación es ejecutada como uno o más procesos libres de estado (stateless) que no comparten recursos entre ellos.

Un proceso libre de estado es aquel cuya funcionalidad no depende del estado interno en el que se encuentre en un momento específico. Esto garantiza que el proceso funcionará de igual manera en cualquier momento.

Ventajas:

* **Consistencia**: Al garantizar que la lógica de la aplicación no dependa de lo que esta hizo previamente, podemos garantizar la consistencia de la aplicación en el tiempo.

* **Bajo índice de acoplamiento**: Ya que los procesos de la aplicación no comparten recursos entre ellos, se eliminan dependencias innecesarias.

* **Escalabilidad** horizontal: Con múltiples instancias de la aplicación corriendo en paralelo, si estos mantuvieran estado de manera interna, sería muy complicado orquestrar la interacción entre ellos.

Los procesos del sistema FASTAAPS no guardan datos de sesiones o memoria de transacciones, todo el estado persistente es relegado a servicios de apoyo como bases de datos o agentes de mensajería.

La interacción entre los procesos del sistema es realizada a través de protocolos de comunicación definidos de manera explícita y ofrecidos como servicio, por ejemplo el servicio de sincronización utiliza el servicio REST-API para ingresar datos al sistema. 

## Factor 7: Exportación de Servicios vía Enlaces de Puertos

La aplicación expone sus servicios a través de puertos de acceso específicos.

Entre otras cosas, esto significa que la aplicación no depende de un servidor web adicional para ofrecer sus servicios. 

Ventajas:

* **Portabilidad**: Al eliminar dependencias de conectividad, la aplicación puede ser considerada como un paquete "completo" que puede ser instalado fácilmente en cualquier ambiente.

* **Interconexión**: Al contar con protocolos de conexión bien definidos, resulta más factible hacer uso de estos canales para conectar distintos servicios, en especial si existen múltiples instancias de la aplicación.

Los contenedores Docker utilizados por el sistema FASTAAPS exponen puertos específicos, definidos de manera explícita en los archivos de creación de imágenes base. La interacción entre componentes utiliza estos canales de comunicación. Por ejemplo, el servicio de sincronización de datos utiliza el puerto expuesto por el servicio REST-API para alimentar datos al sistema y por lo tanto se adhiere a los protocolos de acceso definidos por este servicio.

Los puertos expuestos por los distintos contenedores es detallado en la sección [Tecnologías de Contenerización](/FASTAAPS/docker).

## Factor 8: Procesos como Modelo de Concurrencia

La aplicación utiliza procesos computacionales como mecanismo fundamental para la extensión de sus servicios.

Durante su ciclo de vida, es común que la aplicación reciba cargas de trabajo diversas, por ejemplo un fin de semana, se espera que el número de pedidos a la aplicación sea menor que en horas de trabajo. Este factor instruye que la manera de afrontar esta situación es a través de procesos computacionales concurrentes.

De acuerdo al factor número seis, los procesos computacionales son aislados y libres de estado. Este punto es importante para evitar problemas de consistencia y complejidad al tener que manejar múltiples procesos paralelos de manera simultánea. 

Ventajas:

* **Escalabilidad**: La arquitectura basada en procesos computacionales permite a la aplicación manejar cargas de trabajo diversas de manera eficiente, iniciando y terminando procesos de acuerdo al uso de sus componentes.

* **Eficiencia**: Responder a altas cargas de trabajo incrementando el número de procesos de cierto tipo (escalabilidad horizontal), tiende ser más económico en términos de recursos computacionales que incrementar la capacidad de los servidores (escalabilidad vertical), ademas de adaptarse más facilmente a sistemas distribuidos.

El uso de contenedores Docker encapsula los servicios del sistema FASTAAPS en procesos aislados. Además, el uso de tecnologías de orquestación de contenedores permite que el sistema se adapte a distintas cargas de trabajo.

## Factor 9: Facilidad y Rapidez de Puesta en Marcha y Cierre

La aplicación puede ser iniciada y apagada con facilidad y de manera rápida.

Ventajas:

* **Robustez**: La facilidad de manejo incentiva las mejoras constantes y cambios de configuración en producción.

* **Escalabilidad**: La rapidez de inicio y cierre de la aplicación es importante para la adaptación dinámica de la aplicación.

El sistema FASTAAPS utiliza herramientas de orquestración de contenedores como `docker-compose` para facilitar y agilizar los procesos de inicio y cierre de aplicaciones. Estos procesos no tardan más de unos segundos desde que el comando inicial es ejecutado.

## Factor 10: Entornos de Trabajo Similares

Los entornos de trabajo (desarrollo, prueba y producción) de la aplicación deben ser lo más similares posibles.

Ventajas:

* **Robustez/Consistencia**: Si los entornos de trabajo son similares, se reducen las probabilidades de fallas inesperadas que tengan como causa factores externos a la aplicación.

* **Integración Contínua**: Al mantener la brecha entre desarrollo y producción pequeña, se posibilita la automatización de la puesta en producción.

Al abstraer el entorno de trabajo a nivel sistema operativo usando contenedores, garantizamos que los ambientes de trabajo sean lo más similares posibles. De igual manera, las herramientas y servicios de apoyo utilizados durante el desarrollo del sistema FASTAAPS son los mismos que los que son utilizados en producción.

## Factor 11: Archivos de Registro como un Flujo de Eventos 

La aplicación permite monitorear sus servicios a través de un flujo de eventos en tiempo real (event stream).

Este flujo de eventos será redirigido posteriormente a archivos para ser archivado.

Ventajas:

* **Portabilidad**: Como la aplicación no administra los archivos de registro de sus servicios individualmente, la aplicación y sus registros pueden ser manejados con mayor faicilidad.

* **Facilidad de Uso**: Tener todos los eventos de la aplicación en un sólo lugar, facilita el trabajo de monitoreo de la aplicación.

Todos los eventos de los servicios del sistema FASTAAPS son unificados en un flujo de eventos que son almacenados periódicamente en archivos persistentes.

## Factor 12: Tareas Administrativas como Procesos de Vida Corta Incluídos en la Distribución de Código

La aplicación permite realizar tareas administrativas creando procesos de vida corta en un entorno similar/idéntico al entorno de la aplicación. Estas tareas administrativas deben ser incluídas en la distribución de código de la aplicación.

Ejemplos de tareas administrativas son: Migraciones de bases de datos, limpieza/actualización de datos, administración de usuarios y credenciales. 

Ventajas:

* **Consistencia**: Al utilizar un ambiente similar/idéntico al de la aplicación para ejecutar tareas administrativas, se minimiza el riesgo de errores con causa ajena a la implementación de estas tareas.  

* **Seguridad**: Las tareas administrativas pueden ser riesgosas para la aplicación por lo que es mejor usar herramientas que los desarrolladores hayan puesto a prueba. 

* **Facilidad de Uso**: Al incluír las tareas en la distribución de código, no es necesario importarlas desde un entorno distinto y el equipo de desarrollo garantiza que estas tareas se encuentren actualizadas y que funcionen apropiadamente.

Las tareas admnistrativas del sistema FASTAAPS son incluídas en el repositorio de código fuente y son ejecutadas dentro del contenedor correspondiente a la tarea en cuestión.





