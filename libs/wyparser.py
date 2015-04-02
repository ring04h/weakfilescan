#!/usr/bin/env python
# encoding: utf-8
# email: ringzero@0x557.org

import re
import string
from datetime import *
import datetime
import utils.exrex as exrex

"""
string.digits
string.lowercase
string.uppercase
string.letters
"""

# 规则解释器，四种模式：date/int/str/re

class DictParser(object):
	"""
		docstring for DictParser
		字典可配置规则解析器
		{类型=名称#长度$step:开始-结束}
	"""
	def __init__(self, dictstr):
		super(DictParser, self).__init__()
		self.dictstr = dictstr

	def parse(self):
		if self.get_reg_rule():
			parse_result = []
			start_str = self.get_start_str()
			end_str = self.get_end_str()
			dic_result = self.generate_dic(self.get_reg_rule())
			for line in dic_result:
				parse_result.append('%s%s%s' % (start_str, line, end_str))
			return parse_result
		else:
			return ''

	def get_reg_rule(self):
		# 获取字典生成规则
		reg_str = re.compile(r'(\{date|\{int|\{re|\{str).+\}\$')
		result = reg_str.search(self.dictstr)
		if result:
			# 判断是否有分隔符存在,是否正常规则
			if ':' in result.group() and result.group().startswith('{') and result.group().endswith('}$'):
				return result.group()[1:][:-2]
			else:
				return ''

	def generate_dic(self, myrule):
		
		"""
			分离规则，获取条件和参数
			rule_name : 规则类型 ['DATE','INT','STR']
			rule_type : 规则子分类
			option_start : 起始字符
			option_end : 结束字符
		"""

		rules, options = myrule.split(':')
		rule_name, rule_type = rules.split('=')

		# 解析规则类型
		# 日期、整数、字符
		if rule_name == 'date': # 处理日期
			
			"""
				日期会出现的子分类情况，初始位数补充0911,911
				年(YEAR) 2005-2015
				月(MON) 1-12
				# 日(DAY) 0-30 !!! 这种情况几乎不存在
				年月(YEAR_MON) 200501-201512
				月日(MON_DAY) 0101-1231
				年月日(YEAR_MON_DAY) 20050101-20151231
				月日年(MON_DAY_YEAR) 01012005-12312015
			"""

			if rule_type == 'year': # 返回指定年份列表
				result = []
				option_from, option_to = options.split('-')
				if len(option_from) == 4 and len(option_to) == 4:
					for year in xrange(int(option_from), int(option_to) + 1):
						result.append(str(year))
						result.append(str(year)[-2:4])
				return result
			elif rule_type == 'mon': # 返回指定月份列表
				result = []
				option_from, option_to = options.split('-')
				if len(option_from) <= 2 and len(option_to) <= 2:
					for month in xrange(int(option_from), int(option_to) + 1):
						result.append(str(month))
						if len(str(month)) == 1:
							result.append('0' + str(month))
				return result
			elif rule_type == 'day': # 返回日期列表 !!! 这种情况几乎不存在
				result = []
				option_from, option_to = options.split('-')
				if len(option_from) <= 2 and len(option_to) <= 2:
					for day in xrange(int(option_from), int(option_to) + 1):
						result.append(str(day))
						if len(str(day)) == 1:
							result.append('0' + str(day))
				return result
			elif rule_type == 'year_mon': # 年月
				result = []
				option_from, option_to = options.split('-')
				if len(option_from) == 6 and len(option_to) == 6:
					from_year = option_from[0:4]
					from_mon = option_from[4:6]
					to_year = option_to[0:4]
					to_mon = option_to[4:6]
					for year in xrange(int(from_year), int(to_year) + 1):
						for month in xrange(int(from_mon), int(to_mon) + 1):
							if len(str(month)) == 1:
								result.append(str(year) + '0' + str(month))
							result.append(str(year) + str(month))
				return result
			elif rule_type == 'mon_day': # 月日，采用库函数
				result = []
				today = date.today()
				this_year = today.year
				option_from, option_to = options.split('-')
				if len(option_from) == 4 and len(option_to) == 4:
				 	from_mon = option_from[0:2]
					from_day = option_from[2:4]
					to_mon = option_to[0:2]
					to_day = option_to[2:4]
					from_date = date(int(this_year), int(from_mon), int(from_day))
					to_date = date(int(this_year), int(to_mon), int(to_day))
					total_days = to_date - from_date
					for day in xrange(total_days.days):
						day += 1
						concat_date = from_date + datetime.timedelta(days=day)
						result.append(concat_date.strftime('%-m%-d'))
						result.append(concat_date.strftime('%m%d')) # 保留前置零
				result = list(set(result))
				return result
			elif rule_type == 'year_mon_day': # 年月日
				result = []
				option_from, option_to = options.split('-')
				if len(option_from) == 8 and len(option_to) == 8:
					from_year = option_from[0:4]
					from_mon = option_from[4:6]
					from_day = option_from[6:8]
					to_year = option_to[0:4]
					to_mon = option_to[4:6]
					to_day = option_to[6:8]
					from_date = date(int(from_year), int(from_mon), int(from_day))
					to_date = date(int(to_year), int(to_mon), int(to_day))
					total_days = to_date - from_date
					for day in xrange(total_days.days):
						day += 1
						concat_date = from_date + datetime.timedelta(days=day)
						result.append(concat_date.strftime('%y%-m%-d'))
						result.append(concat_date.strftime('%Y%-m%-d'))
						result.append(concat_date.strftime('%y%m%d')) # 保留前置零
						result.append(concat_date.strftime('%Y%m%d')) # 保留前置零
				result = list(set(result))
				return result
			elif rule_type == 'mon_day_year': # 月日年
				result = []
				option_from, option_to = options.split('-')
				if len(option_from) == 8 and len(option_to) == 8:
					from_year = option_from[4:8]
					from_mon = option_from[0:2]
					from_day = option_from[2:4]
					to_year = option_to[4:8]
					to_mon = option_to[0:2]
					to_day = option_to[2:4]
					from_date = date(int(from_year), int(from_mon), int(from_day))
					to_date = date(int(to_year), int(to_mon), int(to_day))
					total_days = to_date - from_date
					for day in xrange(total_days.days):
						day += 1
						concat_date = from_date + datetime.timedelta(days=day)
						result.append(concat_date.strftime('%y%-m%-d'))
						result.append(concat_date.strftime('%Y%-m%-d'))
						result.append(concat_date.strftime('%y%m%d')) # 保留前置零
						result.append(concat_date.strftime('%Y%m%d')) # 保留前置零
				result = list(set(result))
				return result

		elif rule_name == 'int': # 处理整数
			if rule_type.startswith('series'): # 正常按照顺序递进，单步处理step
				result = []
				option_from, option_to = options.split('-')
				step_reg = re.compile(r'\$\d+')
				if step_reg.search(rule_type): # 存在步长选项
					step = step_reg.search(rule_type).group().lstrip('$')
					for i in xrange(int(option_from), int(option_to) + 1, int(step)):
						result.append(i)
				else: # 没有步长选项，默认为1
					for i in xrange(int(option_from), int(option_to) + 1):
						result.append(i)
				return result
			elif rule_type.startswith('digits'): # 连号数字，硬编码写入键盘连续位
				result = []
				option_from, option_to = options.split('-')
				length_reg = re.compile(r'\#\d+')
				if length_reg.search(rule_type): # 存在长度选项
					length = length_reg.search(rule_type).group().lstrip('#')
					length = int(length)
					for i in xrange(int(option_from), int(option_to) + 2 - length):
						concat_char = []
						for value in xrange(length):
							concat_char.append(str(i + value))
						result.append(''.join(concat_char))
						result.append(''.join(concat_char)[::-1]) # 倒序
				return result
			elif rule_type.startswith('overlap'): # 重叠数字
				result = []
				option_from, option_to = options.split('-')
				length_reg = re.compile(r'\#\d+')
				if length_reg.search(rule_type): # 存在长度选项
					length = length_reg.search(rule_type).group().lstrip('#')
					for i in xrange(int(option_from), int(option_to) + 1):
						result.append(str(i) * int(length))
				return result

		elif rule_name == 'str': # 处理字符
			if rule_type.startswith('letters'): # 正常按照顺序递进，单步处理step
				result = []
				option_from, option_to = options.split('-')
				length_reg = re.compile(r'\#\d+')
				if length_reg.search(rule_type): # 存在长度选项
					length = length_reg.search(rule_type).group().lstrip('#')
					length = int(length)
					# 字母的临界值 (z-length) (Z-length)
					"""
						小于91，都是大写
						a(97) - z(122)
						A(65) - Z(90)
						大于91，都是小写
					"""
					if ord(option_from) > 96 and ord(option_to) > 96: # 都是小写
						str_from_id = string.letters.index(option_from)
						str_to_id = string.letters.index(option_to)
					elif ord(option_from) < 91 and ord(option_to) < 91: # 都是大写
						str_from_id = string.letters.index(option_from)
						str_to_id = string.letters.index(option_to)
					elif ord(option_from) > 91 and ord(option_to) < 96: # 开始小写，结束大写
						str_from_id = string.letters.index(option_from)
						str_to_id = string.letters.index(option_to)
					else:
						pass # print '规则错误'
					for i in xrange(str_from_id, str_to_id-length+2): # 平衡xrange分配id从0开始
						concat_char = []
						for value in xrange(length):
							concat_char.append(string.letters[i + value])
						result.append(''.join(concat_char))
						# result.append(''.join(concat_char)[::-1]) # 结果倒序
				return result

			if rule_type.startswith('overlap'): # 重叠字母
				result = []
				option_from, option_to = options.split('-')
				if ord(option_from) > 96 and ord(option_to) > 96: # 都是小写
					str_from_id = string.letters.index(option_from)
					str_to_id = string.letters.index(option_to)
				elif ord(option_from) < 91 and ord(option_to) < 91: # 都是大写
					str_from_id = string.letters.index(option_from)
					str_to_id = string.letters.index(option_to)
				elif ord(option_from) > 91 and ord(option_to) < 96: # 开始小写，结束大写
					str_from_id = string.letters.index(option_from)
					str_to_id = string.letters.index(option_to)
				else:
					pass # print '规则错误'
				length_reg = re.compile(r'\#\d+')
				if length_reg.search(rule_type): # 存在长度选项
					length = length_reg.search(rule_type).group().lstrip('#')
					length = int(length)
					for letter in string.letters[str_from_id:str_to_id+1]:
						result.append(letter * length)
				return result

		elif rule_name == 're': # 自定义正则解析器
			"""
			已知的正则解析生成器有 exrex、sre_yield
			"""
			if rule_type.startswith('exrex'): # exrex 引擎
				result = list(exrex.generate(options))
				return result
			if rule_type.startswith('sre_yield'): # sre_yield 引擎
				import sre_yield
				result = list(sre_yield.AllStrings(options))
				return result
			else:
				pass

	def get_start_str(self):
		# 获取字典起始字符串
		start_str = re.compile(r'^.+(\{date|\{int|\{re|\{str)')
		result = start_str.search(self.dictstr)
		if result:
			return re.sub('(\{date|\{int|\{re|\{str)', '', result.group())
		else:
			return ''

	def get_end_str(self):
		# 获取字典结束字符串
		end_str = re.compile(r'(\}\$).+')
		result = end_str.search(self.dictstr)
		if result:
			return result.group().replace('}$','')
		else:
			return ''







