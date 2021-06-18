<p align="center">
<img src="docs/static/ico.png" width="150"/>
</p>

MachineWolf 已经转移到 MachineDevil[https://github.com/banrieen/MachineDevil]， 请注意！ 

-----------

[English Doc](README.md) | [简体中文](README_zh_CN.md)

**MachineWolf** 是一个自动化测试性能套件。

### 快速使用指导

* 在docker环境中执行testsuites

    1. 拉取已经编译好的镜像
    
        `docker pull banrieen/machinewolf`

    2. 执行docker
    
        如果找不到测试脚本，可以使用快捷键"Ctrl+K Crtl+O"打开`/home/MachineWolf`
        ```bash
        docker run -d  -p 8088:8080  -p 8090:8090   --name "machinewolf"  -v "${PWD}:/home/MachineWolf"  --env NOTEBOOK_ARGS="--NotebookApp.notebook_dir=/home/MachineWolf"  --shm-size 2048m  --restart always   banrieen/machinewolf:latest
        # Open web IDE VS Code
        # http://<xxx.xxx.xxx.xxx>:8088/tools/vscode/
        ```

    3. 查看和调试测试脚本
    
        ![create-teatcases](docs/static/createtestcase.png)

* 在本地执行测试脚本

    ```bash
    sudo chmod +x init_dev.sh
    bash ./init_dev.sh
    locust -f ./example/locust/test_http.py --conf ./example/locust/host.conf
    ```

* 使用taurus执行locust脚本

    `bzt example/taurus/quick_test.yml`

* 使用taurus执行jmeter脚本

    `bzt example/jmeter/trace_user_footprint.jmx`

* 使用taurus执行纯yaml脚本

    `bzt example/taurus/quick_test.yml`

* 使用pytest执行非接口类的脚本，比如ha,吞吐量测试集等

    `pytest example/pytest/test_ha.py`

**测试报告示例**

![locust-http-response](docs/static/locust_report.png)

**CLI看板示例**

![taurus-status](docs/static/taurus_report.png)

**导出测试报告**

* `testreport/result.csv_stats.csv`
* `testreport/result.csv_stats_history.csv`
* `testreport/result.csv_failures.csv`
* `testreport/result.csv_exceptions.csv`

### 测试集结构

测试套件本着兼容并蓄，容纳萃取的宗旨，独立灵活的组织测试套件。支持各种前沿的、优秀的工具和理念；目前将测试方案（testscheme）、数据(datas.yaml)、脚本(.py,.jmx)、执行计划（host.yml,taurus.yml）灵活的组织在一起。
目前还是一些样例，还需要完善和补充。

``` direction
|-- testhub/
    `-- testscheme
        |-- manufacturing
        |-- annotations
    `-- testsuites
        |-- annotations
            |-- host.conf
            |-- test_cvat_suites.py
            |-- datas.yaml
        |-- dlws
        |-- e2e
        |-- ha
        |-- jobmanager
        |-- qip
    `-- testlib
        |-- fake_users
        |-- postgres_client
        |-- csv_client
```

### 安全性

为避免信息暴漏，无效信息泛滥。

* 所有测试脚本，说明文本和配置文件中去除一切ID, ACCOUNT, HOST信息
* 不保留任何测试环境信息，和任何测试数据
* 使用规范的标识替换敏感信息：

    + 账号： `<HOSTNAME>:<PASSWORLD>`
    + 主机： `<HOST>:<PORT>`
    + 链接： `<LINKTYPE>:<LINKADDRESS>`
    + 证书： `<KEYGEN> 或 <TOKEN>`
    + 邮件： `<EMAIL-NAME@EMAIL-SERVICE.COM>`

