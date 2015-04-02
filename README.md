# weakfilescan
动态多线程敏感信息泄露检测工具

具体使用文档，安装文档，帮助文档正在写

* 支持动态正则规则引擎
* 自动分析与目标相关的一切信息进行关联扫描

## 安装
#### CentOS 6.* 7.* Linux
安装 setuptools, pip
``` shell
wget https://bootstrap.pypa.io/ez_setup.py -O - | python
wget https://pypi.python.org/packages/source/p/pip/pip-6.0.8.tar.gz
tar zvxf pip-6.0.8.tar.gz
cd pip-6.0.8
python setup.py install
```
安装 lxml解析器
``` shell
yum install python-devel libxml2-devel libxslt-devel
pip install lxml
```
安装 beautifulsoup4
``` shell
pip install beautifulsoup4
```

### 使用
``` shell
[root@localhost weakfilescan]# python wyspider.py http://wuyun.org
--------------------------------------------------
* scan http://wuyun.org start
--------------------------------------------------
[200] http://wuyun.org => http://wuyun.org/
[200] http://wuyun.org/wuyun.tar.gz => http://wuyun.org/wuyun.tar.gz
--------------------------------------------------
* scan complete...
--------------------------------------------------
{
  "dirs": {
    "http://wuyun.org": [
      "http://wuyun.org"
    ]
  }, 
  "files": {
    "http://wuyun.org": [
      "http://wuyun.org/wuyun.tar.gz"
    ]
  }
}
```
