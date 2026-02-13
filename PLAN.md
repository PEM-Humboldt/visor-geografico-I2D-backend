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

## Cronograma y productos principales

| Producto / Actividad                                                    | Fecha tentativa de entrega | Comentario                                    |
| ----------------------------------------------------------------------- | -------------------------- | --------------------------------------------- |
| 📄 1. Plan de trabajo (cronograma, productos, fechas de entrega)        | **6 ago 2025**             | Dentro de los 5 días hábiles desde el inicio. |
| 🗃️ 2. Informe técnico – Base de datos (consultas, estructura, pruebas)  | **30 ago 2025**            | Bloque para primer pago.                      |
| 🔧 3. Informe técnico – Backend (código, lógica, dependencias)          | **30 sep 2025**            | Bloque para segundo pago.                     |
| 💻 4. Informe técnico – Frontend (interfaz, accesibilidad, pruebas)     | **15 oct 2025**            |                                               |
| 🧪 5. Informe del entorno de pruebas (pruebas antes de producción)      | **31 oct 2025**            |                                               |
| ✨ 6. Nueva funcional para el manejo personalizado de URLs              | **10 nov 2025**            |                                               |
| 📘 7. Documentación técnica completa y actualizada                      | **15 nov 2025**            |                                               |
| 📚 Actualización y nueva documentación del sistema                      | **20 nov 2025**            |                                               |
| 👥 Socialización de cambios con equipo                                  | **22 nov 2025**            | Debe ir acompañada de informe de soporte.     |
| 📆 Participación en reuniones / atención a observaciones                | Durante toda la ejecución  | Continuo, según agenda del supervisor.        |
| 📝 Correcciones y ajustes a entregables                                 | Según observaciones        | Antes del acta de liquidación final.          |

## Resumen de recomendaciones clave de UPGRADE_STRATEGY.md
- Modernizar el frontend usando frameworks como React, Vue, Angular o Svelte, y actualizar herramientas de build (Vite, Webpack 5+, Parcel 2+).
- Asegurar compatibilidad hacia atrás y planificar migraciones graduales.
- Priorizar funcionalidades avanzadas de mapas (3D, análisis en tiempo real, capas temporales) y herramientas de usuario.

## Dependencias del ambiente de pruebas (docker-compose)
- Incluye PostgreSQL (db), backend Django y volúmenes para archivos estáticos/media.
- Falta agregar y configurar GeoServer para servicios geoespaciales.

## Pendientes
- Falta el envío de la base de datos para el entorno de pruebas y desarrollo.
- Para el setup y creación del visor personalizado, se debe crear una historia de usuario con los requerimientos exactos.

## Objetivo actual
Redactar y aprobar el plan de trabajo.


Formato de los cronogramas (Formato pendiente) PDF y Excel.
Volumen de GeoServer


https://i2d.humboldt.org.co/visor-I2D/?proyecto=ecoreservas#
https://i2d.humboldt.org.co/visor-I2D/
