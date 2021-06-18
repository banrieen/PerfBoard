# coding=UTF-8
""" annotation
# 数据集标注基础测试集
# VERSION: 0.0.1
# EDITOR:  thomas
# TIMER:   2021-03-11
"""

import locust.stats
locust.stats.CONSOLE_STATS_INTERVAL_SEC = 3

from locust import TaskSet, task, between, User
from locust.contrib.fasthttp import FastHttpUser
from locust import events
import logging
import json
import os
import yaml
import pdb

TEST_CONF = os.path.join(os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + os.path.sep  ), "datas.yaml")
TEST_DATAS = {}

def read_test_datas(conf_file=TEST_CONF):
    stream = {}
    with open(conf_file,'r') as cf:
        stream =cf.read()
    conf = yaml.safe_load(stream)
    return conf

@events.quitting.add_listener
def _(environment, **kw):
    if environment.stats.total.fail_ratio > 0.001:
        logging.error("Test failed due to failure ratio > 1%")
        environment.process_exit_code = 1
    elif environment.stats.total.avg_response_time > 200:
        logging.error("Test failed due to average response time ratio > 200 ms")
        environment.process_exit_code = 2
    elif environment.stats.total.get_response_time_percentile(0.99) > 800:
        logging.error("Test failed due to 95th percentile response time > 800 ms")
        environment.process_exit_code = 3
    else:
        environment.process_exit_code = 0

class BasicalActions(TaskSet):
    """ 
    数据标注测试集

        1. 单用户并发10个task的基础操作请求
        2. 单用户持续标注1000以上图标的响应和时延
        3. 100用户并发的基础操作
        4. 20用户并发的upload/dump 500M文件的操作（数据集导入，导出）。
        5. 存储空间的耗用和回收
        6. 内存空间的耗用和系统整体的响应
        7. 内网环境、Internet下响应时延
    """
    global TEST_DATAS
    testdatas = {}


    @events.test_start.add_listener
    def on_test_start_get_homepage(self, environment, **kwargs):
        print("======================= A new test is starting, user will login! =======================")
        self.client.get(self.testdatas["RESTFULAPI"]["homepage"])
        with self.client.post(path=self.testdatas["RESTFULAPI"]["login"]["path"], 
                              headers=self.testdatas["RESTFULAPI"]["Header"], 
                              data=json.dumps(self.testdatas["ACCOUNT"]["admin"])) as response:
            if response.status_code == 200:
                token = response.json["token"]
                self.testdatas["token"] = token
                response.success()

    @events.test_stop.add_listener
    def on_test_stop_logout(self, environment, **kwargs):
        print("======================= A  test is ending, user will logout! =======================")
        responses = self.client.get(url=self.testdatas["RESTFULAPI"]["logout"]["path"])
        if responses.status_code == 200:
            rst = json.loads(responses.text, strict=False)
            if rst['success'] == '200':
                responses.success() 
    @task(1)
    def test_redirect_cvat(self):
        self.testdatas = TEST_DATAS
        with self.client.get(path=self.testdatas["RESTFULAPI"]["redirect_cvat"]["path"], 
                              headers=self.testdatas["RESTFULAPI"]["header"], 
                              params=json.dumps(self.testdatas["RESTFULAPI"]["redirect_cvat"]["datas"])) as response:
            if response.status_code == 200:
                response.success()
            elif response.status_code == 401:
                print("account error")
            else:
                response.raise_for_status()

    @task(1)
    def test_projects_list(self):
        self.testdatas = TEST_DATAS
        with self.client.get(path=self.testdatas["RESTFULAPI"]["projects_list"]["path"], 
                            headers=self.testdatas["RESTFULAPI"]["header"], 
                            params=json.dumps(self.testdatas["RESTFULAPI"]["projects_list"]["datas"])) as response:
            if response.status_code == 200:
                response.success()
            elif response.status_code == 401:
                print("account error")
            else:
                response.raise_for_status()

    @task(1)
    def test_create_task(self):
        self.testdatas = TEST_DATAS
        with self.client.post(path=self.testdatas["RESTFULAPI"]["create_task"]["path"], 
                            headers=self.testdatas["RESTFULAPI"]["header"], 
                            data=json.dumps(self.testdatas["RESTFULAPI"]["create_task"]["datas"])) as response:
            if response.status_code == 200:
                response.success()
            elif response.status_code == 401:
                print("account error")
            else:
                response.raise_for_status()

    @task(1)
    def test_upload_task_label(self):
        self.testdatas = TEST_DATAS
        with self.client.get(path=self.testdatas["RESTFULAPI"]["upload_task_label"]["path"], 
                            headers=self.testdatas["RESTFULAPI"]["header"], 
                            params=json.dumps(self.testdatas["RESTFULAPI"]["upload_task_label"]["datas"])) as response:
            if response.status_code == 200:
                response.success()
            elif response.status_code == 401:
                print("account error")
            else:
                response.raise_for_status()

    @task(1)
    def test_upload_task_data(self):
        self.testdatas = TEST_DATAS
        with self.client.get(path=self.testdatas["RESTFULAPI"]["upload_task_data"]["path"], 
                            headers=self.testdatas["RESTFULAPI"]["header"], 
                            params=json.dumps(self.testdatas["RESTFULAPI"]["upload_task_data"]["datas"])) as response:
            if response.status_code == 200:
                response.success()
            elif response.status_code == 401:
                print("account error")
            else:
                response.raise_for_status()

    @task(1)
    def test_get_task_status(self):
        self.testdatas = TEST_DATAS
        with self.client.get(path=self.testdatas["RESTFULAPI"]["get_task_status"]["path"], 
                            headers=self.testdatas["RESTFULAPI"]["header"], 
                            params=json.dumps(self.testdatas["RESTFULAPI"]["get_task_status"]["datas"])) as response:
            if response.status_code == 200:
                response.success()
            elif response.status_code == 401:
                print("account error")
            else:
                response.raise_for_status()

    @task(1)
    def test_get_task_list(self):
        self.testdatas = TEST_DATAS
        with self.client.get(path=self.testdatas["RESTFULAPI"]["get_task_list"]["path"], 
                            headers=self.testdatas["RESTFULAPI"]["header"], 
                            params=json.dumps(self.testdatas["RESTFULAPI"]["get_task_list"]["datas"])) as response:
            if response.status_code == 200:
                response.success()
            elif response.status_code == 401:
                print("account error")
            else:
                response.raise_for_status()

    @task(1)
    def test_auto_annotations(self):
        self.testdatas = TEST_DATAS
        with self.client.post(path=self.testdatas["RESTFULAPI"]["auto_annotations"]["path"], 
                            headers=self.testdatas["RESTFULAPI"]["header"], 
                            data=json.dumps(self.testdatas["RESTFULAPI"]["auto_annotations"]["datas"])) as response:
            if response.status_code == 200:
                response.success()
            elif response.status_code == 401:
                print("account error")
            else:
                response.raise_for_status()

    @task(1)
    def test_open_task(self):
        self.testdatas = TEST_DATAS
        with self.client.get(path=self.testdatas["RESTFULAPI"]["open_task"]["path"], 
                            headers=self.testdatas["RESTFULAPI"]["header"], 
                            params=json.dumps(self.testdatas["RESTFULAPI"]["open_task"]["datas"])) as response:
            if response.status_code == 200:
                response.success()
            elif response.status_code == 401:
                print("account error")
            else:
                response.raise_for_status()

    @task(1)
    def test_open_job(self):
        self.testdatas = TEST_DATAS
        with self.client.get(path=self.testdatas["RESTFULAPI"]["open_job"]["path"], 
                            headers=self.testdatas["RESTFULAPI"]["header"], 
                            params=json.dumps(self.testdatas["RESTFULAPI"]["open_job"]["datas"])) as response:
            if response.status_code == 200:
                response.success()
            elif response.status_code == 401:
                print("account error")
            else:
                response.raise_for_status()

    @task(1)
    def test_open_job_meta(self):
        self.testdatas = TEST_DATAS
        with self.client.get(path=self.testdatas["RESTFULAPI"]["open_job_meta"]["path"], 
                             headers=self.testdatas["RESTFULAPI"]["header"], 
                             params=json.dumps(self.testdatas["RESTFULAPI"]["open_job_meta"]["datas"])) as response:
            if response.status_code == 200:
                response.success()
            elif response.status_code == 401:
                print("account error")
            else:
                response.raise_for_status()

    @task(1)
    def test_open_job_logs(self):
        self.testdatas = TEST_DATAS
        with self.client.post(path=self.testdatas["RESTFULAPI"]["open_job_logs"]["path"], 
                             headers=self.testdatas["RESTFULAPI"]["header"], 
                             data=json.dumps(self.testdatas["RESTFULAPI"]["open_job_logs"]["datas"])) as response:
            if response.status_code == 200:
                response.success()
            elif response.status_code == 401:
                print("account error")
            else:
                response.raise_for_status()

    @task(1)
    def test_open_job_data(self):
        self.testdatas = TEST_DATAS
        with self.client.get(path=self.testdatas["RESTFULAPI"]["open_job_data"]["path"], 
                             headers=self.testdatas["RESTFULAPI"]["header"], 
                             params=json.dumps(self.testdatas["RESTFULAPI"]["open_job_data"]["datas"])) as response:
            if response.status_code == 200:
                response.success()
            elif response.status_code == 401:
                print("account error")
            else:
                response.raise_for_status()

    @task(1)
    def test_open_job_annotations(self):
        self.testdatas = TEST_DATAS
        with self.client.get(path=self.testdatas["RESTFULAPI"]["open_job_annotations"]["path"], 
                             headers=self.testdatas["RESTFULAPI"]["header"], 
                             params=json.dumps(self.testdatas["RESTFULAPI"]["open_job_annotations"]["datas"])) as response:
            if response.status_code == 200:
                response.success()
            elif response.status_code == 401:
                print("account error")
            else:
                response.raise_for_status()

    @task(1)
    def test_save_job(self):
        self.testdatas = TEST_DATAS
        with self.client.get(path=self.testdatas["RESTFULAPI"]["save_job"]["path"], 
                             headers=self.testdatas["RESTFULAPI"]["header"], 
                             params=json.dumps(self.testdatas["RESTFULAPI"]["save_job"]["datas"])) as response:
            if response.status_code == 200:
                response.success()
            elif response.status_code == 401:
                print("account error")
            else:
                response.raise_for_status()

    @task(1)
    def test_save_job_create_annotations(self):
        self.testdatas = TEST_DATAS
        with self.client.patch(path=self.testdatas["RESTFULAPI"]["save_job_create_annotations"]["path"], 
                             headers=self.testdatas["RESTFULAPI"]["header"], 
                             data=json.dumps(self.testdatas["RESTFULAPI"]["save_job_create_annotations"]["datas"])) as response:
            if response.status_code == 200:
                response.success()
            elif response.status_code == 401:
                print("account error")
            else:
                response.raise_for_status()

    @task(1)
    def test_save_job_update_annotations(self):
        self.testdatas = TEST_DATAS
        with self.client.patch(path=self.testdatas["RESTFULAPI"]["save_job_update_annotations"]["path"], 
                             headers=self.testdatas["RESTFULAPI"]["header"], 
                             data=json.dumps(self.testdatas["RESTFULAPI"]["save_job_update_annotations"]["datas"])) as response:
            if response.status_code == 200:
                response.success()
            elif response.status_code == 401:
                print("account error")
            else:
                response.raise_for_status()

    @task(1)
    def test_save_job_delete_annotations(self):
        self.testdatas = TEST_DATAS
        with self.client.patch(path=self.testdatas["RESTFULAPI"]["save_job_delete_annotations"]["path"], 
                             headers=self.testdatas["RESTFULAPI"]["header"], 
                             data=json.dumps(self.testdatas["RESTFULAPI"]["save_job_delete_annotations"]["datas"])) as response:
            if response.status_code == 200:
                response.success()
            elif response.status_code == 401:
                print("account error")
            else:
                response.raise_for_status()

    @task(1)
    def test_save_save_job_logs(self):
        self.testdatas = TEST_DATAS
        with self.client.post(path=self.testdatas["RESTFULAPI"]["save_job_logs"]["path"], 
                             headers=self.testdatas["RESTFULAPI"]["header"], 
                             data=json.dumps(self.testdatas["RESTFULAPI"]["save_job_logs"]["datas"])) as response:
            if response.status_code == 200:
                response.success()
            elif response.status_code == 401:
                print("account error")
            else:
                response.raise_for_status()

    @task(1)
    def test_save_job_loader(self):
        self.testdatas = TEST_DATAS
        with self.client.post(path=self.testdatas["RESTFULAPI"]["save_job_loader"]["path"], 
                             headers=self.testdatas["RESTFULAPI"]["header"], 
                             data=json.dumps(self.testdatas["RESTFULAPI"]["save_job_loader"]["datas"])) as response:
            if response.status_code == 200:
                response.success()
            elif response.status_code == 401:
                print("account error")
            else:
                response.raise_for_status()

    @task(1)
    def test_reback_task(self):
        self.testdatas = TEST_DATAS
        with self.client.post(path=self.testdatas["RESTFULAPI"]["reback_task"]["path"], 
                             headers=self.testdatas["RESTFULAPI"]["header"], 
                             data=json.dumps(self.testdatas["RESTFULAPI"]["reback_task"]["datas"])) as response:
            if response.status_code == 200:
                response.success()
            elif response.status_code == 401:
                print("account error")
            else:
                response.raise_for_status() 

    @task(1)
    def test_upload_anotaion(self):
        self.testdatas = TEST_DATAS
        with self.client.post(path=self.testdatas["RESTFULAPI"]["upload_anotaion"]["path"], 
                             headers=self.testdatas["RESTFULAPI"]["header"], 
                             data=json.dumps(self.testdatas["RESTFULAPI"]["upload_anotaion"]["datas"])) as response:
            if response.status_code == 200:
                response.success()
            elif response.status_code == 401:
                print("account error")
            else:
                response.raise_for_status() 

    @task(1)
    def test_push_to_ai_platform(self):
        self.testdatas = TEST_DATAS
        with self.client.get(path=self.testdatas["RESTFULAPI"]["push_to_ai_platform"]["path"], 
                             headers=self.testdatas["RESTFULAPI"]["header"], 
                             params=json.dumps(self.testdatas["RESTFULAPI"]["push_to_ai_platform"]["datas"])) as response:
            if response.status_code == 200:
                response.success()
            elif response.status_code == 401:
                print("account error")
            else:
                response.raise_for_status()  

    @task(1)
    def test_dump_anotation(self):
        self.testdatas = TEST_DATAS
        with self.client.get(path=self.testdatas["RESTFULAPI"]["dump_anotation"]["path"], 
                             headers=self.testdatas["RESTFULAPI"]["header"], 
                             params=json.dumps(self.testdatas["RESTFULAPI"]["dump_anotation"]["datas"])) as response:
            if response.status_code == 200:
                response.success()
            elif response.status_code == 401:
                print("account error")
            else:
                response.raise_for_status() 

    @task(1)
    def test_delect_task(self):
        self.testdatas = TEST_DATAS
        with self.client.delete(path=self.testdatas["RESTFULAPI"]["delect_task"]["path"], 
                             headers=self.testdatas["RESTFULAPI"]["header"], 
                             data=json.dumps(self.testdatas["RESTFULAPI"]["delect_task"]["datas"])) as response:
            if response.status_code == 200:
                response.success()
            elif response.status_code == 401:
                print("account error")
            else:
                response.raise_for_status() 

class AnnotationUser(FastHttpUser):
    global TEST_DATAS  
    sock = None
    wait_time = between(0.5, 5) 
    TEST_DATAS = read_test_datas(conf_file=TEST_CONF)
    tasks = [BasicalActions]

if __name__ == "__main__":
    cmd = 'locust -f locust_demo.py'
    os.system(cmd)
    # Run in cmd
    # locust -f ./testhub/testsuites/annotations_cvat/test_cvat_actions.py --conf ./testhub/testsuites/annotations_cvat/host.conf

