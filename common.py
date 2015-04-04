# encoding: utf-8
# 全局函数文件
# email: ringzero@0x557.org

from config import *
import re
import urlparse
import threading
from bs4 import BeautifulSoup
from libs.tldextract import extract, TLDExtract
import libs.requests as requests
import libs.requests as __requests__
from libs.FuzzUrlGenerator import UrlGenerator
from libs.UrlSplitParser import UrlSplitParser

if allow_http_session:
	requests = requests.Session()

def get_basedomain(url):
	try:
		if basedomain == 1:
			return urlparse.urlparse(url).netloc
		elif basedomain == 2:
			return extract(url).registered_domain
		elif basedomain == 3:
			return extract(url).domain # 更加有关联性的处理方法
	except Exception, e:
		pass

def get_baseurl(link):
	netloc = urlparse.urlparse(link).netloc
	if netloc:
		split_url = link.split(netloc)
		baseurl = '%s%s' % (split_url[0], netloc)
		return baseurl

def http_request_get(url, body_content_workflow=False, allow_redirects=allow_redirects):
	try:
		result = requests.get(url, 
			stream=body_content_workflow, 
			headers=headers, 
			timeout=timeout, 
			proxies=proxies,
			allow_redirects=allow_redirects,
			verify=allow_ssl_verify)
		return result
	except Exception, e:
		# 返回空的requests结果对象
		return __requests__.models.Response()

def http_request_post(url, payload, body_content_workflow=False, allow_redirects=allow_redirects):
	"""
		payload = {'key1': 'value1', 'key2': 'value2'}
	"""
	try:
		result = requests.post(url, 
			data=payload, 
			headers=headers, 
			stream=body_content_workflow, 
			timeout=timeout, 
			proxies=proxies,
			allow_redirects=allow_redirects,
			verify=allow_ssl_verify)
		return result
	except Exception, e:
		# 返回空的requests结果对象
		return __requests__.models.Response()

def checksite_isalive(siteurl):
	result = http_request_get(siteurl, allow_redirects=False)
	if result.status_code: # 存在状态码
		return True
	else:
		return False

def checksite_possibility(siteurl): # 检查可能性
    temp_weburls = [
        '/ea63a430b109194d/',
        '/ea63a430b109194d1/',
        '/ea63a430b109194d.'+default_extion,
        '/ea63a430b109194d1.'+default_extion,
    ]

    req_result = {}
    for tempurl in temp_weburls:
        httpres = http_request_get(siteurl.rstrip('/')+tempurl)
        is_redirect = True if len(httpres.history) > 0 else False
        req_result[tempurl] = {
            'status_code' : httpres.status_code,
            'is_redirect' : is_redirect,
            'text' : httpres.text,
            'history' : httpres.history,
            'request' : httpres.url,
            'text_size' : len(httpres.text),
        }

    possibility = 100
    refer_to_val = 0
    regex = re.compile(page_not_found_reg)

    dir1 = temp_weburls[0]
    dir2 = temp_weburls[1]
    file1 = temp_weburls[2]
    file2 = temp_weburls[3]

    # 分析状态判断结果
    if req_result[dir1]['status_code'] != 404 and req_result[dir2]['status_code'] != 404:
        possibility -= 10 # print '返回状态不等于404'
        if not regex.findall(req_result[dir1]['text']) and not regex.findall(req_result[file1]['text']):
            possibility -= 10 # print '文件和目录错误页面都没有状态标示'
        else:
            refer_to_val += 50 # print '有特征码可参考'
        if req_result[dir1]['text_size'] != req_result[dir2]['text_size']:
            possibility -= 10 # print '返回的结果大小不一样'
        if dir1 in req_result[dir1]['text'] and file1 in req_result[file1]['text']:
            possibility -= 10 # 请求的文件名存在于返回内容当中

    if req_result[dir1]['request'] == req_result[dir2]['request']:
        possibility -= 10 # 返回的请求url结果一样

    if req_result[file1]['status_code'] != 404 and req_result[file2]['status_code'] != 404:
        possibility -= 10 # print '返回状态不等于404'
        if not regex.findall(req_result[dir1]['text']) and not regex.findall(req_result[file1]['text']):
            possibility -= 10 # print '文件和目录错误页面都没有状态标示'
        else:
            refer_to_val += 50 # print '有特征码可参考'
        if req_result[file1]['text_size'] != req_result[file2]['text_size']:
            possibility -= 10 # print '返回的结果大小不一样'
        if dir1 in req_result[dir1]['text'] and file1 in req_result[file1]['text']:
            possibility -= 10 # 请求的文件名存在于返回内容当中

    if req_result[file1]['request'] == req_result[file2]['request']:
        possibility -= 10 # 返回的请求url结果一样

    if refer_to_val < 50 and possibility < 65:
        return {'considered':False, 'possibility':possibility, 'refer_to_val':refer_to_val}
    else:
        return {'considered':True, 'possibility':possibility, 'refer_to_val':refer_to_val}

def get_segments(url):
	url_webdirs = []
	parser_obj = UrlSplitParser(urlparse.urlparse(url))
	for segment in parser_obj.get_paths()['segment']:
		url_webdirs.append(parser_obj.baseurl + segment)
	return url_webdirs

def get_first_segment(url):
	pathobj = urlparse.urlparse(url)
	path = pathobj.path.replace('//','/')
	if len(path.split('/')) < 3:
		return '/'
		# return pathobj.scheme+'://'+pathobj.netloc+'/'
	else:
		segment = path.split('/')[1]
		return '/'+segment+'/'
		# return pathobj.scheme+'://'+pathobj.netloc+'/'+segment+'/'

class LinksParser(object):
	"""docstring for link_parser"""
	def __init__(self, html_content):
		super(LinksParser, self).__init__()
		self.html_content = html_content
		self.url_links = {
			'a':[],
			'link':[],
			'img':[],
			'script':[]
		}
		self.url = self.html_content.url
		self.baseurl = get_baseurl(self.url)
		self.soup = BeautifulSoup(self.html_content.text, 'lxml')

	def complet_url(self, link):
		if link.startswith('/') or link.startswith('.'):
			return urlparse.urljoin(self.baseurl, link)
		elif link.startswith('http') or link.startswith('https'):
			return link
		elif link.startswith('#'): # 为了兼容某些变态的URI模式
			return urlparse.urljoin(self.url, link)
		else:
			return False

	def getall(self):
		self.get_tag_a()
		self.get_tag_link()
		self.get_tag_img()
		self.get_tag_script()
		# links 去重
		for child in self.url_links.keys():
			self.url_links[child] = list(set(self.url_links[child]))
		return {self.url : self.url_links}

	def get_tag_a(self):
		# 处理A链接
		for tag in self.soup.find_all('a'):
			if tag.attrs.has_key('href'):
				link = tag.attrs['href']
				# link = urlparse.urldefrag(tag.attrs['href'])[0] # 处理掉#tag标签信息
				complet_link = self.complet_url(link.strip())
				if complet_link:
					self.url_links['a'].append(complet_link)
		return self.url_links

	def get_tag_link(self):
		# 处理link链接资源
		for tag in self.soup.find_all('link'):
			if tag.attrs.has_key('href'):
				link = tag.attrs['href']
				complet_link = self.complet_url(link.strip())
				if complet_link:
					self.url_links['link'].append(complet_link)
		return self.url_links

	def get_tag_img(self):
		# 处理img链接资源
		for tag in self.soup.find_all('img'):
			if tag.attrs.has_key('src'):
				link = tag.attrs['src']
				complet_link = self.complet_url(link.strip())
				if complet_link:
					self.url_links['img'].append(complet_link)
		return self.url_links

	def get_tag_script(self):
		# 处理script链接资源
		for tag in self.soup.find_all('script'):
			if tag.attrs.has_key('src'):
				link = tag.attrs['src']
				complet_link = self.complet_url(link.strip())
				if complet_link:
					self.url_links['script'].append(complet_link)
		return self.url_links



