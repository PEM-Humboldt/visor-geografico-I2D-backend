# Plan de trabajo para Visor Geográfico I2D (Backend)

## Estrategia de ramas y gestión de issues
- Se crearon forks para actualizar los repositorios principales.
- Todo el trabajo se gestionará inicialmente en la rama `develop`.
- Cuando se disponga de un ambiente de pruebas, se creará la rama `uat`.
- Después de la aprobación de los cambios en `uat`, estos se subirán a `master`.
- Este flujo de trabajo aplica tanto para backend como para frontend.
- Se utilizarán las opciones de Issues de GitHub para el control y seguimiento de tareas y bugs, permitiendo una mejor gestión del proyecto.

## Notas
- Los entregables y actividades están basados en la lista proporcionada.
- El paso 6 (setup/creación del visor) ha sido añadido y los pasos siguientes movidos en consecuencia.
- La fecha límite de finalización es el 10 de diciembre de 2025.
- El plan aplica para ambos repositorios.
- El setup del visor implica creación de URL, configuración, branding (nombre, logo) y estructura para esta funcionalidad.

## Resumen de recomendaciones clave de UPGRADE_STRATEGY.md
- Modernizar el frontend usando frameworks como React, Vue, Angular o Svelte, y actualizar herramientas de build (Vite, Webpack 5+, Parcel 2+).
- Asegurar compatibilidad hacia atrás y planificar migraciones graduales.
- Priorizar funcionalidades avanzadas de mapas (3D, análisis en tiempo real, capas temporales) y herramientas de usuario.

## Dependencias del ambiente de pruebas (docker-compose)
- Incluye PostgreSQL (db), backend Django y volúmenes para archivos estáticos/media.
- Falta agregar y configurar GeoServer para servicios geoespaciales.

## Preguntas
- ¿Se definirán las variables del proyecto únicamente en inglés? (pendiente de decisión)

## Pendientes
- Falta el envío de la base de datos para el entorno de pruebas y desarrollo.
- Para el setup y creación del visor personalizado, se debe crear una historia de usuario con los requerimientos exactos.

## Lista de tareas
- [ ] 📄 Plan de trabajo (cronograma, productos, fechas)
- [ ] 🗃️ Informe técnico – Base de datos (cambios, optimización, pruebas)
- [ ] 🔧 Informe técnico – Backend (código, dependencias, lógica de negocio)
- [ ] 💻 Informe técnico – Frontend (UI, accesibilidad, funcionalidad, pruebas)
- [ ] 🧪 Informe de entorno de pruebas (configuración, validaciones, recomendaciones para producción)
- [ ] ⚙️ Setup y creación del visor (estructura, URL, configuración, branding)
- [ ] 📘 Documentación técnica final (diagramas, manuales, configuración, mantenimiento)
- [ ] 👥 Socialización de cambios con el equipo definido por el supervisor
- [ ] 🔄 Actualización de documentación existente (diagramas, instrucciones, etc.)
- [ ] 📚 Nueva documentación generada por los cambios realizados
- [ ] 📆 Asistencia a reuniones y atención a requerimientos del supervisor
- [ ] 📝 Atención a observaciones y correcciones de productos entregados
- [ ] ⚙️ Otras actividades necesarias para cumplir el objeto del contrato

## Objetivo actual
Redactar y aprobar el plan de trabajo.
