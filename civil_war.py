# -*- coding: utf-8 -*-

from settings import Settings
from fighter import Fighter
from battle import Battle
import fight_engine as fn
import common_function as cf

if __name__ == '__main__':
	print("Welcome to the Civil War of the Avengers.")
	mode = cf.choose_input("Automatically fight?", ["y", "n"], "(y/n)")  # 询问是否开启自动战斗
	tony_mode = "minimax"
	steven_mode = "random"
	if mode == 'n':
		choice = cf.choose_input("Who do you want to stand for?", ["t", "s"],
								 "(T: Tony Starks / S: Steven Rogers)")  # 若手动操作，询问操作哪一方
		if choice == 't':
			tony_mode = 'user'
		else:
			steven_mode = 'user'

	# 初始化
	settings = Settings()
	tony = Fighter("Tony Stark", settings)
	steven = Fighter("Steven Rogers", settings)
	battle = Battle(tony, steven, settings)
	while battle.round:

		# 获取战斗策略
		tony_act = tony.fight_strategy(steven, tony_mode)
		steven_act = steven.fight_strategy(tony, steven_mode)

		# 进行战斗
		fn.fight_function[tony_act](tony, steven, steven_act)
		fn.fight_function[steven_act](steven, tony, tony_act)

		# 键盘输出
		cf.keyboard_output(settings, tony, steven, tony_act, steven_act)

		# 判断胜负
		battle.round -= 1
		battle.check_winner()

