# weakfilescan
动态多线程敏感信息泄露检测工具

* 支持动态正则规则引擎
* 自动分析与目标相关的一切信息进行关联扫描

## 字典支持规则
#### 规则使用简介
* DATE (日期类型)
``` python
{date=类型#长度$step:开始-结束}$
{date=year:2010-2015}$ # 年
[2010,2011,2012,2013,2014,2015]
```
* INT (整数)
```
{int=类型#长度$step:开始-结束}$
```
* STR (字符类型)
```
{str=类型#长度$step:开始-结束}$
```
* RE (正则引擎)
> {re=引擎名称:正则表达式}$
``` python
{re=exrex:[0-9]}$
[0,1,2,3,4,5,6,7,8,9]
{re=exrex:(a|A)dmin[0-9]}$
[u'admin0',u'admin1',u'admin2',u'admin3',u'admin4',u'admin5',u'admin6',u'admin7',u'admin8',u'admin9',
 u'Admin0',u'Admin1',u'Admin2',u'Admin3',u'Admin4',u'Admin5',u'Admin6',u'Admin7',u'Admin8',u'Admin9']
```


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
安装 lxml解析器 & beautifulsoup4
``` shell
yum install python-devel libxml2-devel libxslt-devel
pip install lxml beautifulsoup4
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
