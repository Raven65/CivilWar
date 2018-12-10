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
		self.hp = settings.max_hp
		self.mp = 0
		self.cd = 0
		self.max_hp = settings.max_hp
		self.max_mp = settings.max_mp
		self.act_command = [str(x) for x in range(settings.min_act, settings.max_act + 1)]
		self.actions = settings.actions

	def update(self):
		"""防止属性变化超过边界"""
		self.cd = max(self.cd, 0)
		self.hp = max(self.hp, 0)
		self.mp = min(self.mp, self.max_mp)

	def fight_strategy(self, enemy, mode):
		"""战斗策略选择
		Args:
			enemy: 敌人
			auto: 是否自动
		Returns:
			action: 返回战斗动作，字符串
		"""
		while mode == "random":  # 自动战斗
			action = random.randint(1, 300)
			if not self.cd:
				if action > 100:
					continue
				else:
					return "counter attack"
			if self.mp == 4:
				if action > 100:
					continue
				else:
					return "super attack"
			if action > 50:
				return "defend"
			else:
				return "attack"
		if mode == "minimax":
			return self.minimax(enemy, 0, "stand by")
		# 询问用户键盘输入操作指令
		if mode == "user":

			act_intro = "(" + "".join([" %s:%s," % (str(value), key) for key, value in self.actions.items() if
									   str(value) in self.act_command]).strip().strip(",") + ")"
			action = cf.choose_input("Choose your next move for %s" % self.name, self.act_command, act_intro)
			# 对特殊技能做判断，若不满足条件则待机
			if int(action) == self.actions["counter attack"] and self.cd != 0:
				print("You can't counter attack now (Your cd is not 0.), you will do nothing in this round.")
				return "do nothing"
			if int(action) == self.actions["super attack"] and self.mp != 4:
				print("You can't super attack now (Your mp is not 4.), you will do nothing in this round.")
				return "do nothing"
			new_action_dict = {v: k for k, v in self.actions.items()}
			return new_action_dict[int(action)]

	def minimax(self, enemy, player, enemy_move):

		max_val = -30
		min_val = 30
		if player == 0:
			move = ["attack", "defend"]
			if not self.cd:
				move.append("counter attack")
			if self.mp == 4:
				move.append("super attack")
			for x in move:
				temp_a = copy.deepcopy(self)
				temp_b = copy.deepcopy(enemy)
				enemy_move = self.minimax(enemy, 1, x)
				fn.fight_function[x](temp_a, temp_b, enemy_move)
				fn.fight_function[enemy_move](temp_b, temp_a, x)
				val = temp_a.hp - temp_b.hp
				if val >= max_val:
					max_val = val
					best_move = x
				del temp_a
				del temp_b
		elif player == 1:
			move = ["attack", "defend"]
			if not enemy.cd:
				move.append("counter attack")
			if enemy.mp == 4:
				move.append("super attack")
			for x in move:
				temp_a = copy.deepcopy(self)
				temp_b = copy.deepcopy(enemy)
				fn.fight_function[x](temp_b, temp_a, enemy_move)
				fn.fight_function[enemy_move](temp_a, temp_b, x)
				val = temp_a.hp - temp_b.hp
				if val <= min_val:
					min_val = val
					best_move = x
				del temp_a
				del temp_b
		return best_move
