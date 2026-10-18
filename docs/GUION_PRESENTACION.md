# Guion de presentación (máximo 20 minutos)

1. **Problema y alcance, 2 minutos.** El video motivó una hipótesis. Aquí estudiamos reapariciones de éxitos históricos en Hot 100, no todo el consumo musical. Debut y lanzamiento son campos distintos.
2. **Arquitectura y fuente, 2 minutos.** Mostrar README, fuente Kaggle v179 y diagrama. Grano: canción acreditada, fecha del ranking y chart. Dos lotes cronológicos.
3. **Bronze y silver, 4 minutos.** Abrir los outputs de la corrida exitosa. Mostrar archivos de origen, schemaLocation, checkpoint, conteos 15.700/31.400 y reejecución sin nuevas filas. Explicar NULL, deduplicación por llave y join muchos-a-uno.
4. **Gold y calidad, 3 minutos.** Mostrar classic_comebacks, semanas observadas y posición mínima. Mostrar error literal de rank=101 y song_id=NULL; ambas filas fueron rechazadas por Delta.
5. **Job y CI/CD, 3 minutos.** Mostrar cinco tareas dependientes, reintento bronze y disparador. Abrir el PR integrado, el Git folder y los targets dev/prod.
6. **Gobernanza y observabilidad, 3 minutos.** SHOW GRANTS del lector, tabla ficticia, máscara visible/oculta, tags. Mostrar DESCRIBE DETAIL, OPTIMIZE, historial y consulta de linaje.
7. **O9 y aprendizaje, 2 minutos.** Explicar uso del agente y las correcciones concretas, incluida la diferencia entre debut y lanzamiento. La decisión de reemplazos queda al profesor.

## Preguntas para practicar

- ¿Por qué checkpoint y schemaLocation tienen rutas distintas? Uno guarda progreso del stream y el otro el esquema inferido/evolución.
- ¿Qué pasa si ejecutás otra vez sin archivos nuevos? Auto Loader conserva el progreso; se comprueba en la tabla de auditoría, no se presupone.
- ¿Por qué no poner cero donde falta la posición previa? Cero no es una posición válida; NULL representa el dato ausente.
- ¿Por qué un join puede duplicar registros? Si el catálogo tiene múltiples filas para la misma llave. Se verifica su unicidad antes del join y el conteo después.
- ¿Qué hace cumplir las reglas? NOT NULL y CHECK de Delta, demostrado con inserciones rechazadas.
- ¿Por qué no concluir que se escucha más música vieja? El ranking no mide el universo de streams, y el filtro por debut no clasifica exhaustivamente lanzamientos originales.
- ¿Se probó otro usuario? No. La máscara se verificó modificando la tabla de mapeo del usuario de demostración; no equivale al opcional O2.
