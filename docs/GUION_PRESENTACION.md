# Guion de defensa con O9 como reemplazo de C5

Ruta evaluada: V1/V2, C1, C2, C3, C4 y O9. Objetivo: 18 minutos incluidos cambios de pestaña.

1. **Problema, fuentes y arquitectura, 2 minutos.** Compartir enlace público al repositorio. Mostrar diagrama del README. Separar pipeline original y ampliación local.
2. **V1/V2, 4 minutos.** Mostrar outputs de ingesta, conteos por lote, source_file, checkpoint y schemaLocation. Explicar tipos, NULL, llave, deduplicación y join con métricas antes/después.
3. **C1, 2 minutos.** Mostrar Gold y errores literales de las dos filas rechazadas por Delta.
4. **C2, 2 minutos.** Mostrar cinco tareas, dependencias, reintento Bronze, trigger y corrida completa. Las pruebas fueron manuales.
5. **C3, 2 minutos.** Mostrar SHOW GRANTS, access_map, máscara visible/oculta y tags del correo ficticio. La segunda identidad no se probó y no se reclama O2.
6. **C4, 2 minutos.** Mostrar Git folder conectado a GitHub, rama, PR #1 integrado en main y bundle dev/prod. Dev no se declara desplegado.
7. **O9 reemplaza C5, 2 minutos.** Mostrar bitácora: petición, trabajo del agente, fallo de CHECK, corrección y resultado. Explicar responsabilidad del estudiante.
8. **Resultados y aprendizajes, 2 minutos.** Resumir resultados con límites. Para el examen: progreso incremental, calidad aplicada por Delta, privilegios acumulativos y DAG. Linaje/clustering quedan en respaldo.

## Preguntas técnicas para practicar

- Checkpoint conserva el progreso del stream; schemaLocation conserva información del esquema. No se borran para repetir la prueba.
- Sin archivos nuevos, Auto Loader agrega cero filas; la auditoría lo demuestra. Silver y las auditorías pueden volver a escribirse.
- NULL representa posición previa ausente; cero no es una posición válida.
- Un catálogo con llave duplicada multiplica filas en el join. Se valida unicidad y cardinalidad.
- NOT NULL y CHECK los hace cumplir Delta. Una aserción de Python solo protege esa ejecución.
- El trigger está configurado; los runs mostrados se iniciaron manualmente. Reintento no equivale a reparación manual.
- SHOW GRANTS prueba configuración; el dueño no demuestra permisos efectivos de otro usuario.
- El Git folder versiona el código. El bundle declara el Job. Actions valida archivos y no despliega a Databricks.
- O9 sustituye C5 por elección del estudiante, no sustituye la defensa ni suma puntos extra.
