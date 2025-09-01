-- Add Missing Layer Groups for General Project
-- This SQL script adds the missing layer groups and layers to the general project
-- Based on the HTML structure analysis, these groups are missing from the database

-- Get the general project ID (should be 1)
-- INSERT layer groups for general project (proyecto_id = 1)

-- 1. Add Capas Base layer group (Base maps - handled separately but needed for completeness)
INSERT INTO layer_groups (nombre, orden, fold_state, parent_group_id, proyecto_id, created_at, updated_at)
VALUES ('Capas Base', 0, 'close', NULL, 1, NOW(), NOW());

-- 2. Add División político-administrativa layer group
INSERT INTO layer_groups (nombre, orden, fold_state, parent_group_id, proyecto_id, created_at, updated_at)
VALUES ('División político-administrativa', 1, 'close', NULL, 1, NOW(), NOW());

-- 3. Add Proyecto Oleoducto Bicentenario layer group
INSERT INTO layer_groups (nombre, orden, fold_state, parent_group_id, proyecto_id, created_at, updated_at)
VALUES ('Proyecto Oleoducto Bicentenario', 5, 'close', NULL, 1, NOW(), NOW());

-- 4. Add Gobernanza layer group
INSERT INTO layer_groups (nombre, orden, fold_state, parent_group_id, proyecto_id, created_at, updated_at)
VALUES ('Gobernanza', 6, 'close', NULL, 1, NOW(), NOW());

-- 5. Add Restauración layer group
INSERT INTO layer_groups (nombre, orden, fold_state, parent_group_id, proyecto_id, created_at, updated_at)
VALUES ('Restauración', 7, 'close', NULL, 1, NOW(), NOW());

-- 6. Add GEF Páramos layer group
INSERT INTO layer_groups (nombre, orden, fold_state, parent_group_id, proyecto_id, created_at, updated_at)
VALUES ('GEF Páramos', 8, 'close', NULL, 1, NOW(), NOW());

-- Now add the layers for each group
-- Get the layer group IDs for inserting layers

-- Add División político-administrativa layers
INSERT INTO layers (nombre_geoserver, nombre_display, store_geoserver, estado_inicial, metadata_id, orden, grupo_id, created_at, updated_at)
SELECT 'dpto_politico', 'Departamentos', 'Capas_Base', false, NULL, 1, lg.id, NOW(), NOW()
FROM layer_groups lg 
WHERE lg.nombre = 'División político-administrativa' AND lg.proyecto_id = 1;

INSERT INTO layers (nombre_geoserver, nombre_display, store_geoserver, estado_inicial, metadata_id, orden, grupo_id, created_at, updated_at)
SELECT 'mpio_politico', 'Municipios', 'Capas_Base', false, NULL, 2, lg.id, NOW(), NOW()
FROM layer_groups lg 
WHERE lg.nombre = 'División político-administrativa' AND lg.proyecto_id = 1;

-- Add Proyecto Oleoducto Bicentenario layer
INSERT INTO layers (nombre_geoserver, nombre_display, store_geoserver, estado_inicial, metadata_id, orden, grupo_id, created_at, updated_at)
SELECT 'coberturas_bo_2009_2010', 'Cobertura Bo', 'Historicos', false, '008150a7-4ee9-488a-9ac0-354d678b4b8e', 1, lg.id, NOW(), NOW()
FROM layer_groups lg 
WHERE lg.nombre = 'Proyecto Oleoducto Bicentenario' AND lg.proyecto_id = 1;

-- Add Gobernanza layer
INSERT INTO layers (nombre_geoserver, nombre_display, store_geoserver, estado_inicial, metadata_id, orden, grupo_id, created_at, updated_at)
SELECT 'procesos_gobernanza', 'Posibles procesos de gobernanza', 'Historicos', false, 'a6fcfe1b-11e8-4383-a38e-a7f0035dece5', 1, lg.id, NOW(), NOW()
FROM layer_groups lg 
WHERE lg.nombre = 'Gobernanza' AND lg.proyecto_id = 1;

-- Add Restauración layers
INSERT INTO layers (nombre_geoserver, nombre_display, store_geoserver, estado_inicial, metadata_id, orden, grupo_id, created_at, updated_at)
SELECT 'integr_total4326', 'Integridad', 'Historicos', false, '55d29ef5-e419-489f-a450-3299e4bcc4d4', 1, lg.id, NOW(), NOW()
FROM layer_groups lg 
WHERE lg.nombre = 'Restauración' AND lg.proyecto_id = 1;

INSERT INTO layers (nombre_geoserver, nombre_display, store_geoserver, estado_inicial, metadata_id, orden, grupo_id, created_at, updated_at)
SELECT 'red_viveros', 'Red Viveros', 'Historicos', false, NULL, 2, lg.id, NOW(), NOW()
FROM layer_groups lg 
WHERE lg.nombre = 'Restauración' AND lg.proyecto_id = 1;

INSERT INTO layers (nombre_geoserver, nombre_display, store_geoserver, estado_inicial, metadata_id, orden, grupo_id, created_at, updated_at)
SELECT 'scen_mincost_target1', 'Escenario mínimo costo target 1', 'Historicos', false, '1d6b06b6-8a57-4c87-97ef-e156cb40dc46', 3, lg.id, NOW(), NOW()
FROM layer_groups lg 
WHERE lg.nombre = 'Restauración' AND lg.proyecto_id = 1;

INSERT INTO layers (nombre_geoserver, nombre_display, store_geoserver, estado_inicial, metadata_id, orden, grupo_id, created_at, updated_at)
SELECT 'scen_mincost_target2', 'Escenario mínimo costo target 2', 'Historicos', false, '1d6b06b6-8a57-4c87-97ef-e156cb40dc46', 4, lg.id, NOW(), NOW()
FROM layer_groups lg 
WHERE lg.nombre = 'Restauración' AND lg.proyecto_id = 1;

INSERT INTO layers (nombre_geoserver, nombre_display, store_geoserver, estado_inicial, metadata_id, orden, grupo_id, created_at, updated_at)
SELECT 'scen_mincost_target3', 'Escenario mínimo costo target 3', 'Historicos', false, '1d6b06b6-8a57-4c87-97ef-e156cb40dc46', 5, lg.id, NOW(), NOW()
FROM layer_groups lg 
WHERE lg.nombre = 'Restauración' AND lg.proyecto_id = 1;

INSERT INTO layers (nombre_geoserver, nombre_display, store_geoserver, estado_inicial, metadata_id, orden, grupo_id, created_at, updated_at)
SELECT 'scen_mincost_target4', 'Escenario mínimo costo target 4', 'Historicos', false, '1d6b06b6-8a57-4c87-97ef-e156cb40dc46', 6, lg.id, NOW(), NOW()
FROM layer_groups lg 
WHERE lg.nombre = 'Restauración' AND lg.proyecto_id = 1;

-- Add GEF Páramos layers
INSERT INTO layers (nombre_geoserver, nombre_display, store_geoserver, estado_inicial, metadata_id, orden, grupo_id, created_at, updated_at)
SELECT 'paramo', 'Paramos', 'Historicos', false, NULL, 1, lg.id, NOW(), NOW()
FROM layer_groups lg 
WHERE lg.nombre = 'GEF Páramos' AND lg.proyecto_id = 1;

INSERT INTO layers (nombre_geoserver, nombre_display, store_geoserver, estado_inicial, metadata_id, orden, grupo_id, created_at, updated_at)
SELECT 'municipio', 'Municipios', 'Historicos', false, NULL, 2, lg.id, NOW(), NOW()
FROM layer_groups lg 
WHERE lg.nombre = 'GEF Páramos' AND lg.proyecto_id = 1;

-- Verify the changes
SELECT 
    p.nombre as proyecto,
    lg.nombre as grupo,
    lg.orden as grupo_orden,
    COUNT(l.id) as num_layers
FROM projects p
LEFT JOIN layer_groups lg ON lg.proyecto_id = p.id
LEFT JOIN layers l ON l.grupo_id = lg.id
WHERE p.nombre_corto = 'general'
GROUP BY p.nombre, lg.nombre, lg.orden
ORDER BY lg.orden;

-- Show all layers for general project
SELECT 
    lg.nombre as grupo,
    l.nombre_display as layer_name,
    l.nombre_geoserver as geoserver_name,
    l.store_geoserver as store,
    l.orden as layer_orden
FROM layer_groups lg
JOIN layers l ON l.grupo_id = lg.id
WHERE lg.proyecto_id = 1
ORDER BY lg.orden, l.orden;
