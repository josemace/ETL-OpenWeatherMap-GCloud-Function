import config
import logging
import pandas as pd
from google.cloud import bigquery
from google.cloud import storage

def df_to_bucket(df: pd.DataFrame):
    """ Upload the given csv file to a bucket"""

    try:
        # Initiate Client with the user credentials provided by using the gcloud CLI
        project_id = config.config_vars.get("project_id")
        storage_client = storage.Client(project=project_id)

        #print(buckets = list(storage_client.list_buckets())

        # Select the bucket where to upload the file
        bucket_id = config.config_vars.get("bucket_id")
        bucket = storage_client.get_bucket(bucket_id)

        # Create the file/object
        blob_name = config.config_vars.get("output_filename")
        blob = bucket.blob(blob_name)

        # Upload the file
        blob.upload_from_string(df.to_csv(index=False), 'text/csv')
        
        #returns a public url
        return blob.public_url

    except Exception as e:
        logging.error(f"[Exception] {e} on {e.__traceback__.tb_frame} line {e.__traceback__.tb_lineno}")


def blob_to_bigquery(blob_uri):
    """Load the data from a given Google Cloud Storage file into Google BigQuery"""

    try:
        # Set up a client object for interacting with Google BigQuery
        project_id = config.config_vars.get("project_id")
        bigquery_client = bigquery.Client(project=project_id)

        # Set up a job config object with the CSV options
        job_config = bigquery.LoadJobConfig(
            source_format=bigquery.SourceFormat.CSV,
            skip_leading_rows=1,
            autodetect=True
        )

        # Create a job to load the data from the CSV file into a BigQuery table
        dataset_id = config.config_vars.get("output_dataset_id")
        table_name = config.config_vars.get("output_table_name")
        job = bigquery_client.load_table_from_uri(
            source_uris=blob_uri,
            destination=f"{project_id}.{dataset_id}.{table_name}",
            job_config=job_config
        )

        # Wait for the job to complete
        job.result()

    except Exception as e:
        logging.error(f"[Exception] {e} on {e.__traceback__.tb_frame} line {e.__traceback__.tb_lineno}")
