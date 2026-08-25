# Backend-Visor-I2D

[![Django](https://img.shields.io/badge/Django-4.2_LTS-092E20?style=flat&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791?style=flat&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![PostGIS](https://img.shields.io/badge/PostGIS-3.4-4169E1?style=flat&logo=postgresql&logoColor=white)](https://postgis.net/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=flat&logo=docker&logoColor=white)](https://docs.docker.com/)

Versión actual: 1.2.1

El backend del Visor Geográfico I2D es un sistema robusto de información geográfica que permite la gestión, consulta y visualización de datos de biodiversidad. Desarrollado con Django y PostGIS, proporciona APIs REST completas para la interacción con registros biológicos georeferenciados. 

**Desarrollado por el [Instituto Alexander von Humboldt Colombia](http://www.humboldt.org.co)**
*Programa de Evaluación y Monitoreo de la Biodiversidad*

## 🚀 Estado Actual del Sistema

### ✅ **COMPLETAMENTE FUNCIONAL**
- **Django GIS**: PostGIS habilitado con GeometryField y operaciones espaciales
- **APIs REST**: Endpoints completos para departamentos, municipios, GBIF y proyectos
- **Base de Datos**: PostgreSQL 16 + PostGIS 3.4 con datos completos
- **Sistema de Proyectos**: Gestión dinámica de proyectos sin cambios de código
- **Búsqueda Geográfica**: API de búsqueda de municipios con coordenadas
- **Auditoría**: Script completo de métricas de rendimiento y optimización

## 📋 Características Principales

- **🗺️ Gestión Geoespacial**: Operaciones PostGIS con GeometryField para datos espaciales
- **📊 APIs REST Completas**: Endpoints para departamentos, municipios, GBIF y proyectos
- **🔍 Búsqueda Inteligente**: Sistema de búsqueda de municipios con manejo de acentos
- **📈 Sistema de Proyectos**: Gestión dinámica configurable vía base de datos
- **🔧 Auditoría Avanzada**: Métricas de rendimiento y optimización de consultas
- **🐳 Docker Ready**: Despliegue completo con Docker Compose
- **🔒 Seguridad**: Configuración CORS, ALLOWED_HOSTS y variables de entorno

## 🛠️ Stack Tecnológico

### Backend Core
- **Python**: 3.12
- **Django**: 4.2 LTS con django.contrib.gis
- **Django REST Framework**: 3.15.2
- **PostGIS**: Operaciones espaciales completas

### Base de Datos
- **PostgreSQL**: 16 con extensiones PostGIS 3.4
- **Esquemas**: django, gbif_consultas, capas_base, geovisor
- **Datos**: 8,702 municipios, 297 departamentos con geometrías

### Infraestructura
- **Servidor**: Gunicorn con 3 workers
- **Proxy**: Nginx para archivos estáticos
- **Contenedores**: Docker + Docker Compose
- **Monitoreo**: Health checks y logs estructurados

### 🔒 Compatibilidad y Seguridad
- **Python 3.12**: Versión estable actual con mejoras de seguridad y rendimiento
- **Django 4.2 LTS**: Soporte a largo plazo hasta abril 2026, actualizaciones de seguridad garantizadas
- **PostgreSQL 16**: Última versión estable con mejoras de rendimiento
- **Dependencias**: Todas las librerías actualizadas para resolver vulnerabilidades conocidas (CVE-2023-32681, etc.)
- **Matriz de Pruebas**: Verificado en Python 3.11+ y Django 4.2.16+

## 📋 Prerequisitos

### Para Desarrollo Local:
- Python 3.12+
- pip
- postgresql-dev, gcc, python3-dev, musl-dev
- PostgreSQL con PostGIS

### Para Producción (Recomendado):
- Docker 20.0+
- Docker Compose 2.0+
- Git 2.20+
- 4GB RAM mínimo (8GB recomendado)

## Configuración inicial

### Instalación y ejecución

Debe tener instalado python y pip en su equipo local, para la instalación de paquetes y ejecución del proyecto sin utilizar docker.

Clone el proyecto en su equipo e ingrese por línea de comandos al directorio del proyecto.

### 1.1. Clone el repositorio:

```
$ git clone https://github.com/PEM-Humboldt/visor-geografico-I2D-backend.git
```

### 1.2. Archivo secret.json (opcional)

El proyecto soporta configuración por variables de entorno (recomendado). El archivo `secret.json` es opcional y solo necesario si alguna librería requiere credenciales en formato JSON o si desea mantener compatibilidad con configuraciones previas. Si va a usar un archivo JSON, puede indicar su ruta con la variable de entorno `SECRET_FILE`.

Plantilla de `secret.json`:
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
Complete el archivo con las credenciales correspondientes y ubíquelo en una ruta segura (por ejemplo montado como volumen en producción). Para usarlo, defina `SECRET_FILE=/ruta/a/secret.json`. Si no define `SECRET_FILE`, el proyecto intentará usar `./secret.json` si existe.

### 1.3. Configuración de variables de entorno (.env)

El proyecto también soporta configuración mediante variables de entorno usando un archivo `.env`. Puede crear un archivo `.env` a partir de `env.example`:
`docker cp .env.example .env` 

Este archivo debe estar en la raíz del proyecto y debe hacer referencia a las siguientes variables:

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
DJANGO_SECRET_KEY=su-clave-secreta-django
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

# Configuración de archivos estáticos y media
STATIC_ROOT=/app/static
MEDIA_ROOT=/app/media

# Configuración de CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

#### Variables de S3
```bash
# Estas variables deben ser configuradas en caso de necesitar conexión con un S3
S3_ENDPOINT_URL=http://localhost:4566 # Never use '_' 
S3_BUCKET_NAME=visors3
S3_AUTH_TOKEN=token
S3_ACCESS_KEY=access_key
S3_SECRET_ACCESS_KEY=secret_access_key
S3_DEFAULT_REGION=sa-east-1
```

**Nota:** Las variables de entorno tienen prioridad sobre los valores del archivo `secret.json`. Si una variable está definida en ambos lugares, se usará el valor de la variable de entorno.

Además, si desea usar un archivo JSON para credenciales, exponga su ruta mediante `SECRET_FILE`. Por ejemplo:
```bash
SECRET_FILE=/run/secrets/i2d_backend.json
```

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

Él despliegue en producción de la aplicación se realizará utilizando [Gunicorn](https://gunicorn.org) como servidor de aplicaciones WSGI HTTP y [NGINX](https://www.nginx.com) como servidor web.

Por esta razón se utilizará un contenedor [Docker](https://www.docker.com) para cada componente: 1) *Django con Gunicorn* y 2) *NGINX*. El tercer componente es la base de datos, pero esa no está incluida en el alcance de este despligue y se asume su existencia.

La herramienta [Docker compose](https://docs.docker.com/compose/) se utilizará para la ejecución de los dos componentes y su interacción.

### 2.1. Instalación de Docker y Docker compose

Es necesario contar con la versión 19.03.13 de Docker o superior y Docker-compose versión 1.28.5.

La instalación se puede hacer siguiendo los pasos según el sistema operativo en la documentación oficial de Docker.

### 2.2. Despliegue

Una vez se haya clonado el repositorio, verificar que en la raíz del mismo se encuentren los siguientes archivos:

- dockerfile
- docker-compose.yml
- default.conf
- `.env` (preferiblemente) o de manera alternativa `secret.json` si decide usar archivo de secretos. En caso de optar por la segunda opción, recuerde indicar su ruta en la variable `SECRET_FILE`.

A continuación, desde la raíz del proyecto se debe ejecutar el siguiente comando para construir la imagen personalizada del contenedor que ejecutará el componente de Django con Gunicorn:

```
docker compose build
```
Se utilizará la  imagen  oficial del contenedor de NGINX que se encuentra [aquí](https://hub.docker.com/_/nginx), y por lo tanto no es necesario su creación.

Para ejecutar los contenedores, se debe ejecutar el siguiente comando:

```
docker compose up -d
```
Para comprobar que los dos contenedores están en ejecución se puede revisar su estado de la siguiente manera:

```
docker ps
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

El script ejecuta múltiples consultas organizadas en dos secciones:

#### **Sección 1: Verificación de Infraestructura **
- **Conectividad**: Verifica conexión a la base de datos y versión de PostgreSQL
- **Esquemas**: Lista todos los esquemas disponibles y permisos de acceso
- **Tablas**: Inventario de tablas por esquema con información de propietarios
- **Índices**: Documentación de índices para optimización
- **Extensiones**: Lista extensiones instaladas (PostGIS, etc.)
- **Restricciones**: Documenta claves foráneas y integridad referencial
- **Tamaños**: Análisis de uso de almacenamiento por base de datos
- **Conexiones**: Monitoreo de conexiones activas

#### **Sección 2: Consultas del Backend **
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

# Iniciar los contenedores si está detenido
docker compose up -d
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

---

## 🌐 APIs y Endpoints

### 📍 Endpoints Geográficos

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/api/dpto/` | GET | Lista todos los departamentos con geometrías |
| `/api/mpio/` | GET | Lista todos los municipios con geometrías |
| `/api/mpio/search/<term>/` | GET | Búsqueda de municipios por nombre |

### 🗂️ Endpoints de Proyectos

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/api/projects/` | GET | Lista todos los proyectos disponibles |
| `/api/projects/<name>/` | GET | Obtiene proyecto específico por nombre |

### 🐛 Endpoints GBIF

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/api/gbif/gbifinfo/` | GET | Información general de registros GBIF |
| `/api/gbif/descargar-zip/` | GET | Descarga masiva en ZIP por región |

### 🔧 Endpoints de Sistema

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/admin/` | GET | Panel de administración Django |
| `/health/` | GET | Health check del sistema |
| `/static/` | GET | Archivos estáticos |

### 📊 Ejemplos de Uso

```bash
# Buscar municipios
curl "http://localhost:8001/api/mpio/search/medellin"

# Obtener proyecto específico
curl "http://localhost:8001/api/projects/HU-VisorI2D-0001/"

# Descargar datos por departamento
curl "http://localhost:8001/api/gbif/descargar-zip/?codigo_dpto=05&nombre=Antioquia"

# Health check
curl "http://localhost:8001/health"
```

---

## 🔧 Funcionalidades Avanzadas

### 🗺️ Operaciones PostGIS

El sistema utiliza Django GIS con PostGIS para operaciones espaciales:

```python
# Ejemplos de consultas espaciales disponibles
from applications.dpto.models import Departamento
from applications.mupio.models import Municipio

# Obtener área de un departamento
dpto = Departamento.objects.get(codigo='05')
area = dpto.geom.area  # Área en unidades del sistema de coordenadas

# Obtener centroide de un municipio
mpio = Municipio.objects.get(codigo='05001')
centroide = mpio.geom.centroid  # Punto central

# Consultas espaciales
municipio_dentro = Municipio.objects.filter(geom__within=dpto.geom)
```

### 🔍 Sistema de Búsqueda Inteligente

Implementa búsqueda con manejo de acentos y caracteres especiales:

```python
# Búsqueda insensible a acentos
resultados = mpioSearch(request, 'medellin')  # Encuentra "Medellín"
resultados = mpioSearch(request, 'bogota')    # Encuentra "Bogotá"
```

### 📈 Sistema de Proyectos Dinámico

Permite configurar nuevos proyectos sin cambios de código:

```python
# Modelo Project permite configuración dinámica
project = Project.objects.create(
    name="HU-VisorI2D-0002",
    title="Nuevo Proyecto",
    description="Descripción del proyecto",
    is_active=True
)
```

---

## 📊 Métricas y Rendimiento

### 🚀 Benchmarks Actuales

| Consulta | Tiempo Promedio | Registros | Estado |
|----------|----------------|-----------|--------|
| Lista Departamentos | < 50ms | 297 | ✅ Óptimo |
| Lista Municipios | < 100ms | 8,702 | ✅ Óptimo |
| Búsqueda Municipios | < 200ms | Variable | ✅ Bueno |
| Consultas GBIF | < 500ms | Variable | ⚠️ Optimizable |

### 📈 Optimizaciones Implementadas

- **Índices Espaciales**: Índices GIST en campos de geometría
- **Consultas Específicas**: Evita SELECT * en tablas grandes
- **Límites de Resultados**: LIMIT aplicado en consultas de auditoría
- **Conexión Pooling**: Configuración optimizada de PostgreSQL

### 🔍 Auditoría Continua

Usa el script de auditoría para monitoreo regular:

```bash
# Ejecutar auditoría semanal
cd docs/
./database_audit.sh weekly_audit_$(date +%Y%m%d).md
```

---

## 🔄 Changelog Reciente

### ✅ Versión Actual (2025-08-28)

#### Funcionalidades Implementadas:
- **Django GIS Completo**: PostGIS habilitado con GeometryField
- **API de Búsqueda**: Endpoint `/api/mpio/search/<term>/` funcional
- **Sistema de Proyectos**: APIs REST para gestión dinámica
- **Auditoría de BD**: Script completo con métricas de rendimiento
- **Optimización**: Consultas espaciales optimizadas

#### Correcciones Críticas:
- **DisallowedHost**: ALLOWED_HOSTS configurado correctamente
- **Docker Volumes**: Mapeo corregido a `/project`
- **Variables de Entorno**: Soporte completo para configuración
- **Static Files**: Servicio de archivos estáticos en desarrollo

#### Mejoras de Rendimiento:
- **Índices Espaciales**: Implementados en campos de geometría
- **Query Optimization**: Consultas específicas sin SELECT *
- **Connection Pooling**: Configuración PostgreSQL optimizada

---

## 🤝 Contribución

### 👥 Equipo de Desarrollo

- **Julián David Torres Caicedo** - *Desarrollo Backend* - [juliant8805](https://github.com/juliant8805)
- **Liceth Barandica Diaz** - *Desarrollo Backend* - [licethbarandicadiaz](https://github.com/licethbarandicadiaz)
- **Daniel López** - *DevOps y Despliegue* - [danflop](https://github.com/danflop)

### 📝 Cómo Contribuir

1. Fork el repositorio
2. Crear rama de feature (`git checkout -b feature/nueva-api`)
3. Implementar cambios con tests
4. Ejecutar auditoría: `./docs/database_audit.sh`
5. Commit siguiendo Conventional Commits
6. Push y crear Pull Request

### 🧪 Testing

```bash
# Tests unitarios
python manage.py test

# Tests de APIs
curl http://localhost:8001/api/dpto/
curl http://localhost:8001/api/mpio/search/bogota/

# Auditoría de rendimiento
./docs/database_audit.sh
```

---

## 📞 Soporte

### 🏢 Instituto Alexander von Humboldt Colombia
- **Programa**: Evaluación y Monitoreo de la Biodiversidad
- **Website**: [http://www.humboldt.org.co](http://www.humboldt.org.co)

### 🐛 Reportar Issues
- **GitHub**: [Reportar problema](https://github.com/maccevedor/visor-geografico-I2D-backend/issues)
- **Documentación**: Ver auditoría de base de datos para métricas

### 📚 Recursos Técnicos
- [Django GIS Documentation](https://docs.djangoproject.com/en/4.2/ref/contrib/gis/)
- [PostGIS Documentation](https://postgis.net/documentation/)
- [Django REST Framework](https://www.django-rest-framework.org/)

## 📄 Licencia

Este proyecto está licenciado bajo la Licencia MIT - consulte [LICENSE.md](LICENSE.md) para más detalles.

---

<div align="center">

**🌱 Desarrollado con ❤️ para la conservación de la biodiversidad colombiana**

[![Instituto Humboldt](https://img.shields.io/badge/Instituto-Humboldt-green?style=for-the-badge)](http://www.humboldt.org.co)

</div>
