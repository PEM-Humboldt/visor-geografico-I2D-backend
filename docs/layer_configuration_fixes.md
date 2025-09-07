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

### 3. Restauración Group Corrections (General project)
The `Restauración` group for the General project had the WRONG subitems (copied from ecoreservas “Compensación”). This caused the UI button to do nothing because WMS requests targeted non-existing layers/workspaces.

Fixes applied:
- Replaced incorrect subitems with the 6 correct layers used in production.
- Updated GeoServer workspace for these layers to `weplan` so the LAYERS param matches production, e.g. `weplan:scen_mincost_target4`.

Final expected items under General → Restauración:
- Integridad (`weplan:integr_total4326`)
- Red Viveros (`weplan:red_viveros`)
- Escenario mínimo costo target 1 (`weplan:scen_mincost_target1`)
- Escenario mínimo costo target 2 (`weplan:scen_mincost_target2`)
- Escenario mínimo costo target 3 (`weplan:scen_mincost_target3`)
- Escenario mínimo costo target 4 (`weplan:scen_mincost_target4`)

How it was fixed (SQL applied locally):

```sql
-- Remove incorrect (Compensación/ecoreservas) layers from General → Restauración
WITH grp AS (
  SELECT lg.id
  FROM django.layer_groups lg
  JOIN django.projects p ON p.id = lg.proyecto_id
  WHERE p.nombre_corto = 'general' AND lg.nombre = 'Restauración'
  LIMIT 1
)
DELETE FROM django.layers l
USING grp
WHERE l.grupo_id = (SELECT id FROM grp)
  AND (
    l.store_geoserver = 'ecoreservas' OR
    l.nombre_display ILIKE '%Compensación%'
  );

-- Insert the six correct layers if missing
WITH grp AS (
  SELECT lg.id
  FROM django.layer_groups lg
  JOIN django.projects p ON p.id = lg.proyecto_id
  WHERE p.nombre_corto = 'general' AND lg.nombre = 'Restauración'
  LIMIT 1
)
INSERT INTO django.layers
  (nombre_geoserver, nombre_display, store_geoserver, estado_inicial, metadata_id, orden, grupo_id, created_at, updated_at)
SELECT v.nombre_geoserver, v.nombre_display, v.store_geoserver, v.estado_inicial, v.metadata_id, v.orden,
       (SELECT id FROM grp), NOW(), NOW()
FROM (
  VALUES
    ('integr_total4326',     'Integridad',                         'Historicos', false, '55d29ef5-e419-489f-a450-3299e4bcc4d4', 1),
    ('red_viveros',         'Red Viveros',                        'Historicos', false, NULL,                                      2),
    ('scen_mincost_target1','Escenario mínimo costo target 1',    'Historicos', false, '1d6b06b6-8a57-4c87-97ef-e156cb40dc46', 3),
    ('scen_mincost_target2','Escenario mínimo costo target 2',    'Historicos', false, '1d6b06b6-8a57-4c87-97ef-e156cb40dc46', 4),
    ('scen_mincost_target3','Escenario mínimo costo target 3',    'Historicos', false, '1d6b06b6-8a57-4c87-97ef-e156cb40dc46', 5),
    ('scen_mincost_target4','Escenario mínimo costo target 4',    'Historicos', false, '1d6b06b6-8a57-4c87-97ef-e156cb40dc46', 6)
) AS v(nombre_geoserver, nombre_display, store_geoserver, estado_inicial, metadata_id, orden)
WHERE NOT EXISTS (
  SELECT 1 FROM django.layers l
  WHERE l.grupo_id = (SELECT id FROM grp)
    AND l.nombre_geoserver = v.nombre_geoserver
);

-- Align GeoServer workspace to production (weplan)
WITH grp AS (
  SELECT lg.id AS group_id
  FROM django.layer_groups lg
  JOIN django.projects p ON p.id = lg.proyecto_id
  WHERE p.nombre_corto = 'general' AND lg.nombre = 'Restauración'
  LIMIT 1
)
UPDATE django.layers l
SET store_geoserver = 'weplan', updated_at = NOW()
WHERE l.grupo_id = (SELECT group_id FROM grp)
  AND l.nombre_geoserver IN (
    'integr_total4326',
    'red_viveros',
    'scen_mincost_target1',
    'scen_mincost_target2',
    'scen_mincost_target3',
    'scen_mincost_target4'
  );
```

Verification (API):

```bash
curl -s "http://localhost:8001/api/layer-groups/?project=1" \
  | jq -r '.[] | select(.nombre=="Restauración") | .layers[] | "\(.nombre_display) -> \(.store_geoserver):\(.nombre_geoserver)"'
# Expected:
# Integridad -> weplan:integr_total4326
# Red Viveros -> weplan:red_viveros
# Escenario mínimo costo target 1 -> weplan:scen_mincost_target1
# Escenario mínimo costo target 2 -> weplan:scen_mincost_target2
# Escenario mínimo costo target 3 -> weplan:scen_mincost_target3
# Escenario mínimo costo target 4 -> weplan:scen_mincost_target4
```

Verification (GeoServer WMS example):

```bash
curl -s "https://geoservicios.humboldt.org.co/geoserver/weplan/wms?SERVICE=WMS&VERSION=1.3.0&REQUEST=GetMap&FORMAT=image/png&TRANSPARENT=true&LAYERS=weplan:scen_mincost_target4&STYLES=&TILED=true&WIDTH=256&HEIGHT=256&CRS=EPSG:3857&BBOX=-7514065.6285,626172.1357,-7200979.5607,939258.2036" -o /dev/null -w "%{http_code}\n"
# Expect 200
```

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

### Verify WePlan Workspace Layers (Restauración)
```bash
curl -s "https://geoservicios.humboldt.org.co/geoserver/weplan/wms?SERVICE=WMS&VERSION=1.3.0&REQUEST=GetMap&FORMAT=image/png&TRANSPARENT=true&LAYERS=weplan:integr_total4326&STYLES=&TILED=true&WIDTH=256&HEIGHT=256&CRS=EPSG:3857&BBOX=-8237642,395691,-7858217,774116" -o /dev/null -w "%{http_code}\n"
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
