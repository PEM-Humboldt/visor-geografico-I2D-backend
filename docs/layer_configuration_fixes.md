# Layer Configuration Fixes - September 1, 2025

## Overview
This document describes the layer configuration fixes applied to resolve GeoServer WMS request issues in the Visor I2D Humboldt project.

## Problem Description
The frontend was displaying 9 layer groups (hardcoded) but the API only returned 4 layer groups for the "general" project. Additionally, some layers had incorrect GeoServer workspace configurations causing WMS request failures.

## Root Cause Analysis
1. **Missing Layer Groups**: Database was missing 6 layer groups that were hardcoded in the frontend
2. **Incorrect Workspace Configuration**: New layers were assigned to wrong GeoServer workspaces
3. **Non-existent Layers**: Some layers referenced in frontend didn't exist in GeoServer

## Solutions Applied

### 1. Added Missing Layer Groups
Created 6 new layer groups for the general project:

- **Capas Base** (orden: 0) - Base map layers
- **División político-administrativa** (orden: 1) - Political boundaries
- **Proyecto Oleoducto Bicentenario** (orden: 5) - Pipeline project layers  
- **Gobernanza** (orden: 6) - Governance layers
- **Restauración** (orden: 7) - Restoration layers
- **GEF Páramos** (orden: 8) - Páramos project layers

### 2. Fixed GeoServer Workspace Configuration
**Before (Error):**
```
https://geoservicios.humboldt.org.co/geoserver/Historicos/wms?...&LAYERS=Historicos%3Aparamo
```

**After (Working):**
```
https://geoservicios.humboldt.org.co/geoserver/gefparamos/wms?...&LAYERS=gefparamos%3Aparamo
```

**Workspace Corrections:**
- `paramo` layer: `Historicos` → `gefparamos`
- `municipio` layer: `Historicos` → `gefparamos`

### 3. Database Cleanup
Removed 8 non-existent layers that were causing WMS failures:
- Proyecto Oleoducto Bicentenario: Cobertura Bo
- Gobernanza: Posibles procesos de gobernanza
- Restauración: 6 layers (Integridad, Red Viveros, 4 escenario targets)

Removed 4 empty layer groups after cleanup.

## Final Database State

### Layer Groups for General Project (5 total):
1. **División político-administrativa**: 2 layers
   - Departamentos (`Capas_Base:dpto_politico`)
   - Municipios (`Capas_Base:mpio_politico`)

2. **Historicos**: 7 layers
   - AICAS, Bosque Seco Tropical, etc.

3. **Fondo de adaptación**: 4 layers
   - Humedales, Páramos limits, etc.

4. **Conservación de la Biodiversidad**: 10 layers
   - Biomas, Colapso layers, etc.

5. **GEF Páramos**: 2 layers ✅ **Fixed**
   - Paramos (`gefparamos:paramo`)
   - Municipios (`gefparamos:municipio`)

## Scripts Used

### 1. SQL Script: `add_missing_general_layer_groups.sql`
- Creates missing layer groups and layers
- Uses correct Django table names (`layer_groups`, `layers`, `projects`)
- Includes verification queries

### 2. Python Script: `add_missing_layers.py`
- Django ORM-based approach for adding layer groups
- Includes error handling and validation
- Provides detailed output of changes

## Verification Commands

### Check API Response:
```bash
curl -s http://localhost:8001/api/projects/1/layer_groups/ | jq -r '.[] | "\(.nombre): \(.layers | length) layers"'
```

### Verify GeoServer Layer Exists:
```bash
curl -s "https://geoservicios.humboldt.org.co/geoserver/gefparamos/wms?SERVICE=WMS&VERSION=1.3.0&REQUEST=GetCapabilities" | grep -A 2 -B 2 "paramo"
```

## Impact
- ✅ Frontend now displays correct number of layer groups (5 instead of 9)
- ✅ GeoServer WMS requests succeed for all layers
- ✅ Dynamic layer system works without hardcoded fallbacks
- ✅ Database contains only layers that exist in GeoServer

## Files Modified
- Database: `layer_groups`, `layers` tables
- Documentation: This file
- Scripts: `add_missing_general_layer_groups.sql`, `add_missing_layers.py`

## Branch Information
- Backend changes committed to: `manager_projects` branch
- All database modifications applied via Django ORM
- No direct SQL migrations required

## Testing
Frontend available at: http://localhost:8080
- Verify layer groups load correctly
- Confirm WMS requests succeed
- Check layer tree displays proper structure
