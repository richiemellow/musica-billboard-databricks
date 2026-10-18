# Databricks notebook source
# MAGIC %md
# MAGIC # Configuración del proyecto de música
# MAGIC Los datos musicales son públicos. Las fechas de Billboard son fechas del ranking, no de lanzamiento.
# COMMAND ----------
import re, json, uuid
from pyspark.sql import functions as F, types as T, Window
dbutils.widgets.text('catalog', 'musica_saenz')
dbutils.widgets.text('schema_prefix', '')
CAT = dbutils.widgets.get('catalog')
PREFIX = dbutils.widgets.get('schema_prefix')
assert re.fullmatch(r'[a-z][a-z0-9_]*', CAT)
assert re.fullmatch(r'[a-z0-9_]*', PREFIX)
B = f'{CAT}.{PREFIX}bronze'
S = f'{CAT}.{PREFIX}silver'
G = f'{CAT}.{PREFIX}gold'
A = f'{CAT}.{PREFIX}audit'
GOV = f'{CAT}.{PREFIX}governance'
for schema in [B, S, G, A, GOV]:
    spark.sql(f'CREATE SCHEMA IF NOT EXISTS {schema}')
spark.sql(f'CREATE VOLUME IF NOT EXISTS {B}.landing')
ROOT = f'/Volumes/{CAT}/{PREFIX}bronze/landing'
EXECUTION_ID = str(uuid.uuid4())
print(json.dumps({'catalog':CAT,'schema_prefix':PREFIX,'volume':ROOT}))
