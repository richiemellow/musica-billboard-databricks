-- Demostración de lectura: V1/V2, C1, C3. C2 y C4 se muestran en sus pantallas.
-- O9 reemplaza C5. No se ejecutan inserciones ni cambios de permisos.
-- 1. Incrementalidad
SELECT observed_at, rows_before, rows_after, rows_added FROM musica_saenz.audit.ingestion_runs ORDER BY observed_at;
-- 2. Cada lote una vez y procedencia completa
SELECT batch_id, count(*) AS filas, count(DISTINCT source_file) AS archivos, count_if(source_file IS NULL) AS origen_nulo FROM musica_saenz.bronze.chart_entries GROUP BY batch_id ORDER BY batch_id;
-- 3. Métricas antes y después
SELECT metric, value FROM musica_saenz.audit.quality_metrics WHERE execution_id=(SELECT execution_id FROM musica_saenz.audit.quality_metrics ORDER BY observed_at DESC LIMIT 1) ORDER BY metric;
-- 4. Tipos y llave. Mostrar además Window y join en notebook 02.
DESCRIBE TABLE musica_saenz.silver.chart_entries;
SELECT chart_id,chart_date,song_id,count(*) AS filas FROM musica_saenz.silver.chart_entries GROUP BY chart_id,chart_date,song_id HAVING count(*)>1;
-- 5. Gold: pregunta original
SELECT * FROM musica_saenz.gold.classic_comebacks ORDER BY weeks_observed DESC,best_rank,song_title;
-- 6. Errores literales ya registrados
SELECT observed_at,test_name,error_literal FROM musica_saenz.audit.quality_rejections ORDER BY observed_at DESC LIMIT 6;
-- 7. Restricciones aplicadas por Delta
SHOW TBLPROPERTIES musica_saenz.gold.validated_positions;
SELECT column_name,is_nullable FROM musica_saenz.information_schema.columns WHERE table_schema='gold' AND table_name='validated_positions';
-- 8. Permisos del perfil lector
SHOW GRANTS `musica_lectores_uc` ON CATALOG musica_saenz;
SHOW GRANTS `musica_lectores_uc` ON SCHEMA musica_saenz.gold;
SHOW GRANTS `musica_lectores_uc` ON TABLE musica_saenz.gold.validated_positions;
SHOW GRANTS `musica_lectores_uc` ON TABLE musica_saenz.governance.reviewers_demo;
-- 9. Mapeo y máscara actual. Solo mostrar la fila de la identidad de demostración.
SELECT profile,can_view_email FROM musica_saenz.governance.access_map WHERE principal=current_user();
SELECT * FROM musica_saenz.governance.reviewers_demo;
-- 10. Dos estados históricos: misma identidad, no una sesión de segundo usuario
SELECT observed_at,scenario,observed_value,is_synthetic FROM musica_saenz.audit.mask_validation ORDER BY observed_at DESC LIMIT 6;
-- 11. Tags
SELECT schema_name,table_name,column_name,tag_name,tag_value FROM musica_saenz.information_schema.column_tags WHERE schema_name='governance';
-- Ampliación de cohortes y Luminate: archivos locales, fuera de Gold.
