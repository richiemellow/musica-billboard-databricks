# Databricks notebook source
# MAGIC %md
# MAGIC # Gold: vigencia observada, no cuota de escuchas
# MAGIC Pregunta: ¿qué canciones con debut registrado en los 80/90 reaparecen entre 2020 y 2025?
# MAGIC La fecha de debut no prueba el año de lanzamiento. Se muestran el año original y su estado de verificación.
# COMMAND ----------
# MAGIC %run ./00_config
# COMMAND ----------
spark.sql(f'''CREATE OR REPLACE VIEW {G}.classic_comebacks AS
 SELECT song_id, song_title, artist_credit, first_hot100_decade,
 first_hot100_date_source, original_release_year, release_year_status,
 count(DISTINCT chart_date) AS weeks_observed, min(rank) AS best_rank,
 min(chart_date) AS first_recent_date, max(chart_date) AS last_recent_date
 FROM {S}.chart_entries
 WHERE chart_date BETWEEN DATE '2020-01-01' AND DATE '2025-12-31'
 AND first_hot100_decade IN ('1980s','1990s')
 GROUP BY ALL''')
spark.sql(f'''CREATE OR REPLACE VIEW {G}.annual_presence AS
 WITH counts AS (
 SELECT year(chart_date) AS observation_year, first_hot100_decade,
 count(*) AS chart_entries, count(DISTINCT song_id) AS distinct_songs
 FROM {S}.chart_entries GROUP BY ALL)
 SELECT *,sum(chart_entries) OVER(PARTITION BY observation_year) AS all_chart_entries_year,
 chart_entries / sum(chart_entries) OVER(PARTITION BY observation_year) AS share_chart_entries
 FROM counts''')
display(spark.sql(f'SELECT * FROM {G}.classic_comebacks ORDER BY weeks_observed DESC,best_rank,song_title'))
display(spark.sql(f'SELECT * FROM {G}.annual_presence ORDER BY observation_year,first_hot100_decade'))
# COMMAND ----------
# MAGIC %md
# MAGIC ## Dos reglas de calidad que Delta hace cumplir
# MAGIC La tabla gold de posiciones válidas usa NOT NULL y CHECK. Las filas de prueba nunca se incorporan al análisis.
# COMMAND ----------
spark.sql(f'''CREATE TABLE IF NOT EXISTS {G}.validated_positions (
 song_id STRING NOT NULL, chart_date DATE NOT NULL, rank INT NOT NULL) USING DELTA''')
properties = {r.key:r.value for r in spark.sql(f'SHOW TBLPROPERTIES {G}.validated_positions').collect()}
if 'delta.constraints.valid_rank' not in properties:
    spark.sql(f'ALTER TABLE {G}.validated_positions ADD CONSTRAINT valid_rank CHECK (rank BETWEEN 1 AND 100)')
spark.sql(f'INSERT OVERWRITE {G}.validated_positions SELECT song_id,chart_date,rank FROM {S}.chart_entries')
spark.sql(f'CREATE TABLE IF NOT EXISTS {A}.quality_rejections (observed_at TIMESTAMP, test_name STRING, error_literal STRING) USING DELTA')
errors=[]
for name,values in [('rank_fuera_de_rango',"'prueba_sintetica',DATE '2025-01-01',101"),('song_id_nulo',"NULL,DATE '2025-01-01',1")]:
    try:
        spark.sql(f'INSERT INTO {G}.validated_positions VALUES ({values})').collect()
    except Exception as exc:
        error=str(exc)
        assert any(token in error.upper() for token in ['CONSTRAINT','NOT_NULL','NOT NULL']),error
        errors.append((name,error))
        print(name+'\n'+error)
    else:
        raise AssertionError(f'La regla no rechazó {name}')
spark.createDataFrame(errors,'test_name string, error_literal string').withColumn('observed_at',F.current_timestamp()).select('observed_at','test_name','error_literal').write.mode('append').saveAsTable(f'{A}.quality_rejections')
assert spark.table(f'{G}.validated_positions').count()==spark.table(f'{S}.chart_entries').count()
display(spark.table(f'{A}.quality_rejections').orderBy(F.col('observed_at').desc()))
