
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
    1. 通过HTTP接口推送原始数据集和推理脚本（具体数量、频次待定）
    2. 平台将数据写入nfs/ceph、数据库的读写性能测试（以及IOPS）
    4. 数据集、模型的增删改查的接口响应（暂定32x6个模型、数据集）
    5. 模型转换测试（暂定32x6个模型、数据集）
    6. 数据集转换测试（暂定32x6个模型、数据集）
    13. master节点在模型转换、数据集转换时IO,CPU,MEM的使用率
    14. master、A3010在满载推理业务时的网络负载，IO,CPU,MEM占用率
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
        # pdb.set_trace()
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
    def test_get_QIP(self):
        """ testcase
        1. 查看工业质检项目类型
         """
        response = self.client.request(TEST_DATAS["RESTFULAPI"]["get_QIP"]["mothed"], 
                                        url=TEST_DATAS["RESTFULAPI"]["get_QIP"]["path"],
                                        headers=TEST_DATAS["RESTFULAPI"]["header"], 
                                        cookies=TEST_DATAS["RESTFULAPI"]["cookie"]) 

    @task(1)
    def test_get_datasets_managerlist(self):
        """ testcase
        1. 查看数据集管理列表
         """
        response = self.client.request(TEST_DATAS["RESTFULAPI"]["get_datasets_managerlist"]["mothed"], 
                                        url=TEST_DATAS["RESTFULAPI"]["get_datasets_managerlist"]["path"],
                                        headers=TEST_DATAS["RESTFULAPI"]["header"], 
                                        cookies=TEST_DATAS["RESTFULAPI"]["cookie"]) 

    @task(0)
    def test_get_datasets_savelist(self):
        """ testcase
        1. 查看数据集存储列表
         """
        response = self.client.request(TEST_DATAS["RESTFULAPI"]["get_datasets_savelist"]["mothed"], 
                                        url=TEST_DATAS["RESTFULAPI"]["get_datasets_savelist"]["path"],
                                        headers=TEST_DATAS["RESTFULAPI"]["header"], 
                                        cookies=TEST_DATAS["RESTFULAPI"]["cookie"])

    @task(1)
    def test_get_project(self):
        """ testcase
        1. 查看数据集存储列表
         """
        response = self.client.request(TEST_DATAS["RESTFULAPI"]["get_project"]["mothed"], 
                                        url=TEST_DATAS["RESTFULAPI"]["get_project"]["path"],
                                        headers=TEST_DATAS["RESTFULAPI"]["header"], 
                                        cookies=TEST_DATAS["RESTFULAPI"]["cookie"])

    @task(1)
    def test_get_dataset_isPublished(self):
        """ testcase
        1. 查看数据集存储列表
         """
        response = self.client.request(TEST_DATAS["RESTFULAPI"]["get_dataset_isPublished"]["mothed"], 
                                        url=TEST_DATAS["RESTFULAPI"]["get_dataset_isPublished"]["path"],
                                        headers=TEST_DATAS["RESTFULAPI"]["header"], 
                                        cookies=TEST_DATAS["RESTFULAPI"]["cookie"])

    @task(1)
    def test_get_dataset_normal(self):
        """ testcase
        1. 查看数据集存储列表
         """
        response = self.client.request(TEST_DATAS["RESTFULAPI"]["get_dataset_normal"]["mothed"], 
                                        url=TEST_DATAS["RESTFULAPI"]["get_dataset_normal"]["path"],
                                        headers=TEST_DATAS["RESTFULAPI"]["header"], 
                                        cookies=TEST_DATAS["RESTFULAPI"]["cookie"])
    
    @task(0)
    def test_get_inferences(self):
        """ testcase
        1. 查看数据集存储列表
         """
        response = self.client.request(TEST_DATAS["RESTFULAPI"]["get_inferences"]["mothed"], 
                                        url=TEST_DATAS["RESTFULAPI"]["get_inferences"]["path"],
                                        headers=TEST_DATAS["RESTFULAPI"]["header"], 
                                        cookies=TEST_DATAS["RESTFULAPI"]["cookie"])
    
    @task(0)
    def test_get_system_settings(self):
        """ testcase
        1. 查看数据集存储列表
         """
        response = self.client.request(TEST_DATAS["RESTFULAPI"]["get_system_settings"]["mothed"], 
                                        url=TEST_DATAS["RESTFULAPI"]["get_system_settings"]["path"],
                                        headers=TEST_DATAS["RESTFULAPI"]["header"], 
                                        cookies=TEST_DATAS["RESTFULAPI"]["cookie"])
  
    @task(1)
    def test_get_currentUser(self):
        """ testcase
        1. 查看数据集存储列表
         """
        response = self.client.request(TEST_DATAS["RESTFULAPI"]["get_currentUser"]["mothed"], 
                                        url=TEST_DATAS["RESTFULAPI"]["get_currentUser"]["path"],
                                        headers=TEST_DATAS["RESTFULAPI"]["header"], 
                                        cookies=TEST_DATAS["RESTFULAPI"]["cookie"])
  
    @task(1)
    def test_get_platform_config(self):
        """ testcase
        1. 查看数据集存储列表
         """
        response = self.client.request(TEST_DATAS["RESTFULAPI"]["get_platform_config"]["mothed"], 
                                        url=TEST_DATAS["RESTFULAPI"]["get_platform_config"]["path"],
                                        headers=TEST_DATAS["RESTFULAPI"]["header"], 
                                        cookies=TEST_DATAS["RESTFULAPI"]["cookie"])
  
    @task(0)
    def test_get_jobs(self):
        """ testcase
        1. 查看数据集存储列表
         """
        response = self.client.request(TEST_DATAS["RESTFULAPI"]["get_jobs"]["mothed"], url=TEST_DATAS["RESTFULAPI"]["get_jobs"]["path"])

    @task(0)  
    def test_get_vc_usages(self):
        """ testcase
        1. 查看数据集存储列表
         """
        response = self.client.request(TEST_DATAS["RESTFULAPI"]["get_vc_usages"]["mothed"], 
                                        url=TEST_DATAS["RESTFULAPI"]["get_vc_usages"]["path"],
                                        headers=TEST_DATAS["RESTFULAPI"]["header"], 
                                        cookies=TEST_DATAS["RESTFULAPI"]["cookie"])

    @task(0) 
    def test_get_devices_usages(self):
        """ testcase
        1. 查看数据集存储列表
         """
        response = self.client.request(TEST_DATAS["RESTFULAPI"]["get_devices_usages"]["mothed"], 
                                        url=TEST_DATAS["RESTFULAPI"]["get_devices_usages"]["path"],
                                        headers=TEST_DATAS["RESTFULAPI"]["header"], 
                                        cookies=TEST_DATAS["RESTFULAPI"]["cookie"])

 
class BasicalDatas(HttpUser):
    global TEST_DATAS
    global USER_CREDENTIALS
    sock = None
    wait_time = between(0.5, 2) 
    TEST_DATAS = read_test_datas(conf_file=TEST_CONF)
    USER_CREDENTIALS = [{'userName': ic['userName'], 'password':ic['password'] } for ic in csv_client.csv_reader_as_json(csv_path=TEST_DATAS["ACCOUNT"]["CSV_PATH"]) if "userName" != ic['userName'] ]
    host = TEST_DATAS["ENV"]["HOST"]
    tasks = [OverviewStatus]

if __name__ == "__main__":
    pass
    # locust -f testhub/testsuites/songshanhu/test_overview.py --conf testhub/testsuites/songshanhu/host.conf



