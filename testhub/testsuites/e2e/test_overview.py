
""" 测试单（场景）
# 平台概览页面
# ScriptType：performance test 
# UpdateDate: 2021.03-30
# Matainer: thomas
# Env: Win10 64bit, python3.8
 """


from locust import HttpUser, TaskSet, task, between
from locust.contrib.fasthttp import FastHttpUser
from locust import events
from locust.clients import HttpSession
import logging
import json
import os
import yaml
import pdb
import hashlib
from testhub.testlib import fake_users
from testhub.testlib import csv_client

TEST_CONF = os.path.join(os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + os.path.sep  ), "datas.yaml")
TEST_DATAS = {}
USER_CREDENTIALS = []

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
    elif environment.stats.total.avg_response_time > 5000:
        logging.error("Test failed due to average response time ratio > 200 ms")
        environment.process_exit_code = 2
    elif environment.stats.total.get_response_time_percentile(0.99) > 2000:
        logging.error("Test failed due to 95th percentile response time > 800 ms")
        environment.process_exit_code = 3
    else:
        environment.process_exit_code = 0


class OverviewStatus(TaskSet):
    """ testsuite
    1. 查看概览页面和各个窗口展示内容
    """
    global TEST_DATAS

    def on_start(self):
        print("======================= A new test is starting, user will login {} ! =======================".format(TEST_DATAS["ENV"]["HOST"]))
        self.client.request("get",TEST_DATAS["RESTFULAPI"]["homepage"])
        self.client.header = TEST_DATAS["RESTFULAPI"]["header"]
        account = USER_CREDENTIALS.pop()
        print("======================= USER_CREDENTIALS.pop: {} ".format(account))
        response = self.client.request(TEST_DATAS["RESTFULAPI"]["login"]["mothed"], url=TEST_DATAS["RESTFULAPI"]["login"]["path"], data=account)
        result = response.json()
        try:
            if result["success"]:
                TEST_DATAS["ACCOUNT"]["token"] = result["token"]
                TEST_DATAS["ACCOUNT"]["currentRole_id"] = result["currentRole"][0]["id"]
                TEST_DATAS["RESTFULAPI"]["header"]["Authorization"] = "Bearer " + TEST_DATAS["ACCOUNT"]["token"]
                TEST_DATAS["RESTFULAPI"]["cookie"] = response.cookies
        except KeyError: 
            response.raise_for_status()

    def on_stop(self):
        print("======================= A  test is ending, user will logout {} ! =======================".format(TEST_DATAS["ENV"]["HOST"]))
        response = self.client.request("get", url=TEST_DATAS["RESTFULAPI"]["logout"]["path"])

    @task(1)
    def test_get_verview(self):
        """ testcase
        1. 查看概览
         """
        response = self.client.request(TEST_DATAS["RESTFULAPI"]["get_verview"]["mothed"], 
                                        url=TEST_DATAS["RESTFULAPI"]["get_verview"]["path"],
                                        headers=TEST_DATAS["RESTFULAPI"]["header"], 
                                        cookies=TEST_DATAS["RESTFULAPI"]["cookie"]) 

    @task(1)
    def test_get_codedev(self):
        """ testcase
        1. 查看代码开发环境
         """
        response = self.client.request(TEST_DATAS["RESTFULAPI"]["get_codedev"]["mothed"], 
                                        url=TEST_DATAS["RESTFULAPI"]["get_codedev"]["path"],
                                        headers=TEST_DATAS["RESTFULAPI"]["header"], 
                                        cookies=TEST_DATAS["RESTFULAPI"]["cookie"]) 

    @task(1)
    def test_get_datasets(self):
        """ testcase
        1. 查看数据集管理列表
         """
        response = self.client.request(TEST_DATAS["RESTFULAPI"]["get_datasets"]["mothed"], 
                                        url=TEST_DATAS["RESTFULAPI"]["get_datasets"]["path"],
                                        headers=TEST_DATAS["RESTFULAPI"]["header"], 
                                        cookies=TEST_DATAS["RESTFULAPI"]["cookie"]) 

    @task(0)
    def test_get_train(self):
        """ testcase
        1. 查看模型训练
         """
        response = self.client.request(TEST_DATAS["RESTFULAPI"]["get_train"]["mothed"], 
                                        url=TEST_DATAS["RESTFULAPI"]["get_train"]["path"],
                                        headers=TEST_DATAS["RESTFULAPI"]["header"], 
                                        cookies=TEST_DATAS["RESTFULAPI"]["cookie"])

    @task(1)
    def test_get_models(self):
        """ testcase
        1. 查看预置模型
         """
        response = self.client.request(TEST_DATAS["RESTFULAPI"]["get_models"]["mothed"], 
                                        url=TEST_DATAS["RESTFULAPI"]["get_models"]["path"],
                                        headers=TEST_DATAS["RESTFULAPI"]["header"], 
                                        cookies=TEST_DATAS["RESTFULAPI"]["cookie"])

    @task(1)
    def test_visualmodels(self):
        """ testcase
        1. 查看可视化训练
         """
        response = self.client.request(TEST_DATAS["RESTFULAPI"]["visualmodels"]["mothed"], 
                                        url=TEST_DATAS["RESTFULAPI"]["visualmodels"]["path"],
                                        headers=TEST_DATAS["RESTFULAPI"]["header"], 
                                        cookies=TEST_DATAS["RESTFULAPI"]["cookie"])

    @task(1)
    def test_get_inferences(self):
        """ testcase
        1. 查看数据集存储列表
         """
        response = self.client.request(TEST_DATAS["RESTFULAPI"]["get_inferences"]["mothed"], 
                                        url=TEST_DATAS["RESTFULAPI"]["get_inferences"]["path"],
                                        headers=TEST_DATAS["RESTFULAPI"]["header"], 
                                        cookies=TEST_DATAS["RESTFULAPI"]["cookie"])
    
    @task(0)
    def test_get_grafana_query(self):
        """ testcase
        1. 查看监控请求
         """
        response = self.client.request(TEST_DATAS["RESTFULAPI"]["get_grafana_query"]["mothed"], 
                                        url=TEST_DATAS["RESTFULAPI"]["get_grafana_query"]["path"],
                                        headers=TEST_DATAS["RESTFULAPI"]["header"], 
                                        cookies=TEST_DATAS["RESTFULAPI"]["cookie"])
    
    @task(0)
    def test_get_grafanadashboard(self):
        """ testcase
        1. 查看监控界面
         """
        response = self.client.request(TEST_DATAS["RESTFULAPI"]["get_grafanadashboard"]["mothed"], 
                                        url=TEST_DATAS["RESTFULAPI"]["get_grafanadashboard"]["path"],
                                        headers=TEST_DATAS["RESTFULAPI"]["header"], 
                                        cookies=TEST_DATAS["RESTFULAPI"]["cookie"])
  
    @task(1)
    def test_get_vc_info(self):
        """ testcase
        1. 查看VC配置
         """
        response = self.client.request(TEST_DATAS["RESTFULAPI"]["get_vc_info"]["mothed"], 
                                        url=TEST_DATAS["RESTFULAPI"]["get_vc_info"]["path"],
                                        headers=TEST_DATAS["RESTFULAPI"]["header"], 
                                        cookies=TEST_DATAS["RESTFULAPI"]["cookie"])
  
    @task(1)
    def test_get_platform_config(self):
        """ testcase
        1. 查看平台配置
         """
        response = self.client.request(TEST_DATAS["RESTFULAPI"]["get_platform_config"]["mothed"], 
                                        url=TEST_DATAS["RESTFULAPI"]["get_platform_config"]["path"],
                                        headers=TEST_DATAS["RESTFULAPI"]["header"], 
                                        cookies=TEST_DATAS["RESTFULAPI"]["cookie"])
  
    @task(0)
    def test_get_jobs(self):
        """ testcase
        1. 查看任务
         """
        response = self.client.request(TEST_DATAS["RESTFULAPI"]["get_jobs"]["mothed"], url=TEST_DATAS["RESTFULAPI"]["get_jobs"]["path"])

    @task(0)  
    def test_get_savedimages(self):
        """ testcase
        1. 查看保存的镜像
         """
        response = self.client.request(TEST_DATAS["RESTFULAPI"]["get_savedimages"]["mothed"], 
                                        url=TEST_DATAS["RESTFULAPI"]["get_savedimages"]["path"],
                                        headers=TEST_DATAS["RESTFULAPI"]["header"], 
                                        cookies=TEST_DATAS["RESTFULAPI"]["cookie"])

 
class BasicalDatas(HttpUser):
    global TEST_DATAS
    global USER_CREDENTIALS
    sock = None
    wait_time = between(0.5, 2) 
    TEST_DATAS = read_test_datas(conf_file=TEST_CONF)
    # USER_CREDENTIALS = csv_client.csv_reader_as_json(csv_path=TEST_DATAS["ACCOUNT"]["CSV_PATH"]) 
    # import pdb
    # pdb.set_trace()
    USER_CREDENTIALS = [{'userName': ic['Brandon'], 'password':ic['e10adc3949ba59abbe56e057f20f883e'] } for ic in csv_client.csv_reader_as_json(csv_path=TEST_DATAS["ACCOUNT"]["CSV_PATH"])]
    # USER_CREDENTIALS = [{'userName': ic['userName'], 'password':ic['password'] } for ic in csv_client.csv_reader_as_json(csv_path=TEST_DATAS["ACCOUNT"]["CSV_PATH"]) if "userName" != ic['userName'] ]
    host = TEST_DATAS["ENV"]["HOST"]
    tasks = [OverviewStatus]

if __name__ == "__main__":
    pass
    # locust -f testhub/testsuites/e2e_aiarts/test_overview.py --conf testhub/testsuites/e2e_aiarts/host.conf



