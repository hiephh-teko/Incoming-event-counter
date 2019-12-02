from prometheus_client.parser import text_string_to_metric_families
import requests
from datetime import datetime, timedelta
import time
import threading
import pytz
import operator


class Data:
    def __init__(self, time, value):
        self.value = value
        self.time = time


class Counter(object):
    def __init__(self):
        self.url = "http://103.126.156.23:9090/api/v1/query"
        self.metric_name_list = ["kafka_consumergroup_current_offset",
                                 "logstash_node_pipeline_events_filtered_total", "logstash_node_pipeline_events_out_total"]

    def get_greatest_value_less_than_x(self, x):
        res = Data(-1,-1)
        for data in self.data_list:
            if (data.time < x):
                res = data 
            else:
                break

        if (res.time == -1):
            res = self.data_list[0]
        
        return res 
    
    def get_greatest_value_less_equal_than_x(self, x):
        res = Data(-1,-1)
        _len = len(self.data_list)
        
        _id = _len - 1
        while (_id>0):
            if (self.data_list[_id].time<=x):
                return self.data_list[_id]
            _id -=1

    def counter_by_metric(self, metric_name):
        response = requests.get(
            self.url, params={'query': metric_name+'[50h]'})

        ################################TEST########################
        # response = requests.get(
        #     self.url, params={'query': "%s[1m]" % (metric_name)})
        ###########################################################

        results = response.json()['data']['result']

        data_list = []
        for result in results:
            metric = result["metric"]

            if metric_name == self.metric_name_list[0]:
                if (metric["consumergroup"] == "product") & (metric["instance"] == "103.126.156.125:9308"):
                    values = result["values"]

            elif (metric["job"] == "logstashExporter_Live") & (metric["instance"] == "103.126.156.123:9198"):
                values = result["values"]

        for value in values:
            data_list.append(Data(value[0],value[1]))

        self.data_list = sorted(data_list, key=operator.attrgetter('time'))

        start_value = self.get_greatest_value_less_than_x(self.start_unix)
        end_value = self.get_greatest_value_less_equal_than_x(self.end_unix)
        print(metric_name, end_value.time, end_value.value, start_value.time, start_value.value)


    def enter(self):
        threads = list()

        # get current time
        now = datetime.utcfromtimestamp(time.time())
        # get previous day
        previous_day = (now-timedelta(days=1))
        # get start of previous day
        self.start_unix = previous_day.replace(
            microsecond=0, second=0, minute=0, hour=0).replace(tzinfo=pytz.utc).timestamp()
        # get end of previous day
        self.end_unix = previous_day.replace(
            microsecond=999999, second=59, minute=59, hour=23).replace(tzinfo=pytz.utc).timestamp()
        print("start_unix", self.start_unix, self.end_unix)
        for metric_name in self.metric_name_list:

            job = threading.Thread(
                target=self.counter_by_metric, args=(metric_name,))
            threads.append(job)
            job.start()

        for index, thread in enumerate(threads):
            thread.join()

