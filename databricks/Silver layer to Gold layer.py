# Databricks notebook source
# MAGIC %md
# MAGIC ## Transforming Silver Layer to Gold Layer

# COMMAND ----------

# MAGIC %md
# MAGIC  This notebook processes data from the **Silver layer**, applies transformations, and saves the cleaned data to the **Gold layer**.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Transformations:
# MAGIC - **Column Name Standardization**: Converts camel case column names (e.g., `CustomerID`) to snake case (`customer_id`).
# MAGIC - **Delta Format Storage**: Saves data in **Delta Lake format** with **overwrite mode** to ensure Gold tables are refreshed.

# COMMAND ----------

# Get table names from the Silver layer
table_names = [file.name.rstrip('/') for file in dbutils.fs.ls('mnt/silver/SalesLT/')]
print("Tables found in Silver:", table_names)

# COMMAND ----------

from pyspark.sql.functions import col

# Process each table from Silver to Gold
for table in table_names:
    input_path = f'/mnt/silver/SalesLT/{table}'
    print(f"Processing: {table} from {input_path}")

    # Read Delta table from Silver layer
    try:
        df = spark.read.format('delta').load(input_path)
    except Exception as e:
        print(f"Skipping {table} due to error: {e}")
        continue  

    # Get list of original column names
    column_names = df.columns

    # Convert camel case to snake case (e.g., CustomerID → customer_id)
    for old_col_name in column_names:
        new_col_name = "".join(["_" + char.lower() if char.isupper() and not old_col_name[i - 1].isupper() else char.lower() for i, char in enumerate(old_col_name)]).lstrip("_")
        df = df.withColumnRenamed(old_col_name, new_col_name)

    # Write transformed data to Gold layer in Delta format
    output_path = f'/mnt/gold/SalesLT/{table}/'
    df.write.format('delta').mode("overwrite").save(output_path)

    print(f"Processed: {table} → Saved to {output_path}")

# COMMAND ----------

# Example Table: SalesOrderHeader (Before and After Transformation)

example_table = "SalesOrderHeader"

if example_table in table_names:
    example_path = f'/mnt/silver/SalesLT/{example_table}'

    # Read example table
    try:
        example_df = spark.read.format('delta').load(example_path)
    except Exception as e:
        print(f"Skipping {example_table} due to error: {e}")
    else:
        print(f"Before Transformation - {example_table}")
        display(example_df)

        # Apply column name transformation (CamelCase → snake_case)
        for old_col_name in example_df.columns:
            new_col_name = "".join(["_" + char.lower() if char.isupper() and not old_col_name[i - 1].isupper() else char.lower() for i, char in enumerate(old_col_name)]).lstrip("_")
            example_df = example_df.withColumnRenamed(old_col_name, new_col_name)

        print(f"After Transformation - {example_table}")
        display(example_df)