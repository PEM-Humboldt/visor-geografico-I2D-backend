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

### 1.3. Configuración de variables de entorno (.env)

El proyecto también soporta configuración mediante variables de entorno usando un archivo `.env`. Crear un archivo `.env` en la raíz del proyecto con las siguientes variables:

#### Variables de base de datos:
```bash
# Configuración de base de datos
DB_ENGINE=django.db.backends.postgresql_psycopg2
DB_NAME=nombre_de_tu_base_de_datos
DB_USER=usuario_de_base_de_datos
DB_PASSWORD=contraseña_de_base_de_datos
DB_HOST=localhost
DB_PORT=5432
DB_OPTIONS=-c search_path=django,gbif_consultas,capas_base,geovisor
```

#### Variables de configuración general:
```bash
# Configuración de Django
DEBUG=true
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

# Configuración de archivos estáticos y media
STATIC_ROOT=/app/static
MEDIA_ROOT=/app/media

# Configuración de CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

**Nota:** Las variables de entorno tienen prioridad sobre los valores del archivo `secret.json`. Si una variable está definida en ambos lugares, se usará el valor de la variable de entorno.

### 1.4. Instalación de paquetes:
Ubíquese en la carpeta raíz del proyecto y ejecute la siguiente sentencia para instalar las dependencias del proyecto:
```
    pip install -r requirements.txt
```
### 1.5. Para crear nuevos modelos automáticamente en el entorno del administrador
Verifique que no hay errores
```
    python manage.py makemigrations
```
Migre los modelos
```
    python manage.py migrate
```
### 1.6. Ejecución en entorno de desarrollo:
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

## Auditoría de Base de Datos

### 3.1. Script de Auditoría

El proyecto incluye un script de auditoría de base de datos (`docs/database_audit.sh`) que permite verificar el estado de la base de datos, esquemas, tablas, y probar las consultas del backend con parámetros reales.

### 3.2. Requisitos

- Docker y Docker-compose ejecutándose
- Contenedor de base de datos `visor_i2d_db` activo
- Comando `bc` instalado para cálculos de tiempo

### 3.3. Ejecución del Script

#### Comando básico:
```bash
# Desde el directorio docs/
cd docs/
./database_audit.sh
```

#### Con archivo de salida personalizado:
```bash
# Generar reporte con nombre específico
./database_audit.sh mi_auditoria.md

# Generar reporte en directorio específico
./database_audit.sh docs/auditoria_completa.md
```

#### Verificar ayuda:
```bash
./database_audit.sh --help
```

### 3.4. Qué hace el Script

El script ejecuta **24 consultas** organizadas en dos secciones:

#### **Sección 1: Verificación de Infraestructura (14 consultas)**
- **Conectividad**: Verifica conexión a la base de datos y versión de PostgreSQL
- **Esquemas**: Lista todos los esquemas disponibles y permisos de acceso
- **Tablas**: Inventario de tablas por esquema con información de propietarios
- **Índices**: Documentación de índices para optimización
- **Extensiones**: Lista extensiones instaladas (PostGIS, etc.)
- **Restricciones**: Documenta claves foráneas y integridad referencial
- **Tamaños**: Análisis de uso de almacenamiento por base de datos
- **Conexiones**: Monitoreo de conexiones activas

#### **Sección 2: Consultas del Backend (10 consultas)**
- **Biodiversidad por Departamento**: Prueba consultas de especies por departamento
- **Especies Amenazadas**: Verifica datos de conservación por región
- **Biodiversidad por Municipio**: Prueba consultas municipales
- **Búsqueda de Municipios**: Verifica búsqueda con manejo de acentos
- **Información GBIF**: Prueba acceso a metadatos de descargas
- **Exportación de Registros**: Verifica consultas de exportación
- **Listas de Especies**: Prueba generación de listas taxonómicas

### 3.5. Interpretación de Resultados

#### **Tiempos de Ejecución**
- **< 100ms**: Rendimiento excelente
- **100-500ms**: Rendimiento aceptable
- **> 500ms**: Requiere optimización

#### **Códigos de Muestra Utilizados**
El script usa parámetros reales de la base de datos:
- **Departamento**: Código obtenido dinámicamente (ej: '52' = Nariño)
- **Municipio**: Código obtenido dinámicamente (ej: '05001' = Medellín)
- **Búsqueda**: Texto de muestra para búsquedas (ej: 'APART' = Apartadó)

#### **Estructura del Reporte**
Cada consulta incluye:
- **Tiempo de ejecución** en milisegundos
- **Ubicación del archivo** en el código fuente
- **Propósito** de la consulta
- **Query SQL** ejecutada
- **Resultados** con número de filas retornadas

### 3.6. Optimizaciones Implementadas

El script ha sido optimizado para evitar problemas de rendimiento:

- **Sin SELECT \***: Evita cargar columnas de geometría grandes
- **LIMIT aplicado**: Todas las consultas tienen límite de resultados
- **Columnas específicas**: Solo selecciona campos necesarios
- **Timeouts configurados**: Previene consultas colgadas
- **Parámetros dinámicos**: Usa datos reales de la base de datos

### 3.7. Solución de Problemas

#### Error: "Container not running"
```bash
# Verificar contenedores activos
docker ps

# Iniciar contenedor si está detenido
docker-compose up -d db
```

#### Error: "bc command not found"
```bash
# Ubuntu/Debian
sudo apt-get install bc

# Alpine Linux
apk add bc
```

#### Error: "Permission denied"
```bash
# Dar permisos de ejecución
chmod +x docs/database_audit.sh
```

### 3.8. Archivos Generados

El script genera un reporte en formato Markdown con:
- **Timestamp** de generación
- **Métricas de rendimiento** para cada consulta
- **Resultados completos** con datos de muestra
- **Recomendaciones** para optimización
- **Resumen ejecutivo** con hallazgos clave

**Ejemplo de salida**: `database_audit_20250815_080527.md`

## Autores

* **Julián David Torres Caicedo** - *Creación del sitio* - [juliant8805](https://github.com/juliant8805)
* **Liceth Barandica Diaz** - *Creación del sitio* - [licethbarandicadiaz](https://github.com/licethbarandicadiaz)
* **Daniel López** - *Configuración despliegue* - [danflop](https://github.com/danflop)

Programa de Evaluación y Monitoreo de la Biodiversidad, Instituto Alexander von Humboldt Colombia

## Licencia

Este proyecto es licenciado bajo licencia MIT - consulte [LICENSE.md](LICENSE.md) para mas detalles
