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

    def client(self):

        account = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")

        if account is None:
            raise Exception("Please ensure that service account enviornment varible is set before using user")

        credentials = service_account.Credentials.from_service_account_file(account, scopes=[
            "https://www.googleapis.com/auth/cloud-platform"])

        bqclient = bigquery.Client(credentials=credentials, project=credentials.project_id)

        return bqclient
    
    def query(self,client,query):

        start_time = time.time()

        try:
            bq_query = client.query(query)
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

    # def dataload_csv_gsbucket(self,environment, uri, table_id,response_length,start_time,err, _msg):
        
    #     self.environment.events.request.fire(
    #     request_type="GCPBQ",
    #     name=uri+"_"+table_id,
    #     response_time=(time.monotonic() - start_time) * 1000,
    #     response_length=response_length,
    #     context={},
    #     exception=err,
    # )


    