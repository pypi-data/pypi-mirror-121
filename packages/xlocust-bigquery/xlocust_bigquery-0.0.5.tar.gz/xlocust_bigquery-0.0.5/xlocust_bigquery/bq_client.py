import os
import time

from locust import events,User

from xlocust_bigquery.bigquery import query, load_data_gs_bucket_csv, load_data_gs_bucket_json
from google.cloud import bigquery
from google.oauth2 import service_account


class BQClientUser(User):

    abstract = True

    def __init__(self, environment):
        super().__init__(environment)
        self.account = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")

        if self.account is None:
            raise Exception("Please ensure that service account enviornment varible is set before using user")

        self.credentials = service_account.Credentials.from_service_account_file(self.account, scopes=[
            "https://www.googleapis.com/auth/cloud-platform"])

        self.bqclient = bigquery.Client(credentials=self.credentials, project=self.credentials.project_id)
    
    def query(self,query):

        start_time = time.time()

        try:
            bq_query = self.bqclient.query(query)
            results = bq_query.result()
            data = results
            self.environment.events.request.fire(
            request_type="GCPBQ",
            name=query,
            response_time=int((time.time() - start_time) * 1000),
            response_length=int((time.time() - start_time) * 1000),
            context={},
            exception=None,
    )
            return data.to_dataframe()
        except Exception as e:
            print(e)
            self.environment.events.request.fire(
            request_type="GCPBQ",
            name=query,
            response_time=int((time.time() - start_time) * 1000),
            response_length=int((time.time() - start_time) * 1000),
            context={},
            exception=e,
    )

    def dataload_csv_gsbucket(self,uri, table_id):     
        start_time = time.time()
        try:
            job_config = bigquery.LoadJobConfig(
            autodetect=False,
            skip_leading_rows=1,
            source_format=bigquery.SourceFormat.CSV
            )
            job_config.schema_update_options = [
                bigquery.SchemaUpdateOption.ALLOW_FIELD_RELAXATION
            ]
            load_job = self.bqclient.load_table_from_uri(uri, table_id, job_config=job_config)

            load_job.result()

            destination_table = self.bqclient.get_table(table_id)
            print("Loaded {} rows.".format(destination_table.num_rows))
            self.environment.events.request.fire(
            request_type="GCPBQ",
            name=uri+"_"+table_id,
            response_time=int((time.time() - start_time) * 1000),
            response_length=int((time.time() - start_time) * 1000),
            context={},
            exception=None
            )

            return destination_table.num_rows
        except Exception as e:
            print(e)
            self.environment.events.request.fire(
            request_type="GCPBQ",
            name=uri+"_"+table_id,
            response_time=int((time.time() - start_time) * 1000),
            response_length=int((time.time() - start_time) * 1000),
            context={},
            exception=e,
    )


    