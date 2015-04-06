# weakfilescan
基于爬虫，动态收集扫描目标相关信息后进行二次整理形成字典规则，利用动态规则的多线程敏感信息泄露检测工具，支持多种个性化定制选项，包括：
* 规则字典多样化定义（支持正则、整数、字符、日期）
* 扫描域名策略（域名全称、主域名、域名的名字）
* 自定义HTTP状态码
* 支持动态配置HTTP脚本扩展名
* 自定义判断文件是否存在正则
* 返回结果集误报清洗选项
* HTTPS服务器证书校验
* 线程数定义
* HTTP请求超时时间
* 是否允许URL重定向
* 是否开启Session支持，在发出的所有请求之间保持cookies
* 是否允许随机User-Agent
* 是否允许随机X-Forwarded-For
* 动态代理列表配置（支持TOR）
* HTTP头自定义

更多使用详情参照 [/config.py](https://github.com/ring04h/weakfilescan/blob/master/config.py)

# 快速开始
``` shell
python wyspider.py http://wuyun.org php
```

# 字典支持规则
## 规则使用简介
在字典中使用规则引擎，必须以 **{** 括号开头，并以 **}$** 结尾，类型后面跟的 **#** 代表生成数据的长度，**$** 代表单步值，开始-结束，数据的起始区间设置。
```
{规则=类型#长度$step:开始-结束}$
```
| 规则      |    说明 |
| :-------- |:--------|
| re   | 正则引擎 |
| int  | 整数 |
| str  | 字符 |
| date | 日期 |

正则引擎类型
------------
使用实例
{re=引擎名称:正则表达式}$
``` python
{re=exrex:[0-9]}$
[u'0', u'1', u'2', u'3', u'4', u'5', u'6', u'7', u'8', u'9']
{re=exrex:[aA]dmin[1-5]}$
[u'admin1', u'admin2', u'admin3', u'admin4', u'admin5', u'Admin1', u'Admin2', u'Admin3', u'Admin4', u'Admin5']
```

整数类规则
------------
| 类型      | 使用实例 |
| :-------- |:--------|
| 顺序递进 处理step | {int=series$单步值:开始数字-结束数字}$ |
``` python
{int=series$2:0-10}$
[0, 2, 4, 6, 8, 10]
```

| 类型      | 使用实例 |
| :-------- |:--------|
| 连号数字 | {int=digits#长度:开始数字-结束数字}$ |
``` python
{int=digits#3:0-9}$
[123, 234, 345, 456, 567, 678, 789]
```

| 类型      | 使用实例 |
| :-------- |:--------|
| 重叠数字 | {int=overlap#长度:开始数字-结束数字}$ |
``` python
{int=overlap#4:0-9}$ 
[1111, 2222, 3333, 4444, 5555, 6666, 7777, 8888, 9999]
```

字符类规则
------------
| 类型      | 使用实例 |
| :-------- |:--------|
| 顺序递进 处理step | {str=letters#长度:开始字符-结束字符}$ |
``` python
{str=letters#3:a-g}$
['abc', 'bcd', 'cde', 'def', 'efg']
```

| 类型      | 使用实例 |
| :-------- |:--------|
| 重叠字母 | {str=overlap#长度:开始字符-结束字符}$ |
``` python
{str=overlap#4:a-g}$
['aaaa', 'bbbb', 'cccc', 'dddd', 'eeee', 'ffff', 'gggg']
```

日期类规则
------------
| 类型      | 使用实例 |
| :-------- |:--------|
| 年 | {date=year:开始年份-结束年份}$ |
``` python
{date=year:2010-2015}$
[2010, 2011, 2012, 2013, 2014, 2015]
```

| 类型      | 使用实例 |
| :-------- |:--------|
| 月 | {date=mon:开始月份-结束月份}$ |
``` python
{date=mon:01-12}$
[1, 01, 2, 02, 3, 03, ‘...’, 9, 09]
```

| 类型      | 使用实例 |
| :-------- |:--------|
| 日 | {date=day:开始日-结束日}$ |
``` python
{date=day:01-31}$
[1, 01, 2, 02, 3, 03, 4, 04, 5, 05, ‘...’, 31]
```

| 类型      | 使用实例 |
| :-------- |:--------|
| 年月 | {date=year_mon:开始年月-结束年月}$ |
``` python
{date=year_mon:201501-201504}$
[201501, 20151, 201502, 20152, ‘...’, 201504]
```

| 类型      | 使用实例 |
| :-------- |:--------|
| 月日 | {date=mon_day:开始月日-结束月日}$ |
``` python
{date=mon_day:0501-0531}$
[0501, 51, 0502, 52, 0506, 56, 0511, 511, ‘...’, 0530,530]
```

| 类型      | 使用实例 |
| :-------- |:--------|
| 年月日 | {date=year_mon_day:开始年月日-结束年月日}$ |
``` python
{date=year_mon_day:20150101-20150401}$
[20150101, 201511, 20150112, 2015112, ‘...’, 20150401]
```

| 类型      | 使用实例 |
| :-------- |:--------|
| 月日年 | {date=mon_day_year:开始月日年-结束月日年}$ |
``` python
{date=mon_day_year:01012015-04012015}$
[01012015, 112015, 01122015, 1122015, ‘...’, 04012015]
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