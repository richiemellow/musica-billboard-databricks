# Decisiones y límites del laboratorio

- Se eligió Hot 100 por su serie histórica semanal. Billboard 200 contiene álbumes y se excluyó.
- Se conserva toda la población del Hot 100 en 2020-2025 para tener un denominador reproducible, aunque no represente toda la escucha.
- Las fechas de debut se usan para una exploración provisional de clásicos. No se inventaron años originales faltantes.
- La ingesta usa rutas persistentes y archivos inmutables. `schemaLocation` y `checkpointLocation` no se eliminan al volver a ejecutar.
- La limpieza usa `try_cast`; registros con campos obligatorios inválidos van a cuarentena. No se imputa una posición cero.
- El catálogo debe tener llave única; se comprueban filas antes y después del join.
- Silver se reconstruye desde bronze completo por su tamaño pequeño. El costo es aceptable para 31.400 filas; en volúmenes grandes se evaluaría MERGE incremental.
- Liquid clustering usa fecha y canción para consultas por períodos e identidad. Se verifica mediante DESCRIBE DETAIL e HISTORY; no se afirma una mejora de rendimiento sin medirla.
- El grupo lector recibe permisos sobre objetos concretos y no se le agregaron miembros. SHOW GRANTS prueba la configuración, pero no es una sesión de un segundo usuario.
- El correo de gobernanza es ficticio. La máscara es real y depende de una tabla de mapeo. Los tags explicitan la naturaleza de la demostración.
- El bundle contiene dev y prod. El laboratorio principal se ejecuta en prod; validar dev no equivale a desplegar ni ejecutar dev.
- Se utilizan timestamps reales. Las capturas y resultados corresponden a ejecuciones efectivas, incluidas correcciones y reparaciones.
- Los cinco componentes se conservan. O9 es evidencia adicional y cualquier reemplazo lo decide el profesor.
