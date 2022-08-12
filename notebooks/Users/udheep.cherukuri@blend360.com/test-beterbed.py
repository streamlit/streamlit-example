# Databricks notebook source
# mount blob storage
spark.conf.set("fs.azure.account.key.beterbeddev.blob.core.windows.net",
"S3pCl04NELU1YmHouQDhHtkaTRrOLUZbc6zMGUIwWb/G7M4sackpkf8pyeNOU5YpD6k02YRa3rsz+ASthlHIbA==")

dfspark = spark.read.csv("wasbs://beterbedinput@beterbeddev.blob.core.windows.net/bb_test.csv", header="true")

# convert from sparkdf to azuredf 
df = dfspark.toPandas()

# COMMAND ----------



# COMMAND ----------



# COMMAND ----------



# COMMAND ----------



# COMMAND ----------

df.head()