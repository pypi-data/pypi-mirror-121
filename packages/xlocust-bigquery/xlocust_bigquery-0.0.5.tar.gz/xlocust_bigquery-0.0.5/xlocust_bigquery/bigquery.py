import os
from typing import Union

from dotenv import load_dotenv, find_dotenv
from google.cloud import bigquery
from google.cloud.bigquery.table import RowIterator, _EmptyRowIterator
from google.oauth2 import service_account

load_dotenv(find_dotenv())


def client():
    account = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")

    credentials = service_account.Credentials.from_service_account_file(account, scopes=[
        "https://www.googleapis.com/auth/cloud-platform"])

    bqclient = bigquery.Client(credentials=credentials, project=credentials.project_id)

    return bqclient


def query(query):
    bqclient = client()
    bq_query = bqclient.query(query)
    results: Union[RowIterator, _EmptyRowIterator] = bq_query.result()
    data = results
    return data


def load_data_gs_bucket_csv(uri, table_id):
    bqclient = client()
    job_config = bigquery.LoadJobConfig(
        autodetect=False,
        skip_leading_rows=1,
        source_format=bigquery.SourceFormat.CSV
    )
    job_config.schema_update_options = [
        bigquery.SchemaUpdateOption.ALLOW_FIELD_RELAXATION
    ]
    load_job = bqclient.load_table_from_uri(uri, table_id, job_config=job_config)

    load_job.result()

    destination_table = bqclient.get_table(table_id)
    print("Loaded {} rows.".format(destination_table.num_rows))
    return destination_table.num_rows


def load_data_gs_bucket_json(uri, table_id):
    bqclient = client()
    job_config = bigquery.LoadJobConfig(
        autodetect=True,
        skip_leading_rows=1,
        source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON
    )
    job_config.schema_update_options = [
        bigquery.SchemaUpdateOption.ALLOW_FIELD_RELAXATION,
        bigquery.SchemaUpdateOption.ALLOW_FIELD_ADDITION
    ]
    load_job = bqclient.load_table_from_uri(uri, table_id, job_config=job_config)

    load_job.result()

    destination_table = bqclient.get_table(table_id)
    print("Loaded {} rows.".format(destination_table.num_rows))
