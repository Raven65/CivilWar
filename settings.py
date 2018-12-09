# -*- coding: utf-8 -*-


class Settings():
	"""全局设定类
	包含最大回合数，角色各属性边界，角色可用动作，评论长度等
	"""

	def __init__(self):
		self.max_hp = 30
		self.max_mp = 10
		self.max_cdr = 4
		self.max_round = 50
		self.max_comment = 90
		self.sta_length = 10
		# 动作和操作指令对应
		self.actions = {
			"do nothing": 0,
			"attack": 1,
			"defend": 2,
			"counter attack": 3,
			"super attack": 4
		}
		self.max_act = 4
		self.min_act = 1
