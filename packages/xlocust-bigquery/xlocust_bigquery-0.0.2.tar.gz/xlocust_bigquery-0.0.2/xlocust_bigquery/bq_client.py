import functools
import os
import time

from locust import events,User

from xlocust_bigquery.bigquery import query, load_data_gs_bucket_csv, load_data_gs_bucket_json
from google.cloud import bigquery
from google.cloud.bigquery.table import RowIterator, _EmptyRowIterator
from google.oauth2 import service_account


class BQClientUser(User):

    abstract = True

    def __init__(self, environment):
        super().__init__(environment)

    def client(self):
        account = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")

        credentials = service_account.Credentials.from_service_account_file(account, scopes=[
            "https://www.googleapis.com/auth/cloud-platform"])

        self.bqclient = bigquery.Client(credentials=credentials, project=credentials.project_id)
    
    def query(self,query):

        start_time = time.time()

        try:
            bqclient = self.client()
            bq_query = bqclient.query(query)
            results = bq_query.result()
            data = results
            return data
        except Exception as e:
            self.environment.events.request.fire(
            request_type="GCPBQ",
            name=query,
            response_time=int((time.time() - start_time) * 1000),
            response_length=int((time.time() - start_time) * 1000),
            context={},
            exception=e,
    )



    # def dataload_csv_gsbucket(self,environment, uri, table_id,response_length,start_time,err, _msg):
        
    #     self.environment.events.request.fire(
    #     request_type="GCPBQ",
    #     name=uri+"_"+table_id,
    #     response_time=(time.monotonic() - start_time) * 1000,
    #     response_length=response_length,
    #     context={},
    #     exception=err,
    # )


    