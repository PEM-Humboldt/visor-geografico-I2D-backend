# Backend-Visor-I2D
El backend visor geografico I2D es un proyecto que permite interactuar con una base de datos de información geográfica que contiene información de registros biológicos.

Este proyecto ha sido desarrollado por el [Instituto Humboldt](http://www.humboldt.org.co). El proyecto usa [Python 3.9.2](https://www.python.org/), junto al framework web de alto nivel [DJANGO](https://www.djangoproject.com/) y a paquetes como [Django Rest Framework](https://www.django-rest-framework.org/) y [psycopg2](https://pypi.org/project/psycopg2/)

Esta es una version preliminar y se implementarán nuevas funcionalidades.

## Configuración inicial

### Instalación y ejecución

Debe tener instalado python y pip en su equipo local, para la instalación de paquetes y ejecución del proyecto. Clone el proyecto en su equipo e ingrese por línea de comandos al directorio del proyecto.

### 1.1. Clone el repositorio:

```
$ git clone https://github.com/PEM-Humboldt/visor-geografico-I2D-backend.git
```

### 1.2. Entorno virtual:
Ubiquese en la carpeta de Scripts y active el entorno virtual:

```
cd env/i2d-backend/Scripts

.\activate
```

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
### 1.4. Ejecución:
Ejecute la siguiente instrucción:

```
    python manage.py runserver
```
La instrucción iniciará el proyecto en su entorno local.

<!-- 
## Despliegue

### 2.1. Compilación del proyecto
Para desplegar el proyecto, ejecute la siguiente instrucción:
    
    npm run build

### 2.2. Despliegue

Para el caso de apache-tomcat:

- Copie la carpeta *build* en el directorio de despliegue según el servidor web seleccionado. Posteriormente inicie el servidor
```
/DIRECTORIO-APACHE-TOMCAT/webapps/
```
- Inicie el servicio de tomcat
```
/DIRECTORIO-APACHE-TOMCAT/bin/startup.sh
``` -->

## Autores

* **Julián David Torres Caicedo** - *Creación del sitio* - [juliant8805](https://github.com/juliant8805)
* **Liceth Barandica Diaz** - *Creación del sitio* - [licethbarandicadiaz](https://github.com/licethbarandicadiaz)

Ingeniería de Datos y Desarrollo, Programa de Evaluación y Monitoreo de la Biodiversidad, Instituto Alexander von Humboldt Colombia

## Licencia

Este proyecto es licenciado bajo licencia MIT - consulte [LICENSE.md](LICENSE.md) para mas detalles