# Databricks notebook source
# MAGIC %md
# MAGIC # Silver: tipos, nulos, deduplicación y catálogo
# MAGIC Los guiones de posiciones previas se convierten a NULL, nunca a cero. Un año original desconocido permanece NULL.
# MAGIC Se conserva el crédito del artista para no mezclar covers. La primera fecha histórica es un indicador provisional.
# COMMAND ----------
# MAGIC %run ./00_config
# COMMAND ----------
raw = spark.table(f'{B}.chart_entries')
typed = (raw.withColumn('chart_date',F.expr('try_cast(chart_date_source as date)'))
    .withColumn('rank',F.expr('try_cast(rank as int)'))
    .withColumn('last_week',F.expr('try_cast(last_week as int)'))
    .withColumn('peak_position',F.expr('try_cast(peak_position as int)'))
    .withColumn('weeks_in_chart',F.expr('try_cast(weeks_in_chart as int)'))
    .withColumn('song_title',F.trim('song_title')).withColumn('artist_credit',F.trim('artist_credit')))
valid = (F.col('chart_date').isNotNull() & F.col('rank').between(1,100)
    & F.col('song_id').isNotNull() & (F.length('song_id')==64)
    & F.col('song_title').isNotNull() & (F.length('song_title')>0))
quarantine = typed.filter(~F.coalesce(valid,F.lit(False)))
quarantine.write.mode('overwrite').format('delta').saveAsTable(f'{S}.quarantine')
accepted = typed.filter(valid)
keys = ['chart_id','chart_date','song_id']
window = Window.partitionBy(*keys).orderBy(F.col('ingested_at').desc(),F.col('source_file').asc())
dedup = accepted.withColumn('_rn',F.row_number().over(window)).filter('_rn=1').drop('_rn')
catalog = (spark.read.option('header','true').option('escape','"').csv(ROOT+'/reference/catalogo_canciones.csv')
    .withColumn('first_hot100_date_source',F.expr('try_cast(first_hot100_date_source as date)'))
    .withColumn('original_release_year',F.expr('try_cast(original_release_year as int)')))
assert catalog.count()==catalog.select('song_id').distinct().count(), 'Catálogo con llaves duplicadas'
catalog.write.mode('overwrite').format('delta').saveAsTable(f'{S}.songs')
metadata = catalog.select('song_id','first_hot100_date_source','first_hot100_decade','original_release_year','release_year_source_url','release_year_status')
enriched = dedup.join(metadata,'song_id','left')
assert enriched.count()==dedup.count(), 'El join expandió filas'
unmatched = enriched.filter('first_hot100_date_source IS NULL').count()
assert unmatched==0, 'Hay canciones sin catálogo'
enriched.createOrReplaceTempView('prepared_chart_entries')
spark.sql(f'''CREATE TABLE IF NOT EXISTS {S}.chart_entries USING DELTA
 CLUSTER BY (chart_date, song_id) AS SELECT * FROM prepared_chart_entries WHERE false''')
spark.sql(f'INSERT OVERWRITE {S}.chart_entries SELECT * FROM prepared_chart_entries')
metrics = {
 'bronze_rows':raw.count(),'quarantine_rows':quarantine.count(),
 'duplicates_removed':accepted.count()-dedup.count(),'silver_rows':enriched.count(),
 'missing_last_week_before':raw.filter("last_week IS NULL OR last_week IN ('','-')").count(),
 'null_last_week_after':enriched.filter('last_week IS NULL').count(),
 'unknown_original_release_year':enriched.filter('original_release_year IS NULL').count(),
 'unmatched_catalog':unmatched}
spark.sql(f'CREATE TABLE IF NOT EXISTS {A}.quality_metrics (execution_id STRING, observed_at TIMESTAMP, metric STRING, value BIGINT) USING DELTA')
for metric,value in metrics.items():
    spark.sql(f"INSERT INTO {A}.quality_metrics VALUES ('{EXECUTION_ID}',current_timestamp(),'{metric}',{value})")
display(spark.sql(f"SELECT metric,value FROM {A}.quality_metrics WHERE execution_id='{EXECUTION_ID}' ORDER BY metric"))
display(enriched.select('song_title','artist_credit','chart_date','rank','last_week','first_hot100_decade','original_release_year').limit(20))
