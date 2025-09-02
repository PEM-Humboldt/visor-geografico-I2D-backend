# API Documentation - Visor I2D Backend

## Overview

The Visor I2D API provides access to Colombian biodiversity data from the Instituto Alexander von Humboldt. This RESTful API serves geographic and species occurrence data for departments, municipalities, and GBIF records.

## Base URL

```
Production: https://i2d.humboldt.org.co/api/
Development: http://localhost:8001/api/
```

## Authentication

### Public Endpoints
Most data endpoints are publicly accessible for read operations.

### Authenticated Endpoints
- Admin operations require authentication
- Rate limits are higher for authenticated users

### API Keys
Contact the Instituto Alexander von Humboldt for API key access.

## Rate Limits

- **Anonymous**: 100 requests/hour
- **Authenticated**: 1000 requests/hour

## Health Endpoints

### GET /health/
Comprehensive health check with detailed system status.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": 1692614400.123,
  "checks": {
    "database": {
      "status": "healthy",
      "response_time_ms": 45.2
    },
    "cache": {
      "status": "healthy"
    }
  }
}
```

### GET /health/simple/
Simple health check for load balancers.

**Response:**
```json
{
  "status": "OK",
  "timestamp": 1692614400.123
}
```

## Department Endpoints

### GET /dpto/
List all Colombian departments with biodiversity data.

**Parameters:**
- `limit` (optional): Number of results (default: 20, max: 100)
- `offset` (optional): Pagination offset

**Response:**
```json
{
  "count": 32,
  "next": null,
  "previous": null,
  "results": [
    {
      "codigo_dpto": "05",
      "nombre_dpto": "Antioquia",
      "especies_count": 15420,
      "registros_count": 89567,
      "geometry": "MULTIPOLYGON(...)"
    }
  ]
}
```

### GET /dpto/{codigo}/
Get specific department data.

**Parameters:**
- `codigo`: Department code (e.g., "05", "11", "25")

**Response:**
```json
{
  "codigo_dpto": "05",
  "nombre_dpto": "Antioquia",
  "especies_count": 15420,
  "registros_count": 89567,
  "geometry": "MULTIPOLYGON(...)",
  "municipios": [
    {
      "codigo_mpio": "05001",
      "nombre_mpio": "Medellín"
    }
  ]
}
```

## Municipality Endpoints

### GET /mpio/
List all Colombian municipalities with biodiversity data.

**Parameters:**
- `dpto` (optional): Filter by department code
- `limit` (optional): Number of results
- `offset` (optional): Pagination offset

**Response:**
```json
{
  "count": 1122,
  "results": [
    {
      "codigo_mpio": "05001",
      "nombre_mpio": "Medellín",
      "codigo_dpto": "05",
      "especies_count": 2340,
      "registros_count": 12456,
      "geometry": "MULTIPOLYGON(...)"
    }
  ]
}
```

### GET /mpio/{codigo}/
Get specific municipality data.

**Parameters:**
- `codigo`: Municipality code (5 digits, e.g., "05001")

## GBIF Endpoints

### GET /gbif/
Search GBIF occurrence records.

**Parameters:**
- `species` (optional): Scientific species name
- `dpto` (optional): Department code
- `mpio` (optional): Municipality code
- `year` (optional): Occurrence year
- `limit` (optional): Number of results (max: 1000)

**Response:**
```json
{
  "count": 5678,
  "results": [
    {
      "gbif_id": "123456789",
      "species_name": "Puma concolor",
      "latitude": 6.2442,
      "longitude": -75.5812,
      "occurrence_date": "2023-05-15",
      "department": "Antioquia",
      "municipality": "Medellín",
      "basis_of_record": "HUMAN_OBSERVATION"
    }
  ]
}
```

### GET /gbif/species/
List unique species in the database.

**Parameters:**
- `search` (optional): Search species names
- `dpto` (optional): Filter by department

**Response:**
```json
{
  "count": 45678,
  "results": [
    {
      "species_name": "Puma concolor",
      "common_name": "Puma",
      "family": "Felidae",
      "order": "Carnivora",
      "occurrence_count": 234
    }
  ]
}
```

## Error Responses

### 400 Bad Request
```json
{
  "error": "Validation Error",
  "message": "Invalid department code",
  "code": "VALIDATION_ERROR",
  "timestamp": "2023-08-21T12:00:00Z"
}
```

### 404 Not Found
```json
{
  "error": "Not Found",
  "message": "Department with code '99' not found",
  "code": "NOT_FOUND"
}
```

### 429 Too Many Requests
```json
{
  "error": "Rate Limit Exceeded",
  "message": "Rate limit of 100 requests/hour exceeded",
  "code": "RATE_LIMIT_EXCEEDED",
  "retry_after": 3600
}
```

### 500 Internal Server Error
```json
{
  "error": "Internal Server Error",
  "message": "An unexpected error occurred",
  "code": "INTERNAL_ERROR",
  "timestamp": "2023-08-21T12:00:00Z"
}
```

## Data Formats

### Geographic Data
- **Format**: GeoJSON/WKT
- **Coordinate System**: WGS84 (EPSG:4326)
- **Geometry Types**: Point, MultiPolygon

### Date Formats
- **ISO 8601**: `YYYY-MM-DD`
- **Examples**: `2023-08-21`, `2023-12-31`

### Species Names
- **Format**: Scientific nomenclature
- **Example**: `Puma concolor`
- **Validation**: Genus species format required

## Usage Examples

### Python
```python
import requests

# Get all departments
response = requests.get('http://localhost:8001/dpto/')
departments = response.json()

# Get specific department
response = requests.get('http://localhost:8001/dpto/05/')
antioquia = response.json()

# Search GBIF records
params = {
    'species': 'Puma concolor',
    'dpto': '05',
    'limit': 100
}
response = requests.get('http://localhost:8001/gbif/', params=params)
records = response.json()
```

### JavaScript
```javascript
// Fetch departments
fetch('http://localhost:8001/dpto/')
  .then(response => response.json())
  .then(data => console.log(data));

// Search with parameters
const params = new URLSearchParams({
  species: 'Puma concolor',
  dpto: '05'
});

fetch(`http://localhost:8001/gbif/?${params}`)
  .then(response => response.json())
  .then(data => console.log(data));
```

### cURL
```bash
# Get departments
curl -X GET "http://localhost:8001/dpto/"

# Get specific municipality
curl -X GET "http://localhost:8001/mpio/05001/"

# Search GBIF with filters
curl -X GET "http://localhost:8001/gbif/?species=Puma%20concolor&dpto=05"
```

## Interactive Documentation

- **Swagger UI**: `/api/docs/`
- **ReDoc**: `/api/redoc/`
- **OpenAPI Schema**: `/api/schema/`

## Support

For technical support or API access requests:
- **Email**: contact@humboldt.org.co
- **Documentation**: https://i2d.humboldt.org.co/docs/
- **GitHub**: https://github.com/maccevedor/visor-geografico-I2D-backend
