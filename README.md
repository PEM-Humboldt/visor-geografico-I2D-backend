
# Backend-Visor-I2D
El backend visor geografico I2D es un componente que permite interactuar con una base de datos de información geográfica que contiene información de registros biológicos.

Este proyecto ha sido desarrollado por el [Instituto Humboldt](http://www.humboldt.org.co). El proyecto usa [Python 3.9.2](https://www.python.org/), junto al framework web de alto nivel [DJANGO](https://www.djangoproject.com/) y a paquetes como [Django Rest Framework](https://www.django-rest-framework.org/) y [psycopg2](https://pypi.org/project/psycopg2/)

## Prerequisitos

Para despliegue en desarrollo:

 - Python 3.9.2
 - pip
 - postgresql-dev
 - gcc
 - python3-dev
 - musl-dev

Para despliegue en producción:

- Docker version 19.03.13 o superior
- Docker-compose 1.28.5 o superior
- Git 2.23 o superior

En general:

- Debe existir una base de datos en PostgreSQL a la cual se conectará este componente.

Esta es una versión preliminar y se implementarán nuevas funcionalidades.

## Configuración inicial

### Instalación y ejecución

Debe tener instalado python y pip en su equipo local, para la instalación de paquetes y ejecución del proyecto sin utilizar docker. 

Clone el proyecto en su equipo e ingrese por línea de comandos al directorio del proyecto.

### 1.1. Clone el repositorio:

```
$ git clone https://github.com/PEM-Humboldt/visor-geografico-I2D-backend.git
```

### 1.2. Archivo secret.json

El proyecto necesita un archivo secret.json con la siguiente plantilla:
```
{
    "FILENAME": "secret.json",
    "SECRET_KEY": [YOUR DJANGO SECRET KEY],
    "DB_NAME": [YOUR DB NAME],
    "USER": [YOUR DB USER],
    "PASSWORD": [YOUR DB PASSWORD],
    "HOST" : [YOUR DB HOST URL],
    "PORT" : [YOUR DB HOST PORT]
}
```
Completar el archivo con las credenciales correspondientes y copiarlo en la raíz del proyecto.

### 1.3. Instalación de paquetes:
Ubiquese en la carpeta i2dbackend y ejecute la siguiente sentencia para instalar las dependencias del proyecto:
```
    cd ../../../ i2dbackend

    pip install -r requirements.txt
```

<!-- ### 1.4. Para crear nuevos modelos automáticamente a partir de la base de datos de PostgreSql
```
    python manage.py inspectdb
``` -->
### 1.4. Para crear nuevos modelos automáticamente en el entorno del administrador
Verifiqué que no hay errores 
```
    python manage.py makemigrations
```
Migre los modelos
```
    python manage.py migrate
```
### 1.5. Ejecución en entorno de desarrollo:
Ejecute la siguiente instrucción:

```
    python manage.py runserver
```
La instrucción iniciará el proyecto en su entorno de desarrollo.


## Despliegue en producción

### 2.1 Descripción

Él despliegue en producción de la aplicación se realizará utilizando [Gunicorn](https://gunicorn.org) como servidor de aplicaciones WSGI HTTP y [NGINX](https://www.nginx.com)  como servidor web.

Por esta razón se utilizará un contenedor [Docker](https://www.docker.com) para cada componente: 1) *Django con Gunicorn* y 2) *NGINX*. El tercer componente es la base de datos, pero esa no está incluida en el alcance de este despligue y se asume su existencia.

La herramienta [Docker-compose](https://docs.docker.com/compose/) se utilizará para la ejecución de los dos componentes y su interacción.

### 2.1. Instalación de Docker y Docker-compose

Es necesario contar con la versión 19.03.13 de Docker o superior y Docker-compose versión 1.28.5.

La instalación se puede hacer siguiendo los pasos según el sistema operativo en la documentación oficial de Docker. 

### 2.2. Despliegue

Una vez se haya clonado el repositorio, verificar que en la raíz del mismo se encuentren los siguientes archivos:

- dockerfile
- docker-compose.yml
- default.conf
- secret.json

El archivo secret.json debe ser completado según el paso 1.2. con los datos del entorno de producción y debe ser copiado en la raíz.

A continuación, desde la raíz del proyecto se debe ejecutar el siguiente comando para construir la imagen personalizada del contenedor que ejecutará el componente de Django con Gunicorn:

```
docker-compose build
```
Se utilizará la  imagen  oficial del contenedor de NGINX que se encuentra [aquí](https://hub.docker.com/_/nginx), y por lo tanto no es necesario su creación.

Para ejecutar los contenedores, se debe ejecutar el siguiente comando:

```
docker-compose up -d
```
Para comprobar que los dos contenedores están en ejecución se puede revisar su estado de la siguiente manera:

```
docker ps
```
Finalmente, para generar los archivos estáticos que serán servidos por NGINX, se debe ejecutar este comando:
```
docker-compose exec web python manage.py collectstatic
```
### 2.3. Cambios y ajustes

Para realizar modificaciones sobre los puertos y los volúmenes de los contenedores, se pueden realizar sobre el archivo docker-compose.yml.

Para modificar la configuración de NGINX, se debe modificar el archivo default.conf.



## Autores

* **Julián David Torres Caicedo** - *Creación del sitio* - [juliant8805](https://github.com/juliant8805)
* **Liceth Barandica Diaz** - *Creación del sitio* - [licethbarandicadiaz](https://github.com/licethbarandicadiaz)
* **Daniel López** - *Configuración despliegue* - [danflop](https://github.com/danflop)

Programa de Evaluación y Monitoreo de la Biodiversidad, Instituto Alexander von Humboldt Colombia

## Licencia

Este proyecto es licenciado bajo licencia MIT - consulte [LICENSE.md](LICENSE.md) para mas detalles