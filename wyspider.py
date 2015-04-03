#!/usr/bin/env python
# encoding: utf-8
# email: ringzero@0x557.org
# http://github.com/ring04h/weakfilescan

"""
	weakfilescan
	userage: python wyspider.py http://wuyun.org
"""

import sys
import libs.requests as requests
from controller import *

if __name__ == "__main__":
	if len(sys.argv) == 3:
		print json.dumps(start_wyspider(sys.argv[1]), indent=2)
		sys.exit(0)
	elif len(sys.argv) == 2:
		print json.dumps(start_wyspider(sys.argv[1]),indent=2)
		sys.exit(0)
	else:
		print ("usage: %s http://wuyun.org php" % sys.argv[0])
		sys.exit(-1)







