# Azure End-to-End Data Engineering Project: From On-Prem to Cloud Analytics
## Project Overview
This project demonstrates how to build a **fully automated data pipeline on Azure** to extract, process, and visualize **customer and sales data** from an **on-premises SQL Server database**.

## Learning & Inspiration
I followed the methodologies and processes demonstrated by **[Mr.K Talks Tech](https://www.youtube.com/watch?v=iQ41WqhHglk)** and **[Luke J Byrne](https://www.youtube.com/watch?v=ygJ11fzq_ik)**, adapting their approaches to implement my own **Azure-based data pipeline**.

Through this hands-on experience, I gained a deeper understanding of **Azure Data Factory, Databricks, Synapse Analytics, and Power BI**, while also customizing the workflow to align with real-world business use cases.

## Business Requirements
The company aims to gain deeper insights into its customer demographics, particularly the gender distribution of its customer base and its impact on product sales. With a vast amount of customer data stored in an on-premises SQL database, stakeholders require a comprehensive KPI dashboard to analyze sales trends.

This dashboard should:

- Provide a breakdown of total products, total customers, and overall sales revenue.
- Visualize customer distribution and sales revenue by gender.
- Enable users to filter sales data by product category and interactively explore data by gender.
- Offer a user-friendly interface for seamless analysis.

By implementing this solution, stakeholders can make data-driven decisions and better understand how customer demographics influence sales performance.

## Technology Used
1. **Cloud Platform - Microsoft Azure**  
   - **Azure Data Factory (ADF)** – Manages and automates data movement between different services, ensuring seamless ETL (Extract, Transform, Load) workflows. 
   - **Azure Data Lake Storage (ADLS)** – Serves as a centralized repository for storing both raw and processed data at different stages of the pipeline.
   - **Azure Databricks** – Provides a scalable environment for processing and transforming data using PySpark and distributed computing.
   - **Azure Synapse Analytics** – Creates and manages serverless SQL views, executes SQL queries for data retrieval, and orchestrates data processing through Synapse pipelines for structured data integration with Power BI.
   - **Azure Key Vault** – Securely stores and manages authentication credentials, such as secrets and tokens, used for accessing Azure services. 

2. **Programming & Querying**  
   - **Python (PySpark)** - Used in Databricks notebooks for:
     - **Mounting Storage Containers** (`storagemount.py`)
     - **Transforming Bronze to Silver Layer** (`Bronze layer to Silver Layer.py`)
     - **Transforming Silver to Gold Layer** (`Silver layer to Gold layer.py`)
   - **SQL (T-SQL)** - Used for querying structured data in SSMS  

3. **Visualization & Reporting**  
   - **Power BI** - Data visualization and interactive reporting

## Data Source (On-Premises)
For this project, I used the **Lightweight version of AdventureWorksLT2022**, a sample database provided by Microsoft.  

Dataset Download Link:  [AdventureWorksLT2022.bak - Microsoft Docs](https://learn.microsoft.com/en-us/sql/samples/adventureworks-install-configure?view=sql-server-ver16&tabs=ssms)  

##  Architecture Diagram
![diagram](https://github.com/user-attachments/assets/645ec48c-fdf3-4aed-97dd-f0cb3633ecf8)

## Implementation Steps
### Step 1: Setting Up Azure Environment  
- **Create a Resource Group** to organize and manage all Azure resources.  
- **Deploy Azure Data Factory (ADF)** to orchestrate data movement and pipeline automation.  
- **Set up Azure Data Lake Storage (ADLS)** with structured containers:  
  - **Bronze Layer** → Stores raw, unprocessed data.  
  - **Silver Layer** → Stores transformed data.  
  - **Gold Layer** → Stores final data for **Power BI** and reporting.  
- **Create an Azure Databricks workspace** for scalable data processing:  
  - **Set up a Cluster** optimized for workload needs.  
  - Use **fixed worker nodes** to balance cost and performance.  
  - Enable **Auto-Termination** to shut down inactive clusters.  
- **Set up Azure Synapse Analytics** to store and query **Gold Layer data** efficiently.  
- **Configure Azure Key Vault** to store and manage secrets securely.

### Step 2: Data Ingestion  
#### 2.1 Setup On-Premises SQL Server  
- Install **SQL Server** and **SQL Server Management Studio (SSMS)**.  
- Restore the **AdventureWorksLT2022** database as the source.  
#### 2.2 Configure Linked Services in Azure Data Factory (ADF)  
- Create **Linked Services** to connect:  
  - **On-Prem SQL Server** (via Self-Hosted Integration Runtime - SHIR).  
  - **Azure Data Lake Storage (ADLS)** for raw data storage.  
  - **Azure Key Vault** to securely store secrets for connecting ADLS with SSMS.  
#### 2.3 Build ADF Pipeline for Data Ingestion  
- **Lookup Activity**: Fetch table metadata from SQL Server.  
- **ForEach Activity**: Loop through each table dynamically.  
- **Copy Data Activity**: Transfer data from SQL Server → **ADLS (Bronze Layer)**.  

![ADF pipeline](https://github.com/user-attachments/assets/8a7ca00f-2ae5-45d5-83ed-55628d7ce107)

### Step 3: Data Transformation  

#### 3.1 Establish Connection in Databricks  
- **Mount ADLS** in Databricks to access **Bronze, Silver, and Gold Layers**.  
- Secure connection between **ADF and Databricks** is managed via **Linked Services & Azure Key Vault**.

#### 3.2 Process and Refine Data Using Databricks Notebooks  

**Bronze → Silver Layer**  
- Convert date formats to `YYYY-MM-DD` for consistency.  
- Store processed data in **Delta format** for efficient updates.  

**Silver → Gold Layer**  
- Rename columns (e.g., `CustomerID → customer_id`) for readability.  
- Save refined data in **Delta format** to enable fast querying.  

### Step 4: Data Loading and Reporting  
#### 4.1 Load Data into Azure Synapse Analytics  
- Use **ADF Get Metadata Activity** to retrieve table names from the **Gold Layer** in ADLS.  
- Iterate through tables dynamically using **ForEach Activity**.  
- Execute a **Stored Procedure** in Synapse to create **SQL Serverless Views** using `OPENROWSET`.  

![pipeline in synapse](https://github.com/user-attachments/assets/c14c6a72-1b61-4d02-98b2-8cd50b481db7)

#### 4.2 Build Power BI Dashboard  
**Connect Power BI to Synapse**  
- Install **Power BI Desktop** and connect to **Azure Synapse Analytics**.  
**Design Power BI Reports**  
- Create **data models** and define **table relationships**.  
- Build **interactive visualizations** to meet business requirements. 

![dashboard](https://github.com/user-attachments/assets/27a9885f-c973-47d0-8546-10a5321ce645)











