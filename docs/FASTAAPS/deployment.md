---
title: Puesta en Producción (Instalación en Servidor)
description: Instrucciones para el levantamiento del sistema.
hero: FASTAAPS - Puesta en Producción
---

# Puesta en Producción (Instalación del Sistema en Servidores)

En esta sección se dan las instrucciones para que el personal de apoyo técnico (sector TIC) pueda levantar el sistema en servidores.

Esta acción puede resultar necesaria en caso de caida de los servidores, cambio de servidores o simplemente si por algún motivo se desea instalar el sistema nuevamente o en otro servidor.

## Requisitos

En teoría, el único requerimiento para levantar el sistema es un sistema operativo linux con acceso a internet, suficiente espacio y capacidad de cómputo y  que tenga Docker instalado. 

1. (**Requisitos del Servidor**) El sistema fue probado en producción una máquina virtual con las siguientes características, por lo que se recomienda usar un servidor con las siguientes características o de mayor capacidad:


    Propiedad | Valor
    -----|------
    Sistema Operativo | `Ubuntu 18.04.3 LTS (bionic)`
    Arquitectura:     | `x86_64`
    Memoria (total):  | `3.84 GB`
    Memoria (disponible): |  `3.46 GB`
    Número de Núcleos: |  `2`

2. (**Interfaz**) Para realizar la instalación se deberá poder ejecutar comandos en una línea de comandos, ya sea de manera directa o a través de una conexión remota (SSH). Es necesario contar con acceso del tipo *root* (superusuario) en el sistema para poder correr comandos `sudo`. 

3. (**IP pública**) Para que los usuarios del sistema puedan acceder a él a través de Internet, necesitaremos una IP pública que redirija a nuestro servidor.

## Paso 1: Instalar Docker y Docker-Compose

Docker y Docker-Compose simplifican bastante la instalación y el mantenimiento del sistema. 

Existen *scripts* de instalación convenientes que reducirían esta sección a un par de comandos, pero oficialmente estos métodos **no son recomendados en producción** por lo que se sugiere realizar la instalación convencional descrita a continuación.

Para instalar estas herramienas corremos los siguientes comandos:

1. Actualizamos el gestor de paquetes del sistema:
    ```
    sudo apt-get update
    ```
    ```
    sudo apt-get upgrade
    ```
2. Instalación de [Docker Engine](https://docs.docker.com/install/linux/docker-ce/ubuntu/). 

    En caso que se hayan instalado versiones antigüas de docker, las removemos. Es normal que diga que no existen los paquetes.

    ```
    sudo apt-get remove docker docker-engine docker.io containerd run
    ```

    Instalamos algunos paquetes que nos permitirán usar los repositorios vía HTTPS.

    ```
    sudo apt-get install apt-transport-https ca-certificates curl gnupg-agent  software-properties-common
    ```

    Añadimos la llave GPG oficial de Docker.

    ```
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
    ``` 

    Verificamos la integridad de la llave buscando su *huella digital*. El valor de la llave pública (`pub`) mostrada en el output debe igualar a `9DC8 5822 9FC7 DD38 854A E2D8 8D81 803C 0EBF CD88`.

    ```
    sudo apt-key fingerprint 0EBFCD88
    ```

    Añadimos el repositorio de Docker para Ubuntu.

    ```
    sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
    ```

    Actualizamos los repositorios del gestor de paquetes `apt`.

    ```
    sudo apt-get update
    ```
    
    Finalmente instalamos Docker.

    ```
    sudo apt-get install docker-ce docker-ce-cli containerd.io
    ```

    Y verificamos que haya sido instalado correctamente.

    ```
    sudo docker run hello-world
    ```

3. Instalación de [Docker Compose](https://docs.docker.com/compose/install/).

    Descargamos la última versión estable de Docker Compose.

    ```
    sudo curl -L "https://github.com/docker/compose/releases/download/1.25.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    ```

    Le damos permisos de  ejecutable al archivo descargado.

    ```
    sudo chmod +x /usr/local/bin/docker-compose
    ``` 

    Finalmente verificamos que Docker Compose sea accesible y esté instalado.

    ```
    docker-compose --help
    ```

## Paso 2: Descargar el Repositorio

El código fuente se encuentra en un [repositorio de Github](https://github.com/sergio-chumacero/aapsapi-docker), el cual contiene todo lo necesario para levantar el sistema. En este paso lo descargamos en el servidor.

Primero, instalamos Git en caso de que no se encuentre instalado en el servidor.

```
sudo apt install git
```  

Ahora clonamos el repositorio desde Github.

```
git clone https://github.com/sergio-chumacero/aapsapi-docker.git
```

Esto creará una carpeta en el directorio actual de nombre `aapsapi-docker`. 

!!!note "Nota"
    La dirección dentro del sistema de la carpeta con el código no es relevante para la instalación.

Ingresamos a la carpeta del código clonada.

```
cd aapsapi-docker
```

## Paso 3: Configuración del Sistema

Antes de correr el sistema, debemos decidir algunas variables de configuración que, por seguridad, no son incluídas en el código y por lo tanto deben ser editadas "manualmente". Para editar texto a través de la consola de comandos necesitaremos un editor de texto (Vim, Emacs, Nano, Micro, etc.). Dejamos la elección de un editor de texto a elección del funcionario, pero incluímos la instalación de [micro]() como recomendación personal.

???note "Instalar `micro` (click para abrir)"
    Micro es un editor de texto en la consola de comandos. Podemos usarlo para editar los archivos de configuración del sistema. Para instalarlo, podemos usar un script que crea un ejecutable en la carpeta donde estemos.
    ```
    curl https://getmic.ro | bash
    ```
    Para usarlo para abrir y editar un archivo (por ejemplo el archivo `ejemplo.txt` en la carpeta actual) basta con usar el ejecutable.
    ```
    ./micro ejemplo.txt
    ``` 
    Esto abrirá el archivo en modo edición. Para guardar cambios se puede usar `CTRL + S` y para salir del editor `CTRL + Q`.

Los archivos que modificaremos son `config.env` y  `docker-compose.yml`. 

* `config.env`: Siguiendo las normas de diseño de la sección de [calidad de código](/FASTAAPS/quality), utilizamos variables de ambiente para configurar los servicios del sistema y las agrupamos en un solo archivo para facilitar su manejo. Este archivo define variables de ambiente que serán incluidas dentro de los contenedores docker y modificarán su comportamiento. Es importante que, con excepción de las líneas de comentario (las que inician con el símbolo `#`), las líneas en este archivo **no pueden contener espacios**.

* `docker-compose.yml`: Este archivo define y configura los servicios docker, sus propiedades y los aspectos relacionados a la interconectividad de los contenedores Docker entre ellos y con los usuarios. Su uso es extenso y en caso de dudas, recomendamos recurrir a la [documentación oficial](https://docs.docker.com/compose/compose-file/) de referencia. En este archivo también se incluye la configuración del router web [Traefik](https://containo.us/traefik/) que dirije los pedidos de los clientes a los servicios adecuados del sistema.


### Descripción de las Variables de Configuración del Archivo `config.env`

El archivo `config.env` incluye comentarios indicando la funcionalidad de las variables de configuración, que deberían ser suficientemente intuitivas. Pero en caso de dudas, describimos las variables a continuación también. 

#### Configuración de Conexión a Django

* `DJANGO_SECRET_KEY` (**LLave secreta de Django**): Django utiliza métodos de encriptación que requieren de una cadena de caracteres aleatorios. Por motivos de seguridad no podemos incluir esta cadena en el repositorio, por lo que debe ser generada en el momento de la instalación. Esta llave **no puede ser publicada**, porque esto vulneraría las contraseñas encriptadas en la base de datos. Hay [páginas web](https://djecrety.ir/) que generan cadenas válidas de manera automática.

    Ejemplo de cadena válida (**no usar en producción**): `gcynb!y-^2+40794mfyien8_fl*bkue6!^&-v39959-w-&v&-x`

* `DJANGO_ALLOWED_HOSTS` (**URLs permitidas**): Por seguridad, es conveniente limitar las URLs desde las cuales se puede servir la aplicación. El valor de esta variable puede ser una lista sin espacios delimitada por comas. Por ejemplo: `200.185.45.65,aaps-lab.ml`. En última instancia o para hacer la prueba es posible permitir todas las URLs asignandole a esta variable el valor `*` (no recomendado en producción).

#### Configuración de Conexión a la Base de Datos

Estas variables son utilizadas por la aplicación Django para establecer una conexión con la base de datos Postgres que será usada en producción.

* `DJANGO_DB_HOST` (**URL del servicio Postgres**): URL que usará Django para conectarse con el servicio Postgres. Sólo modificar en caso de usar una base de datos externa. Valor por default: `django_postgres`. Con docker conectamos los contenedores en una red común y les asignamos dominios internos (hostnames) a cada servicio docker.

* `DJANGO_DB_PORT` (**Puerto del servicio Postgres (para Django)**): Puerto que usará Django para conectarse con el servicio Postgres. Solo modificar en caso de no usar la base de datos estándar. Valor por default: `5432`. El servicio Docker de base de datos postgres está configurado para usar este puerto por default.

* `DJANGO_DB_USER` (**Nombre de usuario de Postgres (para Django)**): El nombre de usuario que usará la aplicación Django para conectarse a la base de datos.

* `DJANGO_DB_USER` (**Contraseña de usuario de Postgres (para Django)**): La contraseña que usará  la aplicación Django para conectarse a la base de datos.

* `DJANGO_DB_NAME` (**Nombre de la base de datos Postgres (para Django)**): El nombre de la base de datos que usará Django para almacenar sus datos.

* `DJANGO_CONN_MAX_AGE` (**Tiempo de Conexión a la base de datos**): Al establecer una conexión con la base de datos, esta será persistida por este tiempo con el fin de poder ser reutilizada. Valor en segundos. Admite decimales con punto. Valor por default: `60.0`.

#### Configuración de usuario inicial PostgreSQL

* `POSTGRES_USER` (**Nombre del usuario inicial de Postgres.**)

* `POSTGRES_PASSWORD` (**Contraseña del usuario inicial de Postgres.**)

#### Configuración de usuario inicial PGAdmin

Para facilitar el manejo de la base de datos, se incluye el servicio de PGAdmin4. 

* `PGADMIN_DEFAULT_EMAIL` (**Mail de ingreso a PGAdmin**)

* `PGADMIN_DEFAULT_PASSWORD` (**Contraseña de ingreso a PGAdmin**)

#### Datos de Acceso para los Usuarios

Para facilitar el trabajo de instalación, se automatizó la creación de usuarios y permisos en el sistema. Los usuarios y permisos también pueden ser creados, modificados y eliminados desde la aplicación administrativa, cuando esta esté en funcionamiento. De manera automática se crean los siguientes usuarios:

1. **Administrador**: Tiene todos los permisos. Es usado para administrar a los otros usuarios. Puede acceder a la aplicación adminsitrativa.
2. **Administrador DRA**: Tiene todos los permisos sobre los datos de la dirección DRA-RH (SARH). Puede acceder a la aplicación adminsitrativa.
3. **Administrador DER**: Tiene todos los permisos sobre los datos de la dirección DER (Variables, Indicadores y POA). Puede acceder a la aplicación adminsitrativa.
4. **Usuario DRA**: Tiene permisos de sólo-lectura a los de la dirección DRA-RH. No puede acceder a la aplicación administrativa.
5. **Usuario DER**: Tiene permisos de sólo-lectura a los de la dirección DER. No puede acceder a la aplicación administrativa.

* `DJANGO_ADMIN_USER`, `DJANGO_ADMIN_DRA_USER`, `DJANGO_USUARIO_DRA_USER`, `DJANGO_ADMIN_DER_USER`, `DJANGO_USUARIO_DER_USER` (**Nombres de los usuarios**): Los nombres de los usuarios usados para el log-in.

* `DJANGO_ADMIN_PASSWORD`, `DJANGO_ADMIN_DRA_PASSWORD`, `DJANGO_USUARIO_DRA_PASSWORD`, `DJANGO_ADMIN_DER_PASSWORD`, `DJANGO_USUARIO_DER_PASSWORD` (**Contraseñas de los usuarios**): Las contraseñas de los usuario para el log-in. Los usuarios pueden cambiar sus contraseñas desde la página administrativa.

* `DJANGO_ADMIN_MAIL`, `DJANGO_ADMIN_DRA_MAIL`, `DJANGO_USUARIO_DRA_MAIL`, `DJANGO_ADMIN_DER_MAIL`, `DJANGO_USUARIO_DER_MAIL` (**Mail de los usuarios**): Emails de referencia. Los usuarios pueden cambiar sus direcciones de correo elecrónico desde la página administrativa.


### Configuración del archivo `docker-compose.yml`

La única configuración necesaria en este archivo es la de la URL y dominios del servidor. Estas se encuentran en el servicio `django` en la sección `labels`. En específico `Host(...)`. Las distintas URLs y dominiso pueden ser separados por comas.

``` python hl_lines="5"
services:
    ...
    labels:
        - "traefik.enable=true"
        - "traefik.http.routers.django_router.rule=Host(`192.168.99.101`,`aasp-lab.ml`) && PathPrefix(`/`)"
        - "traefik.http.services.django_service.loadbalancer.server.port=8000"
        - "traefik.http.routers.django_router.entrypoints=web" 
```
## Paso 4: Iniciar Servicios y Correr Scripts

Con la configuración lista, sólo hace falta levantar los servicios. Recordamos que todos los comandos del tipo `docker-compose` deben ser realizados en la carpeta base del código (la que contiene el archivo `docker-compose.yml`).

```
sudo docker-compose up -d
```

La primera vez puede tardar un poco en levantar los servicios porque debe descargar y crear las imágenes de los contenedores.

Una vez listo, corremos dos scripts que fueron incluídos en los contenedores de la base de datos y de Django respectivamente.

El primero (`init_db.sh`) crea la tabla de la aplicación en la base de datos y le otorga los accesos necesarios al usuario.

```
sudo docker exec -it django_postgres bash init_db.sh
```

El segundo (`init_django.sh`) crea y corre las migraciones de la base de datos, crea los usuarios  y alista los archivos estáticos.

```
sudo docker exec -it django bash init_django.sh
```

## Paso 5: Reiniciar los Contenedores

Finalmente sólo hace falta reiniciar los contenedores (también en el directorio base). 

```
sudo docker-compose restart 
```

Esto concluye la instalación. Ahora la aplicación administrativa y el servicio REST-API son accesibles desde la IP pública del servidor o dominios que redireccionen a esta IP. El panel de control de Postgres escucha en el puerto 5050.


    




