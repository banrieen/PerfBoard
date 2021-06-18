
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


class InferencePerf(TaskSet):
    """ 推理压力testsuite
    10. 1000次/s的HTTP推理请求失败率
    11. 1000次/s的HTTP推理结果请求失败率（上传到平台数据库）
    12. 1/1000不良率的告警响应测试
    """
    global TEST_DATAS
    @events.test_start.add_listener
    def on_test_start_get_homepage(self, environment, **kwargs):
        print("A new test is starting, user will login")
        # pdb.set_trace()
        # print("+++++++++++++++++++++++", TEST_DATAS["RESTFULAPI"]["homepage"])
        self.client.get(TEST_DATAS["RESTFULAPI"]["Homepage"])

    @events.test_stop.add_listener
    def on_test_stop_logout(self, environment, **kwargs):
        print("A  test is ending, user will logout !")
        responses = self.client.get(url=TEST_DATAS["RESTFULAPI"]["Logout"]["path"])
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
        responses = self.client.post(url=TEST_DATAS["RESTFULAPI"]["Login"]["path"], headers=TEST_DATAS["RESTFULAPI"]["header"], data=TEST_DATAS["RESTFULAPI"]["admin"])
        if responses.status_code == 200:
            rst = json.loads(responses.text, strict=False)
            if rst['success'] == '200':
                responses.success() 
                user_token =  rst['token']
            else:
                responses.failure('code：%s ErrorMsg：%s' % (rst['code'], rst['errorMsg']))
        else:
            responses.failure('status_code：%s' % responses.status_code)


    @task
    def test_post_inference(self):
        """ testcase 
        1000次/s的HTTP推理请求失败率
         """
        self.user_token = ""
        responses = self.client.post(url=TEST_DATAS["RESTFULAPI"]["PostInferenceJob"]["path"], headers=TEST_DATAS["RESTFULAPI"]["header"], data=TEST_DATAS["RESTFULAPI"]["admin"])
        if responses.status_code == 200:
            rst = json.loads(responses.text, strict=False)
            if rst['success'] == '200':
                responses.success() 
                user_token =  rst['token']
            else:
                responses.failure('code：%s ErrorMsg：%s' % (rst['code'], rst['errorMsg']))
        else:
            responses.failure('status_code：%s' % responses.status_code)

    @task
    def test_post_result(self):
        """ testcase 
        1000次/s的HTTP推理结果请求失败率
         """
        self.user_token = ""
        responses = self.client.post(url=TEST_DATAS["RESTFULAPI"]["PostInferenceResult"]["path"], headers=TEST_DATAS["RESTFULAPI"]["header"], data=TEST_DATAS["RESTFULAPI"]["admin"])
        if responses.status_code == 200:
            rst = json.loads(responses.text, strict=False)
            if rst['success'] == '200':
                responses.success() 
                user_token =  rst['token']
            else:
                responses.failure('code：%s ErrorMsg：%s' % (rst['code'], rst['errorMsg']))
        else:
            responses.failure('status_code：%s' % responses.status_code)

    @task
    def test_post_alert(self):
        """ testcase 
        1/1000不良率的告警响应测试
         """
        self.user_token = ""
        responses = self.client.post(url=TEST_DATAS["RESTFULAPI"]["alert"]["path"], headers=TEST_DATAS["RESTFULAPI"]["header"], data=TEST_DATAS["RESTFULAPI"]["admin"])
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
    task_set = InferencePerf
    wait_time = between(0.5, 5)  # 等待时间,单位为s，任务执行间隔时间
    TEST_DATAS = read_test_datas(conf_file=TEST_CONF)
    # pdb.set_trace()
    # print("+++++++++++++++++++++++", TEST_DATAS["RESTFULAPI"]["homepage"])


if __name__ == "__main__":
    cmd = 'locust -f locust_demo.py'
    os.system(cmd)
    # locust -f ./testsuite/songshanhu/inference_perf.py --conf ./testsuite/songshanhu/songshanhu.conf


""" api example
接口描述： （1）
接口：http post, http://10.101.xxx.xxx:port/json
（2）payload，json格式：
设备ID：MachineId	//工控机ID产品编码：
ProductCode	//当前生产的产品编码（330暂不解析）
数据库表名：TableName	//线体
项目名称：ProjectName	//工位
任务名称：TaskName		//工序
OK/NG标记：Flag		//推理结果
图像名：ImageName		//图像名
图像数据：ImageRawData	//图像数据
任务类型：TaskType		//任务类型：检测、分类…
label集合：Labels		//推理标签	
数据生成时间：GenerateDateTime//生成时间
版本：Version		//接口版本

 """
