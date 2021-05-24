<p align="center">
<img src="docs/static/ico.png" width="150"/>
</p>


MachineWolf is transferred to the new project **[MachineDevil](https://github.com/banrieen/MachineDevil) project., Please goto and view**


-----------

**MachineWolf** is a Test Studio for AI 、Deep Learning or Machine Learning framwork、platform.

### Quickly Start

* Runing script at local PC

    ```bash
    sudo chmod +x init_dev.sh
    bash ./init_dev.sh
    locust -f ./example/locust/test_http.py --conf ./example/locust/host.conf
    ```

* Execute testsuites in docker container

    1. Pull the images from docker-hub
    
    `docker pull banrieen/machinewolf`

    2. Start container
    
    ```bash
    docker run -d     -p 8088:8080  -p 8090:8090     --name "ml-workspace"  -v "${PWD}:/workspace"  --env NOTEBOOK_ARGS="--NotebookApp.notebook_dir=/home"  --shm-size 2048m  --restart always     banrieen/machinewolf:latest
    # Open web IDE
    # http://<xxx.xxx.xxx.xxx>:8088 
    ```

* Running locust scripts by taurus

    `bzt example/taurus/quick_test.yml`

* Running jmeter scripts by taurus

    `bzt example/jmeter/trace_user_footprint.jmx`

* Running yaml scripts by taurus 

    `bzt example/taurus/quick_test.yml`

* Runing pytest testsuites, such as non-api， HA， throughput test scripts

    `pytest example/pytest/test_ha.py`

**Example of testreport**

![locust-http-response](docs/static/locust_report.png)

**CLI dashboard**

![taurus-status](docs/static/taurus_report.png)

**Export testreport**

* `testreport/result.csv_stats.csv`
* `testreport/result.csv_stats_history.csv`
* `testreport/result.csv_failures.csv`
* `testreport/result.csv_exceptions.csv`


### Schema of test studio

The test suite is an independent and flexible organization test suite based on the purpose of being inclusive and accommodating extraction. Support a variety of cutting-edge and excellent tools and concepts; currently test schemes (testscheme), data (datas.yaml), scripts (.py, .jmx), and execution plans (host.yml, taurus.yml) are organized flexibly Together.
There are still some examples that need to be improved and supplemented.

``` direction
|-- testhub/
    `-- testscheme
        |-- 5g_manufacturing
        |-- annotations_cvat
    `-- testsuites
        |-- annotations_cvat
            |-- host.conf
            |-- test_cvat_suites.py
            |-- datas.yaml
        |-- dlws
        |-- e2e_aiarts
        |-- ha_aiarts
        |-- jobmanager
        |-- songshanhu
    `-- testlib
        |-- fake_users
        |-- postgres_client
        |-- csv_client
```

### Security

In order to avoid information leaks, invalid information floods.

* All test scripts, explanatory text and configuration files remove all ID, ACCOUNT, HOST information
* Does not retain any test environment information, and any test data
* Replace sensitive information with canonical logos：

    + account： `<HOSTNAME>:<PASSWORLD>`
    + host： `<HOST>:<PORT>`
    + link： `<LINKTYPE>:<LINKADDRESS>`
    + cert： `<KEYGEN> 或 <TOKEN>`
    + email： `<EMAIL-NAME@EMAIL-SERVICE.COM>`


**Please refer to the release notes for details[RELEASE](./RELEASE.md)。**

### License

[MIT](LICENSE)

### Comunity


