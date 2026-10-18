"""Exporta evidencia de solo lectura y sin identidades personales a JSON revisable."""
from pathlib import Path
import json,subprocess,time,tempfile
root=Path(__file__).resolve().parents[1]
out=root/'evidence';out.mkdir(exist_ok=True)
warehouse='f1e105abb6caeaf0'
queries={
 'ingestion_runs':'SELECT observed_at,rows_before,rows_after,rows_added FROM musica_saenz.audit.ingestion_runs ORDER BY observed_at',
 'batch_counts':'SELECT batch_id,count(*) rows,count(DISTINCT source_file) source_files FROM musica_saenz.bronze.chart_entries GROUP BY batch_id ORDER BY batch_id',
 'silver_quality':'''SELECT metric,value FROM musica_saenz.audit.quality_metrics
 WHERE execution_id=(SELECT execution_id FROM musica_saenz.audit.quality_metrics ORDER BY observed_at DESC LIMIT 1) ORDER BY metric''',
 'classics':'SELECT * FROM musica_saenz.gold.classic_comebacks ORDER BY weeks_observed DESC,best_rank,song_title',
 'rejected_rows':'''SELECT observed_at,test_name,substring_index(error_literal,'JVM stacktrace:',1) error_literal_excerpt FROM musica_saenz.audit.quality_rejections ORDER BY observed_at''',
 'reader_catalog_grants':'SHOW GRANTS `musica_lectores_uc` ON CATALOG musica_saenz',
 'reader_gold_grants':'SHOW GRANTS `musica_lectores_uc` ON SCHEMA musica_saenz.gold',
 'reader_table_grants':'SHOW GRANTS `musica_lectores_uc` ON TABLE musica_saenz.gold.validated_positions',
 'reader_demo_grants':'SHOW GRANTS `musica_lectores_uc` ON TABLE musica_saenz.governance.reviewers_demo',
 'demo_tags':"SELECT schema_name,table_name,column_name,tag_name,tag_value FROM musica_saenz.information_schema.column_tags WHERE schema_name='governance'",
 'mask_validation':'SELECT * FROM musica_saenz.audit.mask_validation ORDER BY observed_at,scenario',
 'not_null_columns':"SELECT column_name,is_nullable FROM musica_saenz.information_schema.columns WHERE table_schema='gold' AND table_name='validated_positions' ORDER BY ordinal_position",
 'table_properties':'SHOW TBLPROPERTIES musica_saenz.gold.validated_positions',
 'clustering':'DESCRIBE DETAIL musica_saenz.silver.chart_entries',
 'table_history':'DESCRIBE HISTORY musica_saenz.silver.chart_entries LIMIT 8',
 'system_lineage':'''SELECT event_time,entity_type,source_table_full_name,target_table_full_name
 FROM system.access.table_lineage WHERE source_table_catalog='musica_saenz' OR target_table_catalog='musica_saenz'
 ORDER BY event_time DESC LIMIT 30'''
}
def api(*args):
    p=subprocess.run(['databricks','api',*args,'-o','json'],capture_output=True,text=True,check=True)
    return json.loads(p.stdout)
for name,sql in queries.items():
    with tempfile.NamedTemporaryFile(mode='w',suffix='.json') as f:
        json.dump({'warehouse_id':warehouse,'statement':sql,'wait_timeout':'10s','row_limit':100},f);f.flush()
        response=api('post','/api/2.0/sql/statements','--json','@'+f.name)
    sid=response['statement_id']
    while response['status']['state'] in ('PENDING','RUNNING'):
        time.sleep(2)
        response=api('get','/api/2.0/sql/statements/'+sid)
    if response['status']['state']!='SUCCEEDED':
        raise RuntimeError(json.dumps(response['status']))
    columns=[v['name'] for v in response['manifest']['schema']['columns']]
    rows=[dict(zip(columns,row)) for row in response.get('result',{}).get('data_array',[])]
    if name=='clustering':
        allow=['format','name','numFiles','sizeInBytes','clusteringColumns','partitionColumns']
        rows=[{k:v for k,v in r.items() if k in allow} for r in rows]
    if name=='table_history':
        allow=['version','timestamp','operation','operationParameters','operationMetrics']
        rows=[{k:v for k,v in r.items() if k in allow} for r in rows]
    payload={'statement_id':sid,'query':sql,'status':'SUCCEEDED','rows':rows}
    (out/(name+'.json')).write_text(json.dumps(payload,ensure_ascii=False,indent=2))
    print(name,len(rows),'rows',flush=True)
