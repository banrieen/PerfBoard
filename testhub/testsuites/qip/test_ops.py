
""" 测试单（场景）

松山湖AI制造业推理平台性能测试SLI/SLO
# ScriptType：performance test 
# UpdateDate: 2021.03-4
# Matainer: thomas
# Env: Win10 64bit, python3.8
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
    # 读取配置文件中的datasets, modelsets
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


class EnduranceStress(TaskSet):
    """ 业务（负载）稳定性testsuite
    3. 100批量数据标注、图像预览响应测试
    7. 10x32x6个分布式推理任务调度的稳定性
    8. 64mpbs，128Mbps图片流量的负载测试
    9. 测试（客户）环境rabbitmq的吞吐量和响应延时
    """
    
    @events.test_start.add_listener
    def on_test_start_get_homepage(self, environment, **kwargs):
        print("A new test is starting, user will login")
        # pdb.set_trace()
        # print("+++++++++++++++++++++++", TEST_DATAS["RESTFULAPI"]["homepage"])
        self.client.get(TEST_DATAS["RESTFULAPI"]["homepage"])

    @events.test_stop.add_listener
    def on_test_stop_logout(self, environment, **kwargs):
        print("A  test is ending, user will logout !")
        responses = self.client.get(url=TEST_DATAS["RESTFULAPI"]["logout"]["path"])
        if responses.status_code == 200:
            rst = json.loads(responses.text, strict=False)
            if rst['success'] == '200':
                responses.success() 
    @task
    def test_userlogin(self):
        """ testcase 
        10 ~ 100 用户登录
         """
        self.user_token = ""
        responses = self.client.post(url=TEST_DATAS["RESTFULAPI"]["login"]["path"], headers=TEST_DATAS["RESTFULAPI"]["header"], data=TEST_DATAS["RESTFULAPI"]["admin"])
        if responses.status_code == 200:
            rst = json.loads(responses.text, strict=False)
            if rst['success'] == '200':
                responses.success() 
                user_token =  rst['token']
            else:
                responses.failure('code：%s ErrorMsg：%s' % (rst['code'], rst['errorMsg']))
        else:
            responses.failure('status_code：%s' % responses.status_code)



class WebsiteUser(FastHttpUser):
    global TEST_DATAS 
    task_set = EnduranceStress
    wait_time = between(0.5, 5)  # 等待时间,单位为s，任务执行间隔时间
    TEST_DATAS = read_test_datas(conf_file=TEST_CONF)
    # pdb.set_trace()
    # print("+++++++++++++++++++++++", TEST_DATAS["RESTFULAPI"]["homepage"])


if __name__ == "__main__":
    cmd = 'locust -f locust_demo.py'
    os.system(cmd)
    # locust -f ./testsuite/songshanhu/inference_perf.py --conf ./testsuite/songshanhu/songshanhu.conf



