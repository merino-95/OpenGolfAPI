# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "b365a40e-98aa-487e-ad4a-7d3684eca827",
# META       "default_lakehouse_name": "API_loadLakehouse",
# META       "default_lakehouse_workspace_id": "2cd7948e-ad77-4746-b164-804bea15f6fc",
# META       "known_lakehouses": [
# META         {
# META           "id": "b365a40e-98aa-487e-ad4a-7d3684eca827"
# META         }
# META       ]
# META     }
# META   }
# META }

# CELL ********************

import pandas as pd
from pyspark.sql import functions as F
from datetime import datetime, timezone

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

source_url = "https://raw.githubusercontent.com/opengolfapi/data/main/opengolfapi-us.csv"
source_system = "OpenGolfAPI GitHub CSV"
ingestion_datetime_utc = datetime.now(timezone.utc).isoformat()

bronze_table_name = "`00_bronze`.`bronze_opengolf_courses`"


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

# Eerst via pandas ophalen vanaf GitHub
pdf_raw = pd.read_csv(source_url)

print("Pandas shape:", pdf_raw.shape)

# Pandas naar Spark
df_raw = spark.createDataFrame(pdf_raw)

# Metadata toevoegen
df_bronze = (
    df_raw
    .withColumn("ingestion_datetime_utc", F.lit(ingestion_datetime_utc))
    .withColumn("source_system", F.lit(source_system))
    .withColumn("source_url", F.lit(source_url))
)

# Wegschrijven naar Lakehouse schema 00_bronze
(
    df_bronze.write
    .mode("overwrite")
    .format("delta")
    .option("overwriteSchema", "true")
    .saveAsTable(bronze_table_name)
)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
