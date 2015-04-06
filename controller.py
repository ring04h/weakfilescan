# encoding: utf-8
# 主控制器
# email: ringzero@0x557.org
# http://github.com/ring04h/weakfilescan

import sys
from config import *
from common import *
import json
import urlparse
from libs.GenerateDict import ProcessDic
from libs.GetAllLink import GetAllLink
from libs.HttpFuzzEnginer import FuzzEnginer

reload(sys)
sys.setdefaultencoding('utf-8')

def start_wyspider(siteurl): # 启动爬虫和fuzz类
	# 目标赋值
	if "://" not in siteurl:
		siteurl = 'http://%s' % siteurl.rstrip('/')
	siteurl = siteurl.rstrip('/')
	basedomain = get_basedomain(siteurl)

	print '-' * 50
	print '* scan %s start' % siteurl
	print '-' * 50

	# 初始化字典
	fuzz_bak = ProcessDic(package_ext_dict).parser()
	fuzz_tmp = ProcessDic(tempfile_ext_dict).parser()

	bak_ext_re = '|'.join(fuzz_bak).replace('.', '\.') # 生成常见备份文件规则
	fuzz_filename_replace = {'%EXT%':default_extion,'%BAK_EXT%':bak_ext_re}
	fuzz_filename = ProcessDic(filename_dict,fuzz_filename_replace).parser()

	fuzz_webdirs = ProcessDic(directory_dict).parser()
	fuzz_webdirs_common = ProcessDic(directory_common_dict).parser()

	# 传递一个siteurl，返回当前网页下的三层链接资源
	link_datas = GetAllLink(siteurl).start()

	fuzzdir_request_set = {} # 目录fuzz请求集合
	fuzzfile_request_set = [] # 文件fuzz请求集合

	# 分析爬虫获取的链接，得到所有已知的WEB目录，生成目录FUZZ
	url_webdirs = []
	for category in link_datas.keys():
		if category == 'a': # 所有a=href资源
			for key in link_datas[category].keys(): # 这里的KEY只是域名对象,可以跳过处理
				for second_key in link_datas[category][key].keys(): # 处理第二层的KEY
					url_webdirs.extend(get_segments(second_key))
					urlgenerator_obj = UrlGenerator(second_key, fuzz_bak, fuzz_tmp, extion=default_extion)
					fuzzfile_request_set.extend(urlgenerator_obj.generator())
					for url_values in link_datas[category][key][second_key]: # 处理第二层KEY下的所有（三层链接）
						url_webdirs.extend(get_segments(url_values))
						urlgenerator_obj = UrlGenerator(url_values, fuzz_bak, fuzz_tmp, extion=default_extion)
						fuzzfile_request_set.extend(urlgenerator_obj.generator())
		else: # 所有静态资源（img,link,script）
			pass # 暂不处理静态资源
			# for key in link_datas[category].keys(): # 这里的KEY只是域名对象,可以跳过处理
			# 	for url_values in link_datas[category][key]:
			# 		url_webdirs.extend(get_segments(url_values))

	url_webdirs = list(set(url_webdirs))
	possibility_urls = {siteurl:[]} # fuzz目录列表
	possibility_files = {siteurl:[]} # fuzz 文件列表

	for webdir in url_webdirs: # 生成存在的服务器列表
		if basedomain in webdir:
			httpurl = urlparse.urlparse(webdir).scheme+'://'+urlparse.urlparse(webdir).netloc+'/'
			if not possibility_urls.has_key(httpurl):
				possibility_urls[httpurl] = []
			possibility_urls[httpurl].append(webdir.rstrip('/')+'/')

	possibility_info = {} # 服务端容错处理机制信息
	for httpurl in possibility_urls.keys(): # 清空无法做出正常判断的服务器
		if not checksite_isalive(httpurl): # 纯http请求，返回资源为None，代表出错
			del possibility_urls[httpurl]
		else:
			possibility = checksite_possibility(httpurl)
			if not possibility['considered']: # 服务端配置了容错处理，fuzz规则无法判断
				del possibility_urls[httpurl]
			else:
				possibility_info[httpurl] = possibility

	if checksite_isalive(siteurl): # 根服务器是存活的
		siteurl_possibility = checksite_possibility(siteurl)
		if siteurl_possibility['considered']: # 服务端配置了容错处理，fuzz规则无法判断
			# 根目录 fuzz 对象列表生成
			possibility_info[siteurl] = siteurl_possibility
			for root_fuzz_dir in fuzz_webdirs:
				url = siteurl.rstrip('/')+root_fuzz_dir.rstrip('/')+'/'
				if not fuzzdir_request_set.has_key(siteurl):
					fuzzdir_request_set[siteurl] = []
				fuzzdir_request_set[siteurl].append(url)
			rootdir = siteurl.rstrip('/') # 压入网站根目录
			fuzzdir_request_set[siteurl].append(rootdir) # 压入根目录其因变量文件
			urlgenerator_obj = UrlGenerator(rootdir, fuzz_bak, fuzz_tmp, extion=default_extion)
			possibility_files[siteurl].extend(urlgenerator_obj.generator())

	for http_siteurl in fuzzdir_request_set.keys():
		if not possibility_urls.has_key(http_siteurl): possibility_urls[http_siteurl] = []
		# 生成向HttpFuzzEnginer传递的目录URL列表
		request_webdirs = list(set(fuzzdir_request_set[http_siteurl]))
		refer_to_val = possibility_info[http_siteurl]['refer_to_val']
		httpfuzz_result = FuzzEnginer(request_webdirs, refer_to_val=refer_to_val).start()
		for status_code in httpfuzz_result: # 分析多线程fuzz的结果
			for url in httpfuzz_result[status_code].keys():
				possibility_urls[http_siteurl].append(url.rstrip('/')+'/')
		possibility_urls[http_siteurl] = list(set(possibility_urls[http_siteurl]))

	existing_files = {} # 存在的文件列表
	for httpsite in possibility_urls.keys(): # 处理文件字典，将文件与目录拼接
		if not possibility_files.has_key(httpsite):
			possibility_files[httpsite] = []
		for http_dirurl in possibility_urls[httpsite]:
			for fuzz_request_file in fuzz_filename:
				fuzz_request_path = http_dirurl.rstrip('/')+'/'+fuzz_request_file
				possibility_files[httpsite].append(fuzz_request_path)

	# ----------------------------------------------------
	#  将其因变量文件列表中的内容进行分类
	# ----------------------------------------------------
	for fuzzfile in fuzzfile_request_set:
		if basedomain in fuzzfile:
			httpurl = urlparse.urlparse(fuzzfile).scheme+'://'+urlparse.urlparse(fuzzfile).netloc+'/'
			if not possibility_files.has_key(httpurl):
				possibility_files[httpurl] = []
			possibility_files[httpurl].append(fuzzfile)

	for http_fileurl in possibility_files.keys(): # 清空无法做出正常判断的服务器
		if not checksite_isalive(http_fileurl): # 纯http请求，返回资源为None，代表出错
			del possibility_files[http_fileurl]
		else:
			possibility = checksite_possibility(http_fileurl)
			if not possibility['considered']: # 服务端配置了容错处理，fuzz规则无法判断
				del possibility_files[http_fileurl]
			else:
				possibility_info[http_fileurl] = possibility

	for http_fileurl in possibility_files.keys():
		request_files = list(set(possibility_files[http_fileurl]))
		refer_to_val = possibility_info[http_fileurl]['refer_to_val']
		httpfuzz_result = FuzzEnginer(request_files, refer_to_val=refer_to_val).start()
		for status_code in httpfuzz_result: # 分析多线程fuzz的结果
			for fileurl in httpfuzz_result[status_code].keys():
				if not existing_files.has_key(http_fileurl):
					existing_files[http_fileurl] = {}
				first_segment = get_first_segment(fileurl) # 获取文件的1级目录名称，并为结果分类
				if not existing_files[http_fileurl].has_key(first_segment):
					existing_files[http_fileurl][first_segment] = []
				existing_files[http_fileurl][first_segment].append(fileurl)

	print '-' * 50
	print '* scan complete...'
	print '-' * 50

	# 误报结果统计清洗
	for httpsite in existing_files.keys():
		for first_segment in existing_files[httpsite].keys():
			if len(existing_files[httpsite][first_segment]) > resulst_cnt_val:
				existing_files[httpsite][first_segment] = ['misdescription cleaned']

	for httpsite in possibility_urls.keys():
		if len(possibility_urls[httpsite]) > resulst_cnt_val:
			possibility_urls[httpsite] = ['misdescription cleaned']

	return {'dirs':possibility_urls,'files':existing_files}



