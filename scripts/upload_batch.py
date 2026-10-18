"""Sube un lote explícito. No reinicia checkpoints ni reemplaza archivos existentes."""
from pathlib import Path
import argparse, subprocess, tempfile, zipfile
p=argparse.ArgumentParser()
p.add_argument('--batch',choices=['1','2'],required=True)
p.add_argument('--catalog',default='musica_saenz')
p.add_argument('--schema-prefix',default='')
a=p.parse_args()
volume=f'dbfs:/Volumes/{a.catalog}/{a.schema_prefix}bronze/landing'
root=Path(__file__).resolve().parents[1]
def cli(*args): subprocess.run(['databricks',*args],check=True)
cli('fs','mkdir',volume+'/charts')
cli('fs','mkdir',volume+'/reference')
with tempfile.TemporaryDirectory() as td,zipfile.ZipFile(root/'data/dataset_musica_billboard.zip') as z:
    names=[f'lote_0{a.batch}.csv']
    if a.batch=='1': names.append('catalogo_canciones.csv')
    for name in names:
        target=Path(td)/name
        target.write_bytes(z.read('musica_billboard/'+name))
        folder='reference' if name.startswith('catalogo') else 'charts'
        cli('fs','cp',str(target),volume+'/'+folder+'/'+name)
