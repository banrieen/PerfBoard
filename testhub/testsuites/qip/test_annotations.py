
""" 测试单（场景）

松山湖AI制造业推理平台性能测试SLI/SLO

    1. 通过HTTP接口推送原始数据集和推理脚本（具体数量、频次待定）
    2. 平台将数据写入nfs/ceph、数据库的读写性能测试（以及IOPS）
    3. 100批量数据标注、图像预览响应测试
    4. 数据集、模型的增删改查的接口响应（暂定32x6个模型、数据集）
    5. 模型转换测试（暂定32x6个模型、数据集）
    6. 数据集转换测试（暂定32x6个模型、数据集）
    7. 10x32x6个分布式推理任务调度的稳定性
    8. 64mpbs，128Mbps图片流量的负载测试
    9. 测试（客户）环境rabbitmq的吞吐量和响应延时
    10. 1000次/s的HTTP推理请求失败率
    11. 1000次/s的HTTP推理结果请求失败率（上传到平台数据库）
    12. 1/1000不良率的告警响应测试
    13. master节点在模型转换、数据集转换时IO,CPU,MEM的使用率
    14. master、A3010在满载推理业务时的网络负载，IO,CPU,MEM占用率

# ScriptType：performance test 
# UpdateDate: 2021.03-4
# Matainer: thomas
# Env: Win10 64bit, python3.8
 """


from locust import HttpUser, TaskSet, task, between
from locust.contrib.fasthttp import FastHttpUser
from locust import events
from locust.clients import HttpSession
from credentials import *
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
DATA_PREFIX = "songshanhu"
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


class Datasets(TaskSet):
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
    userName = "NOT_FOUND"
    password = "NOT_FOUND"

    def on_start(self):
        print("======================= A new test is starting, user will login {} ! =======================".format(TEST_DATAS["ENV"]["HOST"]))
        self.client.request("get",TEST_DATAS["RESTFULAPI"]["homepage"])
        self.client.header = TEST_DATAS["RESTFULAPI"]["header"]
        self.email, self.password = USER_CREDENTIALS.pop()
        aaccount={"userName":self.email,"password":self.password}
        response = self.client.request("post", url=TEST_DATAS["RESTFULAPI"]["login"]["path"], data=data)
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
        # self.admin_client = HttpSession(base_url=self.client.base_url)
        # self.admin_client.delete( TEST_DATAS["RESTFULAPI"]["login"]["path"]) # , auth=(self.adminUserName, self.adminUserName)


    @task(10)
    def test_create_project(self):
        """ testcase
        1. 注册新用户
         """
        user_filename = "".join([DATA_PREFIX,"_","fake_user.csv"])
        user_datas = fake_users.new_user()
        print("======================= test_create_user DATAS: {} ".format(user_datas))
        print("======================= test_create_user HEADER: {}".format(self.client.header))
        print("======================= test_create_user COOKIES: {} ".format(TEST_DATAS["RESTFULAPI"]["cookie"]))
        self.client.request("post", url=TEST_DATAS["RESTFULAPI"]["create_user"]["path"], 
                                                headers=TEST_DATAS["RESTFULAPI"]["header"], 
                                                json=user_datas, 
                                                cookies=TEST_DATAS["RESTFULAPI"]["cookie"]) 

    @task(2)
    def test_create_dataset(self):
        """ testcases
        2. 注册新用户组
         """
        group_filename = "".join([DATA_PREFIX,"_","fake_group.csv"])
        group_datas = fake_users.new_group()
        self.client.request("post",url=TEST_DATAS["RESTFULAPI"]["create_group"]["path"], 
                            headers=TEST_DATAS["RESTFULAPI"]["header"], 
                            json=group_datas)
 
class BasicalDatas(HttpUser):
    global TEST_DATAS
    global USER_CREDENTIALS
    sock = None
    wait_time = between(0.5, 2) 
    TEST_DATAS = read_test_datas(conf_file=TEST_CONF)
    USER_CREDENTIALS = [{'userName': ic['userName'], 'password':ic['password'] } for ic in csv_reader_as_json(csv_path=TEST_DATAS["ENV"]["CSV_PATH"]) if "userName" != ic['userName'] ]
    host = TEST_DATAS["ENV"]["HOST"]
    tasks = [Datasets]

if __name__ == "__main__":
    global DATA_PREFIX
    DATA_PREFIX = "songshanhu"
    # locust -f ./testsuite/songshanhu/inference_perf.py --conf ./testsuite/songshanhu/songshanhu.conf



