# Evidencia externa de consumo: Luminate

Estos archivos ya existían en el material local de la defensa. Se incorporan como respaldo documental del README; no se ejecutan ni se cargan en el pipeline Databricks y no se unen a Billboard.

- `luminate_2022_p7.png`: página 7 del [informe oficial 2022](https://luminatedata.com/wp-content/uploads/2023/01/Luminate_US-YearEndReport_2022_FINAL_1.pdf#page=7). Panel inferior “U.S. Catalog vs. Current Consumption”: 69,8%/72,2% de catálogo y 269,5/270,9 millones de unidades equivalentes recientes para 2021/2022. Incluye definición y períodos al pie.
- `luminate_2023_p13.png`: extracto de página 13 del [informe oficial 2023](https://luminatedata.com/wp-content/uploads/2024/01/Luminate_Year-End_Report_2023.pdf#page=13). Panel “U.S. Catalog vs. Current Consumption”: 72,2%/72,6% y 270,9/300,4 millones para 2022/2023, con notas al pie.
- `luminate_catalog_series.csv`: transcripción existente; conserva URL, localizador, períodos y definición. Las filas con diferente `series_id` no se empalman. El README usa la serie `total_consumption_legacy`; las filas de 2024 se conservan para explicar su comparabilidad limitada, no como una actualización verificada en vivo.

Las imágenes se inspeccionaron visualmente y se copiaron sin modificar desde `defensa_musical/entrega/evidencias/luminate/` del proyecto local. El CSV se copió sin modificar de `ampliacion_musica/historico/`. Los PDF locales de ambos informes se cotejaron en las páginas citadas. La evidencia registra informes pasados; no representa una consulta de consumo actual.

Catálogo no equivale a los clásicos 80/90. Las notas de los informes 2022/2023 exigen antigüedad de al menos 18 meses y condiciones de Billboard 200/airplay. La serie del informe 2024 tiene otra base, períodos y notas metodológicas. No se corrige ni promedia la diferencia entre 72,6% y 72,7% para 2023. Las unidades equivalentes de álbum no son conteos de streams.

Derechos de las imágenes e informes: Luminate. Su inclusión como evidencia académica no los relicencia bajo la licencia del código del proyecto.
