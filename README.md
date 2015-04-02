# weakfilescan
动态多线程敏感信息泄露检测工具

具体使用文档，安装文档，帮助文档正在写

* 支持动态正则规则引擎
* 自动分析与目标相关的一切信息进行关联扫描

### 安装
CentOS 6.* 7.* Linux
* install setuptools, pip
``` shell
wget https://bootstrap.pypa.io/ez_setup.py -O - | python

wget https://pypi.python.org/packages/source/p/pip/pip-6.0.8.tar.gz
tar zvxf pip-6.0.8.tar.gz
cd pip-6.0.8
python setup.py install
```
* install lxml解析器
``` shell
yum install python-devel libxml2-devel libxslt-devel
pip install lxml
```
* install beautifulsoup4
``` shell
pip install beautifulsoup4
```

### 使用
``` bash
python wyspider.py http://wuyun.org
```
