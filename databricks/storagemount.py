# Databricks notebook source
# MAGIC %md
# MAGIC ### Mount Bronze Container

# COMMAND ----------

configs = {
    "fs.azure.account.auth.type": "CustomAccessToken",
    "fs.azure.account.custom.token.provider.class": spark.conf.get(
        "spark.databricks.passthrough.adls.gen2.tokenProviderClassName"
    )
}

# Define storage details
storage_account_name = "project01sg"
container_name = "bronze"  
directory_name = "SalesLT/"  # The subdirectory inside the container
mount_point = f"/mnt/{container_name}"  # Mounting the container

# Unmount if already mounted
if any(mount.mountPoint == mount_point for mount in dbutils.fs.mounts()):
    dbutils.fs.unmount(mount_point)

# Mount the ADLS Gen2 container
dbutils.fs.mount(
    source=f"abfss://{container_name}@{storage_account_name}.dfs.core.windows.net/",
    mount_point=mount_point,
    extra_configs=configs
)

# Validate by listing files inside the container
display(dbutils.fs.ls(mount_point))

# Optionally, list files inside the "SalesLT" directory after mounting
saleslt_path = f"{mount_point}/{directory_name}"
display(dbutils.fs.ls(saleslt_path))


# COMMAND ----------

# MAGIC %md
# MAGIC ### Mount Silver Container

# COMMAND ----------

configs = {
    "fs.azure.account.auth.type": "CustomAccessToken",
    "fs.azure.account.custom.token.provider.class": spark.conf.get(
        "spark.databricks.passthrough.adls.gen2.tokenProviderClassName"
    )
}

# Define storage details
storage_account_name = "project01sg"
container_name = "silver"
mount_point = f"/mnt/{container_name}"

# Unmount if already mounted
if any(mount.mountPoint == mount_point for mount in dbutils.fs.mounts()):
    dbutils.fs.unmount(mount_point)

# Mount the ADLS Gen2 container
dbutils.fs.mount(
    source=f"abfss://{container_name}@{storage_account_name}.dfs.core.windows.net/",
    mount_point=mount_point,
    extra_configs=configs
)


# COMMAND ----------

# MAGIC %md
# MAGIC ### Mount Gold Container

# COMMAND ----------

configs = {
    "fs.azure.account.auth.type": "CustomAccessToken",
    "fs.azure.account.custom.token.provider.class": spark.conf.get(
        "spark.databricks.passthrough.adls.gen2.tokenProviderClassName"
    )
}

# Define storage details
storage_account_name = "project01sg"
container_name = "gold"
mount_point = f"/mnt/{container_name}"

# Unmount if already mounted
if any(mount.mountPoint == mount_point for mount in dbutils.fs.mounts()):
    dbutils.fs.unmount(mount_point)

# Mount the ADLS Gen2 container
dbutils.fs.mount(
    source=f"abfss://{container_name}@{storage_account_name}.dfs.core.windows.net/",
    mount_point=mount_point,
    extra_configs=configs
)

