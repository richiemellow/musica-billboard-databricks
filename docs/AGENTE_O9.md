# Bitácora del agente externo (O9 reemplaza C5)

El estudiante pidió investigar fuentes musicales, preparar el dataset y ejecutar el laboratorio completo con su autorización. El estudiante eligió O9 como reemplazo de C5. Se conservan V1/V2 y C1–C4 como requisitos evaluados. La observabilidad y optimización ya implementadas quedan como respaldo adicional.

## Trabajo realizado con el agente

- Investigación de Kaggle, Kworb y MusicBrainz. Selección de la versión 179 de Billboard y conservación de procedencia y licencia.
- Preparación de CSV reales, identificadores, diccionario y controles locales.
- Autenticación oficial de Databricks CLI y uso del CLI para cargar archivos, desplegar notebooks y consultar ejecuciones.
- Creación del pipeline bronze, silver, gold, gobernanza y observabilidad con un bundle que tiene targets dev y prod.
- Preparación del repositorio GitHub, rama de trabajo, validación automática y pull request.

## Correcciones y decisiones

1. El archivo disponible fue M4-proyecto-final.pdf, distinto del nombre mencionado inicialmente. Se trabajó sobre el proyecto final del módulo 4.
2. La licencia declarada por Kaggle es CC BY-NC-SA 4.0, no CC BY-NC 4.0.
3. Primera aparición en Billboard no significa lanzamiento original. Se conservó un campo distinto y se dejaron los años no verificados como NULL.
4. Crear el catálogo mediante CLI requería un almacenamiento explícito. Se creó mediante la interfaz oficial con Default Storage.
5. El primer intento de carga necesitó crear antes las carpetas charts y reference del volume.
6. La primera implementación de CHECK dentro de CREATE TABLE falló. Se corrigió agregando la restricción con ALTER TABLE ADD CONSTRAINT y comprobando su existencia para permitir reejecuciones.
7. Un grupo local de workspace no sirve como grupo lector de Unity Catalog. Se creó un grupo de cuenta específico, vacío, con autorización explícita del estudiante.
8. Los datos musicales no tienen correos privados. Se creó una tabla separada con un correo ficticio example.invalid para la demostración de máscara y etiquetas; no participa del análisis musical.

## Participación y límites

El estudiante eligió el dominio y autorizó el trabajo. El agente preparó y ejecutó el código. La presentación y defensa requieren que el estudiante entienda la arquitectura, las decisiones y las limitaciones. No se fabricaron resultados, fechas de ejecución ni pruebas con una segunda identidad. El historial de errores y correcciones se conserva.

## Demostración en la defensa

1. Solicitud: preparar los datos musicales y ejecutar el laboratorio completo con Databricks CLI.
2. Trabajo: notebooks, bundle, carga incremental, pruebas y pull request. Mostrar el PR #1 integrado y una corrida exitosa.
3. Corrección concreta: la definición inicial de CHECK falló. El agente la cambió a ALTER TABLE ADD CONSTRAINT y comprobó su existencia para permitir reejecuciones. Mostrar notebook 03 y los errores literales de rank=101 y song_id=NULL.
4. Resultado: Delta rechazó ambas filas inválidas; el Job terminó correctamente tras reparar Gold.
5. Responsabilidad: el estudiante eligió el dominio y revisa y explica las decisiones. El agente escribió y ejecutó el código; no se atribuye al estudiante una edición manual no documentada.

O9 ocupa el quinto espacio de evaluación (9% dentro del proyecto). No suma un sexto componente ni reemplaza Bronze/Silver, README o defensa.
