import time

from locust import events

from xlocust_bigquery.bigquery import query, load_data_gs_bucket_csv, load_data_gs_bucket_json


class BQClient:
    def __getattr__(self, name):
        def wrapper(*args, **kwargs):
            start_time = time.perf_counter()
            try:
                exec_query = query(*args, **kwargs)
                events.request_success.fire(request_type="gcp_bq",
                                            name=name,
                                            response_time=int((time.time() - start_time) * 1000),
                                            response_length=len(exec_query))
                data_loader_csv = load_data_gs_bucket_csv(*args, **kwargs)
                events.request_success.fire(request_type="gcp_bq",
                                            name=name,
                                            response_time=int((time.time() - start_time) * 1000),
                                            response_length=data_loader_csv)
                data_loader_csv = load_data_gs_bucket_json(*args, **kwargs)
                events.request_success.fire(request_type="gcp_bq",
                                            name=name,
                                            response_time=int((time.time() - start_time) * 1000),
                                            response_length=data_loader_csv)
            except Exception as e:
                events.request_failure.fire(request_type="gcp_bq",
                                            name=name,
                                            response_time=int((time.time() - start_time) * 1000),
                                            exception=e)

                print('error {}'.format(e))

        return wrapper
