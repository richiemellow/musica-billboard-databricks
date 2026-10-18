# Databricks notebook source
# MAGIC %md
# MAGIC # Bronze: ingesta incremental verificable
# MAGIC Auto Loader conserva su schemaLocation y checkpoint. Las reejecuciones no reinician ese estado.
# COMMAND ----------
# MAGIC %run ./00_config
# COMMAND ----------
target = f'{B}.chart_entries'
before = spark.table(target).count() if spark.catalog.tableExists(target) else 0
columns = ['chart_date_source','song_title','artist_credit','rank','last_week','peak_position','weeks_in_chart','image_url','song_id','chart_id','source_version','source_member','batch_id']
schema = T.StructType([T.StructField(c,T.StringType(),True) for c in columns])
incoming = (spark.readStream.format('cloudFiles')
    .option('cloudFiles.format','csv')
    .option('cloudFiles.schemaLocation',ROOT+'/state/schema')
    .option('cloudFiles.schemaEvolutionMode','rescue')
    .option('rescuedDataColumn','_rescued_data')
    .option('header','true').option('escape','"').option('encoding','UTF-8')
    .schema(schema).load(ROOT+'/charts')
    .withColumn('source_file',F.col('_metadata.file_path'))
    .withColumn('ingested_at',F.current_timestamp()))
query = (incoming.writeStream.format('delta').outputMode('append')
    .option('checkpointLocation',ROOT+'/state/checkpoint')
    .trigger(availableNow=True).toTable(target))
query.awaitTermination()
after = spark.table(target).count()
spark.sql(f'''CREATE TABLE IF NOT EXISTS {A}.ingestion_runs (
 execution_id STRING, observed_at TIMESTAMP, rows_before BIGINT, rows_after BIGINT,
 rows_added BIGINT, schema_location STRING, checkpoint_location STRING) USING DELTA''')
spark.sql(f"""INSERT INTO {A}.ingestion_runs VALUES
 ('{EXECUTION_ID}',current_timestamp(),{before},{after},{after-before},'{ROOT}/state/schema','{ROOT}/state/checkpoint')""")
print(json.dumps({'before':before,'after':after,'added':after-before}))
display(spark.sql(f'SELECT batch_id, count(*) rows, count(DISTINCT source_file) files FROM {target} GROUP BY batch_id ORDER BY batch_id'))
display(spark.sql(f'SELECT * FROM {A}.ingestion_runs ORDER BY observed_at'))
