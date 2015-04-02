# encoding: utf-8
# 传递一个siteurl，返回当前网页下的三层链接资源
# email: ringzero@0x557.org

import sys
sys.path.append("../")
from config import *
from common import *
import threading
import Queue
import urlparse

class GetAllLink(object):
	"""docstring for GetAllLink"""
	def __init__(self, siteurl):
		super(GetAllLink, self).__init__()
		self.siteurl = siteurl
		self.basedomain = get_basedomain(siteurl)
		
	class WyWorker(threading.Thread):
		def __init__(self,queue):
			threading.Thread.__init__(self)
			self.queue = queue
		def run(self):
			while True:
				if self.queue.empty():
					break
				# 用hack方法，no_timeout读取Queue队列，直接异常退出线程避免阻塞
				try:
					url = self.queue.get_nowait()
					response_obj = LinksParser(http_request_get(url))
					resources[url] = response_obj.getall()
				except Exception, e:
					# print e # 队列阻塞
					break

	def start(self):
		# 爬取三层结构基本上就能够覆盖90%链接了，动态结构层将来改进
		link_datas = {
			'a' : {},
			'img' : {},
			'link' : {},
			'script' : {}
		}

		# 获取根网页的所有链接内容
		response_obj = LinksParser(http_request_get(self.siteurl))
		links_res = response_obj.getall()

		for key in links_res.keys(): # 只有A链接的资源需要进一步处理，img, link, script，硬编码实现
			link_arr = {}
			for link in links_res[key]['a']:
				link_arr[link] = []
			link_datas['a'][key] = link_arr

			for proc_key in ['img', 'link', 'script']: # 硬编码逐个处理静态资源
				netloc = urlparse.urlparse(key).netloc
				link_datas[proc_key][netloc] = []
				for link in links_res[key][proc_key]:
					link_datas[proc_key][netloc].append(link)

		# 生成任务队列
		queue = Queue.Queue()

		second_links = link_arr.keys() # 开始处理第二层链接，不用递归方法
		for url in second_links:
			netloc = urlparse.urlparse(url).netloc
			if self.basedomain in netloc: # 检查链接的hostname部分是否与主域名相同
				queue.put(url)

		global resources
		resources = {}
		threads = [] # 初始化线程组
		for i in xrange(threads_count):
			threads.append(self.WyWorker(queue))
		for t in threads: # 启动线程
			t.start()
		for t in threads: # 等待线程执行结束后，回到主线程中
			t.join()

		for rkey in resources.keys(): # 多线程任务结束，遍历结果数组
			if link_datas['a'][key].has_key(rkey):
				link_datas['a'][key][rkey] = resources[rkey].values()[0]['a']

		for proc_key in ['img', 'link', 'script']: # 硬编码逐个处理静态资源
			for rkey in resources.keys():
				for link in resources[rkey].keys(): # 初始化创建对应的[netloc]数组
					netloc = urlparse.urlparse(link).netloc
					if not link_datas[proc_key].has_key(netloc):
						link_datas[proc_key][netloc] = []
					for res_link in resources[rkey][link][proc_key]: # 处理所有netloc对应的静态资源压入数组
						link_datas[proc_key][netloc].append(res_link)

		return link_datas




