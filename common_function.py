# -*- coding: utf-8 -*-
"""定义通用函数"""


def choose_input(message, limit_list, intro):
	"""询问用户选择输入
	Args:
		message: 第一次询问时的信息
		limit_list: 输入选择限定列表
		intro: 对输入的说明，用户输入错误，重新询问时需要展示
	Returns:
		value: 用户输入的值
	"""
	value = input(message + " " + intro + ": ").strip().lower()
	if value == "q" or value == "quit":  # 输入q则退出程序
		quit()
	if len(limit_list) > 0:
		while value not in limit_list:  # 若用户输入不在可输入范围，则重新询问
			value = input("Please check your input." + intro + ": ").strip().lower()
			if value == "q" or value == "quit":  # 输入q则退出程序
				quit()
	return value


def keyboard_output(settings, fighter_x, fighter_y, action_x, action_y):
	"""询问用户选择输入
	Args:
		settings: 设定信息，获取预设评论长度等
		fighter_x, fighter_y: 对战双方
		action_x, action_y: 本回合的动作
	"""
	# 获取名字简写，更改动作时态
	simple_name_x = "".join([name[0:1] for name in fighter_x.name.split()])
	simple_name_y = "".join([name[0:1] for name in fighter_y.name.split()])
	if action_x == "do nothing":
		action_x = "did nothing"
	else:
		action_x += "ed"
	if action_y == "do nothing":
		action_y = "did nothing"
	else:
		action_y += "ed"
	commentary = fighter_x.name + " " + action_x + ", " + fighter_y.name + " " + action_y + "."
	# 计算空格长度
	blank_len = settings.max_comment - 2 * settings.sta_length - len(commentary)
	blank1 = " " * (blank_len // 2)
	blank2 = " " * (blank_len - blank_len // 2)
	print("%s|%02d|%d:%d%s%s%s%d:%d|%02d|%s" % (simple_name_x, fighter_x.hp, fighter_x.mp, fighter_x.cd,
												blank1, commentary, blank2,
												fighter_y.cd, fighter_y.mp, fighter_y.hp, simple_name_y))
