"""Comprueba la evidencia exportada de Databricks antes de publicar el cierre."""
from pathlib import Path
import json
root=Path(__file__).resolve().parents[1]/'evidence'
def rows(name):
    document=json.loads((root/(name+'.json')).read_text())
    assert document['status']=='SUCCEEDED',name
    return document['rows']
ingestion=rows('ingestion_runs')
assert [(int(r['rows_before']),int(r['rows_after']),int(r['rows_added'])) for r in ingestion][:3]==[(0,15700,15700),(15700,31400,15700),(31400,31400,0)]
assert all(int(r['rows_after'])==31400 and int(r['rows_added'])==0 for r in ingestion[2:])
batches=rows('batch_counts')
assert {r['batch_id']:int(r['rows']) for r in batches}=={'lote_01':15700,'lote_02':15700}
quality={r['metric']:int(r['value']) for r in rows('silver_quality')}
assert quality['silver_rows']==quality['bronze_rows']==31400
assert quality['quarantine_rows']==quality['unmatched_catalog']==0
assert quality['null_last_week_after']==quality['missing_last_week_before']
assert len(rows('classics'))==8
assert {r['scenario']:r['observed_value'] for r in rows('mask_validation')}=={'mapping_false':'[oculto]','mapping_true':'revision.musica@example.invalid'}
errors=rows('rejected_rows')
assert any(r['test_name']=='rank_fuera_de_rango' and 'CHECK' in r['error_literal_excerpt'] for r in errors)
assert any(r['test_name']=='song_id_nulo' and 'NOT NULL' in r['error_literal_excerpt'] for r in errors)
assert all(r['is_nullable']=='NO' for r in rows('not_null_columns'))
cluster=rows('clustering')[0]
assert set(json.loads(cluster['clusteringColumns']))=={'chart_date','song_id'}
assert any(r['operation']=='OPTIMIZE' for r in rows('table_history'))
assert rows('system_lineage'),'Debe haber linaje real del proyecto, no solo consulta vacía'
for name in ['reader_catalog_grants','reader_gold_grants','reader_table_grants','reader_demo_grants']:
    granted=rows(name)
    assert granted,name
    direct=[r for r in granted if r['Principal']=='musica_lectores_uc']
    assert direct,name
    assert all(r['ActionType'] in ['USE CATALOG','USE SCHEMA','SELECT'] for r in direct)
    inherited=[r for r in granted if r['Principal']!='musica_lectores_uc']
    assert all(r['Principal']=='account users' and r['ActionType']=='BROWSE' for r in inherited)
job=json.loads((root/'job_configuration.json').read_text())
assert job['trigger']['pause_status']=='UNPAUSED'
assert job['trigger']['file_arrival']['url']=='/Volumes/musica_saenz/bronze/landing/charts/'
tasks={t['task_key']:t for t in job['tasks']}
assert tasks['bronze']['max_retries']>=1
for child,parent in [('silver','bronze'),('gold','silver'),('governance','gold'),('observability','governance')]:
    assert tasks[child]['depends_on']==[{'task_key':parent}]
print('PASS: dos lotes, idempotencia, limpieza, calidad, máscara, mínimo privilegio, clustering y linaje.')
