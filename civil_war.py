# -*- coding: utf-8 -*-

from settings import Settings
from fighter import Fighter
from battle import Battle
# import numpy as np
from ga import Ga
import fight_engine as fn
import common_function as cf


def my_func(x):
	return x[1]


def medianFind(lst):
	# 先将列表进行排序
	lst.sort()
	half = len(lst) // 2
	# 得到中间序列，~half为负索引，列表元素可能为偶数，需要获取中间两个数
	# 转化成float，中位数可能为浮点数类型，如测试用例
	median = (float(lst[half]) + float(lst[~half])) / 2
	return median


if __name__ == '__main__':
	print("Welcome to the Civil War of the Avengers.")
	mode = cf.choose_input("Automatically fight?", ["y", "n"], "(y/n)")  # 询问是否开启自动战斗
	tony_mode = "random"
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
	ga = Ga(settings, 100)
	md = 0
	s = []
	for k in range(10):
		test = []
		for index in range(100):
			win = [0, 0, 0]
			for i in range(10, 1010):
				tony = Fighter("Tony Stark", settings)
				steven = Fighter("Steven Rogers", settings)
				steven.mp += 3
				battle = Battle(tony, steven, settings)
				while battle.round:

					# 获取战斗策略
					tony_act = ga.strategy(ga.population[index], tony, steven, md)[1]
					s.append(ga.strategy(ga.population[index], tony, steven, md)[0])
					# 进行战斗
					fn.fight_function[tony_act](tony, steven)
					# 键盘输出
					# cf.keyboard_output(settings, tony, steven, tony_act, 1)
					winner = battle.check_winner()
					if winner:
						break
					# 获取战斗策略
					steven_act = steven.fight_strategy(tony, steven_mode, i // 10)
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
			test.append((index, win[0]))
		# print("TS won %d games, SR won %d games, and %d games tied." % (win[0], win[1], win[2]))
		md = medianFind(s)
		test.sort(key=my_func, reverse=True)
		print("The best won %d games." % (test[0][1]))
		total = 0
		for i in range(100):
			total += test[i][1]
		print("average:%d. " % (total / 100))
		temp = []
		for j in range(20):
			temp.append(test[j][0])
		ga.copy(temp)
		for j in range(20, 80):
			temp.append(test[j][0])
		ga.calculate_p(temp, test)
		ga.cross_over(temp, 0.5)
		ga.mutation(0.1)

	print("==========================")
	print(md)
	for i in range(10):
		print(ga.population[i])
