# Databricks notebook source
# MAGIC %md
# MAGIC ## Transforming Bronze Tables to Silver Layer

# COMMAND ----------

# MAGIC %md
# MAGIC This notebook processes data from the **Bronze layer**, applies transformations, and saves the cleaned data to the **Silver layer**.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Transformations:
# MAGIC - **Date Formatting**: Converts date/time columns to a standard **"YYYY-MM-DD"** format.
# MAGIC - **Delta Format Storage**: Saves data in **Delta Lake format** with **overwrite mode** to keep Silver tables updated.

# COMMAND ----------

# Get table names from the Bronze layer
table_names = [file.name.rstrip('/') for file in dbutils.fs.ls('mnt/bronze/SalesLT/')]
print("Tables found in Bronze:", table_names)

# COMMAND ----------

from pyspark.sql.functions import from_utc_timestamp, date_format
from pyspark.sql.types import TimestampType

# COMMAND ----------

# Process each table from Bronze to Silver
for table in table_names:
    input_path = f'/mnt/bronze/SalesLT/{table}/{table}.parquet'

    # Read Parquet file
    try:
        df = spark.read.format('parquet').load(input_path)
    except Exception as e:
        print(f"Skipping {table} due to error: {e}")
        continue  

    # Format date columns
    for col in df.columns:
        if "Date" in col or "date" in col:
            df = df.withColumn(col, date_format(from_utc_timestamp(df[col].cast(TimestampType()), "UTC"), "yyyy-MM-dd"))

    # Write transformed data to Silver layer in Delta format
    df.write.format('delta').mode("overwrite").save(f'/mnt/silver/SalesLT/{table}/')

    print(f"Processed: {table}")


# COMMAND ----------

# Example Table: SalesOrderHeader (Before and After Transformation)

example_table = "CustomerAddress"

if example_table in table_names:
    example_path = f'/mnt/bronze/SalesLT/{example_table}/{example_table}.parquet'

    # Read example table
    try:
        example_df = spark.read.format('parquet').load(example_path)
    except Exception as e:
        print(f"Skipping {example_table} due to error: {e}")
    else:
        print(f"Before Transformation - {example_table}")
        display(example_df)

        # Apply date formatting transformation
        for col in example_df.columns:
            if "Date" in col or "date" in col:
                example_df = example_df.withColumn(col, date_format(from_utc_timestamp(example_df[col].cast(TimestampType()), "UTC"), "yyyy-MM-dd"))

        print(f"After Transformation - {example_table}")
        display(example_df)
