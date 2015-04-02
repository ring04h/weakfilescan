# encoding: utf-8
# URL处理对象
# email: ringzero@0x557.org

import sys
sys.path.append("../")
from config import *
import urlparse
from tldextract import extract, TLDExtract

class UrlSplitParser(object):
	"""docstring for UrlSplitParser
		碎片化信息处理并集，生成其因变量组 [dependents]
	"""
	def __init__(self, urlobj, extion=default_extion):
		super(UrlSplitParser, self).__init__()
		self.url = urlobj.geturl()
		self.scheme = urlobj.scheme
		self.netloc = urlobj.netloc
		self.path = urlobj.path
		self.paths = self.split_path()
		self.query = urlobj.query
		self.fragment = urlobj.fragment
		self.domain = extract(urlobj.netloc).domain
		self.rootdomain = extract(urlobj.netloc).registered_domain
		self.subdomain = extract(urlobj.netloc).subdomain.split('.')
		self.domain_info = self.get_domain_info()
		self.extion = extion
		self.file_ext = self.get_extion()
		self.urlfile = self.get_urlfile()
		self.baseurl = self.scheme+'://'+self.netloc
		self.dependent = self.get_dependent()

	def parse(self):
		urlsplit = {}
		urlsplit['url'] = self.url
		urlsplit['scheme'] = self.scheme
		urlsplit['netloc'] = self.netloc
		urlsplit['query'] = self.split_query()
		urlsplit['path'] = self.split_path()
		urlsplit['extion'] = self.get_extion()
		urlsplit['fragment'] = self.fragment
		return urlsplit

	def split_query(self):
		query = {}
		condition = self.query.split('&')
		if len(condition) >= 1:
			for line in condition:
				line_split = line.split('=')
				if len(line_split) > 1:
					query[line_split[0]] = line_split[1]
				else:
					query[line_split[0]] = ''
			return query
		else: return ''

	def split_path(self):
		path = []
		for dirs in self.path.split('/'):
			if dirs != '': path.append(dirs)
		return path

	def split_fragment(self):
		fragment = []
		for frags in self.fragment.split('='):
			if frags != '':
				fragment.append(frags)
		return fragment

	def get_domain_info(self):
		# 扩充域名信息节点
		domain = self.domain
		subdomain = self.subdomain
		subdomain.append(domain)
		if '' in subdomain:
			subdomain.remove('')
		return subdomain

	def get_dependent(self):
		# 生成其因变量组
		dependent = []
		dependent.extend(self.split_query().keys())
		dependent.extend(self.split_query().values())
		dependent.extend(self.split_fragment())
		dependent.extend(self.get_paths()['path'])
		dependent.extend(self.domain_info)
		dependent.append(self.file_ext)
		dependent = list(set(dependent))
		if '' in dependent: dependent.remove('')
		return dependent

	def get_extion(self):
		path = self.split_path()
		if len(path) >= 1: 
			filename = path[-1].split('.')
			if len(filename) > 1: 
				return filename[-1]
			else: return self.extion
		else: return self.extion

	def get_urlfile(self):
		# 初始化脚本文件
		urlfile = self.path
		if self.get_extion():
			file_ext = self.get_extion()
			if urlfile == '/':
				urlfile = urlfile+'index.'+file_ext
			elif urlfile == '':
				urlfile = urlfile+'/index.'+file_ext
			elif not urlfile.endswith(file_ext):
				urlfile = urlfile+'.'+file_ext
		return urlfile

	def get_paths(self):
		paths = []
		segments = ['/']
		fullpath = ''
		if self.path.endswith('/'):
			for pathline in self.paths:
				paths.append(pathline)
				fullpath += '/' + pathline
				segments.append(fullpath)
		else:
			for pathline in self.paths:
				if pathline == self.paths[-1]:
					if '.' in pathline: # 最后一个是文件，判断是否存在扩展名
						rstrip_path = pathline.replace(('.' + self.file_ext), '')
						paths.append(rstrip_path)
					else:
						paths.append(pathline)
				else:
					paths.append(pathline)
					fullpath += '/' + pathline
					segments.append(fullpath)

		return {'segment':segments,'path': paths}






