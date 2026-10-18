# Databricks notebook source
# MAGIC %md
# MAGIC # Gobernanza: perfiles, máscara y datos ficticios
# MAGIC Esta demostración usa correos `example.invalid` ficticios de revisores. No son personas ni contactos reales.
# MAGIC Las políticas se aplican en Unity Catalog. La tabla de mapeo controla el acceso.
# COMMAND ----------
# MAGIC %run ./00_config
# COMMAND ----------
spark.sql(f'''CREATE TABLE IF NOT EXISTS {GOV}.access_map (
 principal STRING, profile STRING, can_view_email BOOLEAN) USING DELTA''')
spark.sql(f'''MERGE INTO {GOV}.access_map t
 USING (SELECT current_user() principal,'owner_demo' profile,true can_view_email) s
 ON t.principal=s.principal WHEN NOT MATCHED THEN INSERT *''')
spark.sql(f'''CREATE TABLE IF NOT EXISTS {GOV}.reviewers_demo (
 reviewer_id STRING, reviewer_email STRING, is_synthetic BOOLEAN) USING DELTA''')
spark.sql(f'''MERGE INTO {GOV}.reviewers_demo t USING
 (SELECT 'REV001' reviewer_id, 'revision.musica@example.invalid' reviewer_email,true is_synthetic) s
 ON t.reviewer_id=s.reviewer_id WHEN NOT MATCHED THEN INSERT *''')
spark.sql(f'''CREATE OR REPLACE FUNCTION {GOV}.mask_reviewer_email(email STRING)
 RETURNS STRING RETURN CASE WHEN EXISTS (
 SELECT 1 FROM {GOV}.access_map WHERE principal=current_user() AND can_view_email)
 THEN email ELSE '[oculto]' END''')
spark.sql(f'ALTER TABLE {GOV}.reviewers_demo ALTER COLUMN reviewer_email SET MASK {GOV}.mask_reviewer_email')
spark.sql(f"ALTER TABLE {GOV}.reviewers_demo ALTER COLUMN reviewer_email SET TAGS ('classification'='sensitive_demo','synthetic'='true')")
display(spark.sql(f'SELECT * FROM {GOV}.reviewers_demo'))
# COMMAND ----------
# MAGIC %md
# MAGIC Se modifica solamente la fila del usuario de la demostración para comprobar ambos resultados de la máscara.
# MAGIC Esto no suplanta una segunda identidad; la verificación con otra sesión pertenece al opcional O2.
# COMMAND ----------
spark.sql(f'UPDATE {GOV}.access_map SET can_view_email=false WHERE principal=current_user()')
try:
    hidden=spark.table(f'{GOV}.reviewers_demo')
    display(hidden)
    hidden_value=hidden.first().reviewer_email
    assert hidden_value=='[oculto]'
finally:
    spark.sql(f'UPDATE {GOV}.access_map SET can_view_email=true WHERE principal=current_user()')
visible_value=spark.table(f'{GOV}.reviewers_demo').first().reviewer_email
assert visible_value=='revision.musica@example.invalid'
spark.sql(f'CREATE TABLE IF NOT EXISTS {A}.mask_validation (observed_at TIMESTAMP, scenario STRING, observed_value STRING, is_synthetic BOOLEAN) USING DELTA')
spark.createDataFrame([('mapping_false',hidden_value,True),('mapping_true',visible_value,True)],'scenario string, observed_value string, is_synthetic boolean').withColumn('observed_at',F.current_timestamp()).select('observed_at','scenario','observed_value','is_synthetic').write.mode('append').saveAsTable(f'{A}.mask_validation')
display(spark.sql(f'SELECT * FROM {GOV}.reviewers_demo'))
reader = 'musica_lectores_uc'
spark.sql(f'GRANT USE CATALOG ON CATALOG {CAT} TO `{reader}`')
for schema in [G,GOV]:
    spark.sql(f'GRANT USE SCHEMA ON SCHEMA {schema} TO `{reader}`')
for table in [f'{G}.classic_comebacks',f'{G}.annual_presence',f'{G}.validated_positions',f'{GOV}.reviewers_demo']:
    spark.sql(f'GRANT SELECT ON TABLE {table} TO `{reader}`')
display(spark.sql(f'SHOW GRANTS `{reader}` ON CATALOG {CAT}'))
display(spark.sql(f'SHOW GRANTS `{reader}` ON SCHEMA {G}'))
display(spark.sql(f'SHOW GRANTS `{reader}` ON TABLE {GOV}.reviewers_demo'))
display(spark.sql(f'SHOW GRANTS ON TABLE {G}.validated_positions'))
display(spark.sql(f"SELECT * FROM {CAT}.information_schema.column_tags WHERE schema_name='{PREFIX}governance'"))
