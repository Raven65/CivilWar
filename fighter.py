# -*- coding: utf-8 -*-
import random
import common_function as cf
import copy
import fight_engine as fn
import pygame
from pygame.sprite import Sprite

class Fighter(Sprite):
	"""战斗者类
	"""

	def __init__(self, name, settings, screen):
		super().__init__()
		self.name = name
		self.hp = settings.max_hp
		self.mp = 0
		self.shield = 0
		self.counter = 0
		self.max_hp = settings.max_hp
		self.max_mp = settings.max_mp
		self.max_shield = settings.max_shield
		self.act_command = [str(x) for x in range(settings.min_act, settings.max_act + 1)]
		self.actions = settings.actions

		self.screen = screen
		self.load_image(2)
		self.point_me = False
		self.mode = "easy"


	def load_image(self,game_state):
		if game_state==2:
			self.image = pygame.image.load('sources/'+self.name+'_2.png')
			self.rect = self.image.get_rect()
			self.rect.center=self.screen.get_rect().center
			if self.name == "Steven Rogers":
				self.rect.centerx -=250
			else:
				self.rect.centerx +=250
			self.rect.centery += 100
		elif game_state == 3:
			self.image = pygame.image.load('sources/' + self.name + '_3.png')
			self.rect = self.image.get_rect()
			self.rect.center = self.screen.get_rect().center
			if self.name == "Steven Rogers":
				self.rect.centerx -= 350
			else:
				self.rect.centerx += 350
			self.rect.centery += 75
		self.x = float(self.rect.x)

	def blitme(self):
		self.screen.blit(self.image, self.rect)
		if self.point_me:
			pygame.draw.rect(self.screen, [200, 0, 0], self.rect, 5)

	def update(self):
		"""防止属性变化超过边界"""
		self.hp = max(self.hp, 0)
		self.mp = min(self.mp, self.max_mp)
		self.shield = min(self.shield, self.max_shield)

	def fight_strategy(self, enemy, p=50):
		"""战斗策略选择
		Args:
			enemy: 敌人
			auto: 是否自动
		Returns:
			action: 返回战斗动作，字符串
		"""
		while self.mode == "Easy":  # 自动战斗
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
		if self.mode == "Normal":
			return self.minimax(self, enemy, 0, 4, -30, 30)[1];
		if self.mode == "User":
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
			return [a.hp - b.hp, "do nothing"]
		if a.hp <= 0 or b.hp <= 0:
			return [a.hp - b.hp, "do nothing"]
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
