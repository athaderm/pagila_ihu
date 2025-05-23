#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#pip install --upgrade pip
#pip install google-cloud-bigquery
#pip install pandas-gbq -U
#pip install db-dtypes
#pip install packaging --upgrade


# In[1]:


# Import libraries
from google.cloud import bigquery
import pandas as pd
from pandas_gbq import to_gbq
import os

print('Libraries imported successfully')


# In[2]:


# Set the environment variable for Google Cloud credentials
# Place the path in which the .json file is located.

# Example (if .json is located in the same directory with the notebook)
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "at-arch-416714-6f9900ec7.json"

# -- YOUR CODE GOES BELOW THIS LINE
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/data_analytics_in_corpo/cosmic-strategy-454618-b0-39bdb7a347d0.json" # Edit path
# -- YOUR CODE GOES ABOVE THIS LINE


# In[3]:


# Set your Google Cloud project ID and BigQuery dataset details

# -- YOUR CODE GOES BELOW THIS

project_id = 'cosmic-strategy-454618-b0' # Edit with your project id
dataset_id = 'staging_db' # Modify the necessary schema name: staging_db, reporting_db etc.
table_id = 'stg_payment' # Modify the necessary table name: stg_customer, stg_city etc.

# -- YOUR CODE GOES ABOVE THIS LINE


# In[5]:


# Create a BigQuery client
client = bigquery.Client(project=project_id)

# -- YOUR CODE GOES BELOW THIS LINE

# Define your SQL query here
query = """
with base as (
  select *
  from `cosmic-strategy-454618-b0.pagila_productionpublic.payment` --Your table path
  )

  , final as (
    select
        payment_id
        , customer_id
        , staff_id
        , rental_id
        , amount as payment_amount
        , payment_date
   FROM base
  )

  select * from final
"""

# -- YOUR CODE GOES ABOVE THIS LINE

# Execute the query and store the result in a dataframe
df = client.query(query).to_dataframe()

# Explore some records
df.head()


# In[8]:


# Define the full table ID
full_table_id = f"{project_id}.{dataset_id}.{table_id}"

# -- YOUR CODE GOES BELOW THIS LINE
# Define table schema based on the project description

schema = [
    bigquery.SchemaField('payment_id', 'INTEGER'),
    bigquery.SchemaField('customer_id', 'INTEGER'),
    bigquery.SchemaField('staff_id', 'INTEGER'),
    bigquery.SchemaField('rental_id', 'INTEGER'),
    bigquery.SchemaField('payment_amount', 'NUMERIC'),
    bigquery.SchemaField('payment_date', 'DATETIME'),
    ]

# -- YOUR CODE GOES ABOVE THIS LINE


# In[9]:


# Create a BigQuery client
client = bigquery.Client(project=project_id)

# Check if the table exists
def table_exists(client, full_table_id):
    try:
        client.get_table(full_table_id)
        return True
    except Exception:
        return False

# Write the dataframe to the table (overwrite if it exists, create if it doesn't)
if table_exists(client, full_table_id):
    # If the table exists, overwrite it
    destination_table = f"{dataset_id}.{table_id}"
    # Write the dataframe to the table (overwrite if it exists)
    to_gbq(df, destination_table, project_id=project_id, if_exists='replace')
    print(f"Table {full_table_id} exists. Overwritten.")
else:
    # If the table does not exist, create it
    job_config = bigquery.LoadJobConfig(schema=schema)
    job = client.load_table_from_dataframe(df, full_table_id, job_config=job_config)
    job.result()  # Wait for the job to complete
    print(f"Table {full_table_id} did not exist. Created and data loaded.")


# In[ ]:




