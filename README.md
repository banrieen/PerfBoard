<p align="center">
<img src="docs/static/ico.png" width="150"/>
</p>

-----------


[English Doc](README.md) | [简体中文](README_zh_CN.md)

**MachineWolf** is a Test Studio for AI 、Deep Learning or Machine Learning framwork、platform. As the Best-Practice about AIops  or MLOps.

🍃 🍂 🍁 🍄 🐚 🍀 🌾 💐 🌷🦥 🐁 🐀 🐿 🦔 🐾 🐉 🐲 🌵 🎄 🌲 🌳 🌴 🌱

**😄 If it’s helpful to you, please click a Star, it is greatly appreciated!🍻 🥂💕 💞 💓**

🌼 🌻 🌞 🌝 🌛🌈 ☀️ 🌤 ⛅️ 🌥🌏 🪐 💫 ⭐️ 🌟 ✨ 🍐 🍊 🍋 🍌 🍉 🍇 🍓

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

### About branch


| Branch name |Info|
| ----------- | -------------------------------------------------------------------- |
| Master      | The master branch maintains the latest release code of the released product, merges from Release or Feature to the official release history|
| Feature     | Opened from the Master branch, it is mainly used to develop new features or special test sets, which are maintained according to the responsible module; the naming convention is: feature/#..., each function should correspond to an issue,...is an issue number. |
| Hotfix      |	Opened from the Master branch, it is mainly used to fix known bugs in the currently released version; please refer to Bugfix for precautions when solving bugs. The naming convention is：hotfix/#... |
| Release	  | It is opened from the Master branch and is mainly used to release the version. Once the Master branch has enough functions to do a release (or the scheduled release day), fork a release branch from the Master branch. The newly created branch is used to start the release cycle. This branch should only be used for bug fixes, document generation, and other release-oriented tasks. Once the external release work is completed, perform the following three operations: merge the Release branch to the Master; tag the Master with the corresponding version; Release returns, and these changes since the new release branch must be merged back into the Master branch. The naming convention is：release/...，...as release No.|
| ngihtly     | Build every night to verify the examples and public libraries of the test suite to ensure that the relevant scripts are available.|

> [!IMPORTANT]
> Master tag To test the version number of the code base itself
> Releas tag Sync with the release/-x-tag of the product to be tested; if the tested product is 2.0.0-rc1, you can pull out a release/2.0.0-rc1
> Hotfix tag Same as the hostfix of the tested product, a hotfix can be pulled out during the test/#window stuck
> Feature tag Independently developed and researched feature prototype verification can pull a feature such as feature/#requirement or bug

* System testing and iterative testing can directly pull the latest code (tag) of the Master branch
* All Feature, Hotfix, and Release that have been debugged and verified must be merged into the Master


### About testsuites

* aisetshub:    About Model validation
* datasetshub:  About Data set validation
* testhub:      Platform, component test cases and scripts
* issuesboard:  Synchronize issues and reports

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

### Documents 

For more detailed information about installation guides, tutorials and APIs, please refer to[Docs](docs/zh_CN)

### Release

* **Latest**

    1. Complete package architecture
    2. Installation and environmental preparation
    3. Implementation example
    4. Basic test case set

* **Planning**

    1. Supplement and improve the test script
    2. Tuning the synchronization process between ZenTao and the test suite Tuning the synchronization process between ZenTao and the test suite
    3. Debug the synchronization process between argo and test suite
    4. Supplemental framework, model performance tools and scripts
    5. Integrate monitoring in k8s

**Please refer to the release notes for details[RELEASE](./RELEASE.md)。**

### License

[MIT](LICENSE)

### Comunity

Welcome everyone to mention questions and suggestions to github issues

* [Gitter Discussion group](https://gitter.im/banrieen/MachineWolfHome?utm_source=share-link&utm_medium=link&utm_campaign=share-link)
* [#Machinewolf tag on StackOverflow](https://stackoverflow.com/search?q=%23Machinewolf)
* Twitter @MachinWolf
* QQ group 868444294 
