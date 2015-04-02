#!/usr/bin/env python
# encoding: utf-8
# email: ringzero@0x557.org
# http://github.com/ring04h/weakfilescan
# 通过一个网页获取三层目录下的所有链接资源

import sys
from config import *
from common import *
import json
import urlparse
from libs.GetAllLink import GetAllLink

def start_getlinks(siteurl):
	if not siteurl.startswith('http://'):
		siteurl = 'http://%s' % siteurl
	siteurl = siteurl.rstrip('/')
	link_datas = GetAllLink(siteurl).start()
	return json.dumps(link_datas, indent=2)

if __name__ == "__main__":
	if len(sys.argv) == 2:
		print start_getlinks(sys.argv[1])
		sys.exit(0)
	else:
		print ("usage: %s http://www.wooyun.org" % sys.argv[0])
		sys.exit(-1)
