# -*- coding: utf-8 -*-

from settings import Settings
from fighter import Fighter
from battle import Battle
import fight_engine as fn
import common_function as cf

if __name__ == '__main__':
	print("Welcome to the Civil War of the Avengers.")
	mode = cf.choose_input("Automatically fight?", ["y", "n"], "(y/n)")  # 询问是否开启自动战斗
	tony_mode = "minimax_random"
	steven_mode = "minimax_random"
	if mode == 'n':
		choice = cf.choose_input("Who do you want to stand for?", ["t", "s"],
								 "(T: Tony Starks / S: Steven Rogers)")  # 若手动操作，询问操作哪一方
		if choice == 't':
			tony_mode = 'user'
		else:
			steven_mode = 'user'

	# 初始化
	settings = Settings()
	win = [0, 0, 0]
	for i in range(1, 101):
		tony = Fighter("Tony Stark", settings)
		steven = Fighter("Steven Rogers", settings)
		steven.mp += 3
		battle = Battle(tony, steven, settings)
		while battle.round:
			# 获取战斗策略
			tony_act = tony.fight_strategy(steven, tony_mode, 50)
			# 进行战斗
			fn.fight_function[tony_act](tony, steven)
			# 键盘输出
			# cf.keyboard_output(settings, tony, steven, tony_act, 1)
			winner = battle.check_winner()
			if winner:
				break
			# 获取战斗策略
			steven_act = steven.fight_strategy(tony, steven_mode, 50)
			# 进行战斗
			fn.fight_function[steven_act](steven, tony)
			# 键盘输出
			# cf.keyboard_output(settings, tony, steven, steven_act, 0)
			# 判断胜负
			battle.round -= 1
			winner = battle.check_winner()
			if winner:
				break
		win[winner - 1] += 1
	print("TS won %d games, SR won %d games, and %d games tied." % (win[0], win[1], win[2]))
