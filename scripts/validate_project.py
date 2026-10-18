"""Validaciones locales reproducibles, sin credenciales ni conexión a Databricks."""
from pathlib import Path
import ast, csv, hashlib, io, json, zipfile
root=Path(__file__).resolve().parents[1]
for notebook in (root/'notebooks').glob('*.py'):
    ast.parse(notebook.read_text(),filename=str(notebook))
with zipfile.ZipFile(root/'data/dataset_musica_billboard.zip') as z:
    prefix='musica_billboard/'
    manifest=json.loads(z.read(prefix+'fuentes_y_validacion.json'))
    for name,digest in manifest['files_sha256'].items():
        assert hashlib.sha256(z.read(prefix+name)).hexdigest()==digest,name
    def rows(name):
        return list(csv.DictReader(io.StringIO(z.read(prefix+name).decode('utf-8-sig'))))
    catalog=rows('catalogo_canciones.csv')
    ids={r['song_id'] for r in catalog}
    assert len(ids)==len(catalog)==32694
    facts=rows('lote_01.csv')+rows('lote_02.csv')
    assert len(facts)==31400
    assert len({(r['chart_id'],r['chart_date_source'],r['song_id']) for r in facts})==31400
    assert all(r['song_id'] in ids and 1<=int(r['rank'])<=100 for r in facts)
    for batch,low,high in [('lote_01','2020-01-01','2022-12-31'),('lote_02','2023-01-01','2025-12-31')]:
        part=[r for r in facts if r['batch_id']==batch]
        assert len(part)==15700
        assert all(low<=r['chart_date_source']<=high for r in part)
print('PASS: sintaxis notebooks, huellas de origen, 31.400 hechos únicos, catálogo y fechas de lotes.')
