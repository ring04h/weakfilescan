# encoding: utf-8
# 全局函数文件
# email: ringzero@0x557.org

"""
	字典文件动态解析器
	# 使用说明
	fuzz_bak = ProcessDic('./dict/package_ext.lst').parser()
	fuzz_tmp = ProcessDic('./dict/tmpfile_ext.lst').parser()
	fuzz_filename_replace = {'%EXT%':'jsp'}
	fuzz_filename = ProcessDic('./dict/filename.lst',fuzz_filename_replace).parser()
"""
from wyparser import DictParser
from utils.FileUtils import FileUtils

class ProcessDic(object):
	"""docstring for ProcessDic"""
	def __init__(self, dicfile, replace_dict={}):
		super(ProcessDic, self).__init__()
		self.dicfile = dicfile
		self.replace_dict = replace_dict

	def parser(self):
		# 读取字典文件存入变量
		tmp_dict = []
		for line in FileUtils.getLines(self.dicfile):
			tmp_dict.append(line)
		# 检查是否拥有需要替换的固定组合
		if len(self.replace_dict) >= 1:
			for key in self.replace_dict.keys():
				new_dict = []
				replace_key = key
				replace_value = self.replace_dict[key]
				for tmp_line in tmp_dict:
					if replace_key in tmp_line:
						new_dict.append(tmp_line.replace(replace_key, replace_value))
					else:
						new_dict.append(tmp_line)
				tmp_dict = new_dict
			fuzz_lst = []
			for line_ in new_dict:
				# 利用正则引擎遍历一次字典
				parser = DictParser(line_)
				wyparser_result = parser.parse()
				if wyparser_result:
					for parser_line in wyparser_result:
						fuzz_lst.append(parser_line)
				else:
					fuzz_lst.append(line_)
			return fuzz_lst
		else:
			fuzz_lst = []
			for line_ in tmp_dict:
				# 利用正则引擎遍历一次字典
				parser = DictParser(line_)
				wyparser_result = parser.parse()
				if wyparser_result:
					for parser_line in wyparser_result:
						fuzz_lst.append(parser_line)
				else:
					fuzz_lst.append(line_)
			return fuzz_lst