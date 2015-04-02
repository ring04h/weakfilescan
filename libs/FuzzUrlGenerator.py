# encoding: utf-8
# Fuzz URL列表 生成器
# email: ringzero@0x557.org

import sys
sys.path.append("../")
from config import *
import urlparse
from UrlSplitParser import UrlSplitParser

class UrlGenerator(object):
	"""docstring for UrlGenerator"""
	def __init__(self, url, fuzz_bak, fuzz_tmp, extion=default_extion):
		super(UrlGenerator, self).__init__()
		self.url = url
		self.fuzz_bak = fuzz_bak
		self.fuzz_tmp = fuzz_tmp
		self.extion = extion

	def generator(self):
		# 整合其因变量(目录列表、文件名、域名、子域名)，拼接备份文件、临时文件
		parser_obj = UrlSplitParser(urlparse.urlparse(self.url),self.extion)
		url_parser = parser_obj.get_paths()
		urls_result = []

		# 处理其因变量备份文件扩展
		depend_files = []
		for bak_line in self.fuzz_bak:
			for depend in parser_obj.dependent:
				depend_files.append(depend + bak_line)

		# 处理临时文件扩展
		script_files = []
		for tmp_line in self.fuzz_tmp:
			if url_parser['path']:
				for path_name in url_parser['path']:
					script_files.append(path_name + '.' + parser_obj.file_ext + tmp_line)
			else:
				script_files.append('index.' + parser_obj.file_ext + tmp_line)

		# 需要检测的目录
		for webdir in url_parser['segment']:
			# 拼接备份文件扫描完整URL
			for depend in depend_files:
				if webdir == '/':
					urls_result.append(parser_obj.baseurl + webdir + depend)
				else:
					urls_result.append(parser_obj.baseurl + webdir + '/' + depend)
			# 拼接临时文件扫描完整URL
			for script in script_files:
				if webdir == '/':
					urls_result.append(parser_obj.baseurl + webdir + script)
				else:
					urls_result.append(parser_obj.baseurl + webdir + '/' + script)
					
		return urls_result



