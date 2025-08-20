# Backend Technical Documentation - Visor I2D Humboldt Project

## Executive Summary

The Visor I2D backend is a Django-based REST API that serves Colombian biodiversity data for the Instituto Alexander von Humboldt's geographic visualization platform. The system provides endpoints for querying biological records, species information, and geographic data across departments and municipalities.

## Table of Contents

1. [System Architecture](#system-architecture)
2. [Technology Stack](#technology-stack)
3. [Application Modules](#application-modules)
4. [API Endpoints](#api-endpoints)
5. [Database Configuration](#database-configuration)
6. [Development Setup](#development-setup)
7. [Testing Strategy](#testing-strategy)
8. [Security Considerations](#security-considerations)
9. [Performance Optimization](#performance-optimization)
10. [Improvement Plan](#improvement-plan)

---

## System Architecture

### Overview
The backend follows Django's MVT (Model-View-Template) pattern with Django REST Framework for API functionality:

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │────│   Django REST   │────│   PostgreSQL    │
│   (External)    │    │   Framework     │    │   Database      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                       ┌─────────────────┐
                       │   Applications  │
                       │   - dpto        │
                       │   - mupio       │
                       │   - gbif        │
                       │   - user        │
                       └─────────────────┘
```

### Core Components
- **Django 3.1.7**: Web framework
- **Django REST Framework 3.12.2**: API functionality
- **PostgreSQL**: Primary database
- **Docker**: Containerization
- **NGINX**: Reverse proxy (production)

---

## Technology Stack

### Backend Framework
- **Django 3.1.7**: Main web framework
- **Django REST Framework 3.12.2**: RESTful API development
- **Python 3.9.2**: Programming language

### Database
- **PostgreSQL**: Primary database engine
- **psycopg2 2.9.9**: PostgreSQL adapter for Python

### Additional Libraries
```python
# Core Dependencies
asgiref==3.3.1
Django==3.1.7
djangorestframework==3.12.2
psycopg2==2.9.9

# Utilities
django-cors-headers  # CORS handling
unidecode==1.3.6    # Text normalization
unicode==2.9        # Unicode support
gunicorn            # WSGI server

# Development Tools
pylint==2.7.1
pylint-django==2.4.2
```

### Deployment
- **Docker**: Containerization
- **Docker Compose**: Multi-container orchestration
- **Gunicorn**: WSGI HTTP Server
- **NGINX**: Reverse proxy and static file serving

---

## Application Modules

### 1. **dpto** (Departments)
**Purpose**: Handles department-level biodiversity queries

**Models**:
- `DptoQueries`: Biodiversity statistics by department
  - `codigo`: Department code (5 chars)
  - `tipo`: Record type
  - `registers`: Number of biological records
  - `species`: Number of species
  - `exoticas`: Exotic species count
  - `endemicas`: Endemic species count
  - `geom`: Geographic geometry (TEXT field)
  - `nombre`: Department name

- `DptoAmenazas`: Threatened species by department
  - `codigo`: Department code
  - `tipo`: Threat category
  - `amenazadas`: Number of threatened species
  - `geom`: Geographic geometry
  - `nombre`: Department name

**Views**:
- `dptoQuery`: Lists biodiversity data by department code
- `dptoDanger`: Lists threatened species by department

### 2. **mupio** (Municipalities)
**Purpose**: Municipality-level biodiversity data

**Models**:
- `MpioQueries`: Similar structure to DptoQueries but for municipalities
- `MpioAmenazas`: Threatened species data for municipalities

**Features**:
- Municipality-specific biodiversity statistics
- Geographic boundary data
- Species threat assessment

### 3. **mupiopolitico** (Political Municipalities)
**Purpose**: Political/administrative municipality data

**Features**:
- Administrative boundaries
- Political divisions
- Municipal metadata

### 4. **gbif** (Global Biodiversity Information Facility)
**Purpose**: GBIF data integration and metadata

**Models**:
- `gbifInfo`: GBIF download metadata
  - `download_date`: Date of data download
  - `doi`: Digital Object Identifier for citations

**Features**:
- GBIF data synchronization
- Citation management
- Data provenance tracking

### 5. **user** (User Management)
**Purpose**: User authentication and management

**Features**:
- User registration and authentication
- Permission management
- User profile data

---

## API Endpoints

### Department Endpoints
```
GET /dpto/{codigo}/          # Get biodiversity data for department
GET /dpto/{codigo}/danger/   # Get threatened species for department
```

### Municipality Endpoints
```
GET /mupio/{codigo}/         # Get biodiversity data for municipality
GET /mupio/{codigo}/danger/  # Get threatened species for municipality
```

### GBIF Endpoints
```
GET /gbif/info/             # Get GBIF metadata and download information
```

### Response Format
All endpoints return JSON responses with the following structure:
```json
{
  "count": 123,
  "next": "http://api.example.com/endpoint/?page=2",
  "previous": null,
  "results": [
    {
      "codigo": "05",
      "nombre": "Antioquia",
      "tipo": "Plantae",
      "registers": 15420,
      "species": 2341,
      "exoticas": 45,
      "endemicas": 123
    }
  ]
}
```

---

## Database Configuration

### Current Setup
- **Engine**: `django.db.backends.postgresql_psycopg2`
- **Database**: `i2d_db`
- **User**: `i2d_user`
- **Schema Search Path**: `django,gbif_consultas,capas_base,geovisor`

### Schema Organization
- **django**: Django application tables
- **gbif_consultas**: GBIF query results and data
- **capas_base**: Base geographic layers
- **geovisor**: Geographic viewer data

### Data Models
All models use `managed = False` indicating they represent database views or external tables:
- No Django migrations for model structure
- Direct database table/view mapping
- Read-only access pattern

---

## Development Setup

### Prerequisites
- Python 3.9.2
- pip
- postgresql-dev
- gcc
- python3-dev
- musl-dev

### Local Development
```bash
# Clone repository
git clone <repository-url>
cd visor-geografico-I2D-backend

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your database credentials

# Run migrations (if any)
python manage.py migrate

# Start development server
python manage.py runserver
```

### Docker Development
```bash
# Build and start containers
docker-compose up -d

# View logs
docker-compose logs -f

# Access backend container
docker exec -it visor_i2d_backend bash
```

### Environment Variables
```bash
# Database Configuration
DB_ENGINE=django.db.backends.postgresql_psycopg2
DB_NAME=i2d_db
DB_USER=i2d_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
DB_OPTIONS=-c search_path=django,gbif_consultas,capas_base,geovisor

# CORS Configuration
CORS_ALLOWED_ORIGINS=https://i2d.humboldt.org.co,http://localhost:1234

# Debug Settings
DEBUG=true
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
```

---

## Testing Strategy

### Current State
⚠️ **Limited Testing Infrastructure**: The project currently lacks comprehensive testing coverage.

### Recommended Testing Approach

#### 1. **Unit Tests**
```python
# Example test structure
from django.test import TestCase
from applications.dpto.models import DptoQueries

class DptoQueriesTestCase(TestCase):
    def setUp(self):
        # Test data setup
        pass
    
    def test_department_query(self):
        # Test department data retrieval
        pass
    
    def test_species_count(self):
        # Test species counting logic
        pass
```

#### 2. **API Integration Tests**
```python
from rest_framework.test import APITestCase
from django.urls import reverse

class DptoAPITestCase(APITestCase):
    def test_dpto_endpoint(self):
        url = reverse('dpto-query', kwargs={'kid': '05'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
```

#### 3. **Database Tests**
- Test database connectivity
- Validate schema access
- Test query performance
- Verify data integrity

---

## Security Considerations

### Current Security Measures
- **CORS Headers**: Configured for specific origins
- **Secret Key Management**: Stored in `secret.json`
- **Database Credentials**: Environment variable configuration

### Security Recommendations
1. **Input Validation**: Implement comprehensive input sanitization
2. **Rate Limiting**: Add API rate limiting
3. **Authentication**: Implement proper API authentication
4. **HTTPS**: Enforce HTTPS in production
5. **SQL Injection Prevention**: Use parameterized queries
6. **Error Handling**: Implement secure error responses

---

## Performance Optimization

### Current Performance Characteristics
- **Database Views**: Using unmanaged models for read-only access
- **Query Optimization**: Limited to basic Django ORM
- **Caching**: No caching layer implemented

### Optimization Opportunities
1. **Database Indexing**: Add indexes for frequently queried fields
2. **Query Optimization**: Implement select_related and prefetch_related
3. **Caching Layer**: Add Redis for API response caching
4. **Database Connection Pooling**: Implement connection pooling
5. **API Pagination**: Optimize pagination for large datasets

---

## Improvement Plan

### Phase 1: Foundation Improvements (Weeks 1-2)

#### 1.1 **OpenAPI/Swagger Integration** 🎯
**Objective**: Implement comprehensive API documentation

**Tasks**:
- Install `drf-spectacular` or `drf-yasg`
- Configure OpenAPI schema generation
- Add endpoint documentation
- Implement interactive API explorer

**Implementation**:
```python
# requirements.txt
drf-spectacular==0.26.2

# settings.py
INSTALLED_APPS = [
    # ... existing apps
    'drf_spectacular',
]

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Visor I2D API',
    'DESCRIPTION': 'Colombian Biodiversity Data API',
    'VERSION': '1.0.0',
}
```

**Deliverables**:
- Interactive API documentation at `/api/docs/`
- OpenAPI schema at `/api/schema/`
- Comprehensive endpoint documentation

#### 1.2 **Unit Testing Implementation** 🧪
**Objective**: Establish comprehensive testing framework

**Tasks**:
- Create test structure for each application
- Implement model tests
- Add API endpoint tests
- Set up test database configuration

**Implementation**:
```python
# Test structure
tests/
├── __init__.py
├── test_models.py
├── test_views.py
├── test_serializers.py
└── test_integration.py

# Example test
class TestDptoAPI(APITestCase):
    def setUp(self):
        self.department_code = '05'
    
    def test_dpto_query_endpoint(self):
        url = f'/dpto/{self.department_code}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('results', response.data)
```

**Deliverables**:
- 80%+ test coverage
- Automated test execution
- CI/CD integration ready

### Phase 2: Enhanced Features (Weeks 3-4)

#### 2.1 **API Authentication & Authorization** 🔐
**Tasks**:
- Implement JWT authentication
- Add API key management
- Create user permission system
- Add rate limiting

#### 2.2 **Performance Optimization** ⚡
**Tasks**:
- Add Redis caching layer
- Implement database query optimization
- Add API response compression
- Optimize serializers

#### 2.3 **Monitoring & Logging** 📊
**Tasks**:
- Implement structured logging
- Add performance monitoring
- Create health check endpoints
- Add error tracking

### Phase 3: Advanced Features (Weeks 5-6)

#### 3.1 **Data Validation & Quality** ✅
**Tasks**:
- Implement comprehensive input validation
- Add data quality checks
- Create data integrity tests
- Implement error handling improvements

#### 3.2 **API Versioning** 🔄
**Tasks**:
- Implement API versioning strategy
- Create backward compatibility layer
- Add deprecation warnings
- Document migration paths

#### 3.3 **Geographic Data Enhancement** 🗺️
**Tasks**:
- Evaluate PostGIS integration
- Implement spatial query optimization
- Add geographic data validation
- Create spatial API endpoints

### Phase 4: Production Readiness (Weeks 7-8)

#### 4.1 **Security Hardening** 🛡️
**Tasks**:
- Security audit and penetration testing
- Implement security headers
- Add input sanitization
- Create security documentation

#### 4.2 **Deployment Optimization** 🚀
**Tasks**:
- Optimize Docker configuration
- Implement health checks
- Add deployment automation
- Create monitoring dashboards

#### 4.3 **Documentation & Training** 📚
**Tasks**:
- Complete API documentation
- Create developer guides
- Add deployment documentation
- Conduct team training

---

## Implementation Timeline

| Phase | Duration | Key Deliverables | Priority |
|-------|----------|------------------|----------|
| **Phase 1** | 2 weeks | OpenAPI docs, Unit tests | High |
| **Phase 2** | 2 weeks | Auth, Performance, Monitoring | High |
| **Phase 3** | 2 weeks | Validation, Versioning, GIS | Medium |
| **Phase 4** | 2 weeks | Security, Deployment, Docs | Medium |

---

## Success Metrics

### Technical Metrics
- **API Response Time**: < 200ms average
- **Test Coverage**: > 80%
- **API Documentation**: 100% endpoint coverage
- **Uptime**: > 99.9%

### Quality Metrics
- **Code Quality**: Pylint score > 8.0
- **Security**: Zero high-severity vulnerabilities
- **Performance**: Handle 1000+ concurrent requests
- **Maintainability**: Clear documentation and tests

---

## Conclusion

The Visor I2D backend provides a solid foundation for serving Colombian biodiversity data. The improvement plan focuses on modernizing the codebase with industry best practices including comprehensive testing, API documentation, and performance optimization.

Key priorities:
1. **Immediate**: OpenAPI documentation and unit testing
2. **Short-term**: Authentication and performance optimization
3. **Long-term**: Advanced features and production hardening

This roadmap will transform the backend into a robust, well-documented, and maintainable API platform suitable for production deployment and future scaling.