# -*- coding: utf-8 -*-
import random
import common_function as cf
import copy
import fight_engine as fn


class Fighter():
	"""战斗者类
	"""

	def __init__(self, name, settings):
		self.name = name
		self.settings = settings
		self.hp = settings.max_hp
		self.mp = 0
		self.shield = 0
		self.counter = 0
		self.max_hp = settings.max_hp
		self.max_mp = settings.max_mp
		self.max_shield = settings.max_shield
		self.act_command = [str(x) for x in range(settings.min_act, settings.max_act + 1)]
		self.actions = settings.actions

	def update(self):
		"""防止属性变化超过边界"""
		self.hp = max(self.hp, 0)
		self.mp = min(self.mp, self.max_mp)
		self.shield = min(self.shield, self.max_shield)

	def fight_strategy(self, enemy, mode, p=50):
		"""战斗策略选择
		Args:
			enemy: 敌人
			auto: 是否自动
		Returns:
			action: 返回战斗动作，字符串
		"""
		while mode == "random":  # 自动战斗
			action = random.randint(1, 100)
			if self.mp >= 6:
				if action > 50:
					return "super attack"
			elif self.mp >= 4:
				if action <= 50:
					return "counter attack"
			if action > p:
				return "defend"
			else:
				return "attack"
		if mode == "minimax":
			return self.minimax(self, enemy, 0, 4, -30, 30)[1];
		if mode == "minimax_random":
			return self.minimax_random_eva(self, enemy, 0, 4, -30, 30)[1];
		if mode == "ga":
			return self.ga_strategy(self,enemy)
		if mode == "user":
			# 询问用户键盘输入操作指令
			act_intro = "(" + "".join([" %s:%s," % (str(value), key) for key, value in self.actions.items() if
									   str(value) in self.act_command]).strip().strip(",") + ")"
			action = cf.choose_input("Choose your next move for %s" % self.name, self.act_command, act_intro)
			# 对特殊技能做判断，若不满足条件则待机
			if int(action) == self.actions["counter attack"] and self.mp < 4:
				print("You can't counter attack now (Your mp is below 4.), you will do nothing in this round.")
				return "do nothing"
			if int(action) == self.actions["super attack"] and self.mp < 6:
				print("You can't super attack now (Your mp is below 4.), you will do nothing in this round.")
				return "do nothing"
			new_action_dict = {v: k for k, v in self.actions.items()}
			return new_action_dict[int(action)]

	def minimax(self, a, b, player, round, alpha, beta):
		if round < 0:
			return [a.hp - b.hp, ""]
		if a.hp <= 0 or b.hp <= 0:
			return [a.hp - b.hp, ""]
		if player == 0:
			move = ["attack", "defend"]
			if a.mp >= 4:
				move.append("counter attack")
			if a.mp >= 6:
				move.append("super attack")
			best_move = move[0]
			for x in move:
				temp_a = copy.deepcopy(a)
				temp_b = copy.deepcopy(b)
				fn.fight_function[x](temp_a, temp_b)
				res = self.minimax(temp_a, temp_b, 1, round - 1, alpha, beta)
				if res[0] > alpha:
					alpha = res[0]
					best_move = x
				if alpha >= beta:
					return [alpha, best_move]
				del temp_a
				del temp_b
			return [alpha, best_move]
		elif player == 1:
			move = ["attack", "defend"]
			if b.mp >= 4:
				move.append("counter attack")
			if b.mp >= 6:
				move.append("super attack")
			best_move = move[0]
			for x in move:
				temp_a = copy.deepcopy(a)
				temp_b = copy.deepcopy(b)
				fn.fight_function[x](temp_b, temp_a)
				res = self.minimax(temp_a, temp_b, 0, round - 1, alpha, beta)
				if res[0] < beta:
					beta = res[0]
					best_move = x
				if alpha >= beta:
					return [beta, best_move]
				del temp_a
				del temp_b
			return [beta, best_move]

	def minimax_random_eva(self, a, b, player, round, alpha, beta):
		if round < 0:
			return [self.eva(a, b), ""]
		if a.hp <= 0 or b.hp <= 0:
			return [self.eva(a, b), ""]
		if player == 0:
			move = ["attack", "defend"]
			if a.mp >= 4:
				move.append("counter attack")
			if a.mp >= 6:
				move.append("super attack")
			best_move = move[0]
			for x in move:
				temp_a = copy.deepcopy(a)
				temp_b = copy.deepcopy(b)
				fn.fight_function[x](temp_a, temp_b)
				res = self.minimax(temp_a, temp_b, 1, round - 1, alpha, beta)
				if res[0] > alpha:
					alpha = res[0]
					best_move = x
				if alpha >= beta:
					return [alpha, best_move]
				del temp_a
				del temp_b
			return [alpha, best_move]
		elif player == 1:
			move = ["attack", "defend"]
			if b.mp >= 4:
				move.append("counter attack")
			if b.mp >= 6:
				move.append("super attack")
			best_move = move[0]
			for x in move:
				temp_a = copy.deepcopy(a)
				temp_b = copy.deepcopy(b)
				fn.fight_function[x](temp_b, temp_a)
				res = self.minimax(temp_a, temp_b, 0, round - 1, alpha, beta)
				if res[0] < beta:
					beta = res[0]
					best_move = x
				if alpha >= beta:
					return [beta, best_move]
				del temp_a
				del temp_b
			return [beta, best_move]

	def eva(self, a, b):
		p = random.randint(1, 4)
		if p == 1:
			return a.hp - b.hp
		elif p == 2:
			return a.hp + a.shield - b.hp - b.shield
		elif p == 3:
			return a.hp + a.mp - b.hp - b.mp
		elif p == 4:
			return a.hp + a.shield + a.mp - b.hp - b.mp - b.shield

	def ga_strategy(self, a, b):
		x = []
		x.append(a.hp / self.settings.max_hp)
		x.append(-b.hp / self.settings.max_hp)
		x.append(a.mp / self.settings.max_mp)
		x.append(-b.mp / self.settings.max_mp)
		x.append(a.shield / self.settings.max_shield)
		x.append(-b.shield / self.settings.max_shield)
		x.append(a.counter / 2)
		x.append(-b.counter / 2)
		sum = 0
		w = [[0.05281437564686202, 0.14945444383419904, 0.061709333866210504, 0.0336483111216646, 0.1954766897701734,
			  0.09447417464023114, 0.030291538332920368, 0.3821311327877388],
			 [0.062037083485515974, 0.09135377376095986, 0.03959110584785366, 0.09276071723180201, 0.16587356281164065,
			  0.0891051796191564, 0.06410612998226826, 0.3951724472608032],
			 [0.043508262346743376, 0.09781163425196711, 0.04778460845263359, 0.02605556195967209, 0.1516258718636814,
			  0.08145150027715191, 0.1609901199716359, 0.3907724408765147],
			 [0.055929239716951226, 0.1117450664854627, 0.04613923439642408, 0.020434184520557203, 0.11871046763056185,
			  0.057372945407143085, 0.2573095466473337, 0.3323593151955663],
			 [0.07306690549243638, 0.10759592777000697, 0.04663016742238634, 0.1092530173661229, 0.19536488913895392,
			  0.10494754705287737, 0.07550381606823663, 0.28763772968897944]]
		t = -0.0365201790437496
		r = random.randint(0,4)
		for i in range(8):
			sum += x[i] * w[r][i]
		if sum > t:
			if a.mp < 6:
				return "attack"
			else:
				return "super attack"
		else:
			if a.mp < 4 or a.counter:
				return "defend"
			else:
				return "counter attack"
