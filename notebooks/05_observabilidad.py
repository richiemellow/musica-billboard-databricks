# Databricks notebook source
# MAGIC %md
# MAGIC # Observabilidad y optimización
# MAGIC Liquid clustering usa fecha y canción. Se conserva el resultado real de OPTIMIZE y el historial Delta.
# MAGIC Las tablas del sistema pueden tener retraso: cero filas no significa ausencia de actividad.
# COMMAND ----------
# MAGIC %run ./00_config
# COMMAND ----------
display(spark.sql(f'OPTIMIZE {S}.chart_entries'))
display(spark.sql(f'DESCRIBE DETAIL {S}.chart_entries'))
display(spark.sql(f'DESCRIBE HISTORY {S}.chart_entries LIMIT 10'))
display(spark.sql(f'SELECT * FROM {A}.ingestion_runs ORDER BY observed_at'))
# COMMAND ----------
lineage = spark.sql(f"""SELECT event_time,entity_type,entity_id,source_table_full_name,target_table_full_name
 FROM system.access.table_lineage
 WHERE source_table_catalog='{CAT}' OR target_table_catalog='{CAT}'
 ORDER BY event_time DESC LIMIT 50""")
display(lineage)
print('Registros de linaje disponibles:',lineage.count())
