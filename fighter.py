# -*- coding: utf-8 -*-
import random
import common_function as cf
import copy
import fight_engine as fn
import pygame
from pygame.sprite import Sprite
from action_bar import ActionBar


class Fighter(Sprite):
	"""战斗者类
	"""

	def __init__(self, name, settings, screen):
		super().__init__()
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

		self.screen = screen

		self.been_hit = False
		self.hit = pygame.image.load("sources/boom.png")
		self.hit_rect = self.hit.get_rect()

		self.load_image(2)
		self.point_me = False
		self.mode = "easy"
		self.action_bar = ActionBar(settings, screen, self)



	def reset(self, settings):
		self.hp = settings.max_hp
		self.mp = 0
		self.shield = 0
		self.counter = 0
		self.max_hp = settings.max_hp
		self.max_mp = settings.max_mp
		self.max_shield = settings.max_shield
		self.point_me = False
		self.mode = settings.mode
		self.load_image(2)

	def load_image(self, game_state):
		if game_state == 2:
			self.image = pygame.image.load('sources/' + self.name + '_2.png')
			self.rect = self.image.get_rect()
			self.rect.center = self.screen.get_rect().center
			if self.name == "Steven Rogers":
				self.rect.centerx -= 250
			else:
				self.rect.centerx += 250
			self.rect.centery += 100
		elif game_state == 3:
			self.image = pygame.image.load('sources/' + self.name + '_3.png')
			self.rect = self.image.get_rect()
			self.rect.center = self.screen.get_rect().center
			if self.name == "Steven Rogers":
				self.rect.centerx -= 350
			else:
				self.rect.centerx += 350
			self.rect.centery += 85
		elif game_state == 5:
			self.image = pygame.image.load('sources/' + self.name + '_5.png')
			self.rect = self.image.get_rect()
			self.rect.center = self.screen.get_rect().center
			if self.name == "Steven Rogers":
				self.rect.centerx -= 300
			else:
				self.rect.centerx += 300
			self.rect.centery += 85
		self.x = float(self.rect.x)
		self.hit_rect.center = self.rect.center
		self.hit_rect.centery = self.rect.centery - 20
	def blitme(self):
		if self.counter:
			pygame.draw.circle(self.screen, (51, 153, 230), self.rect.center, 120, 10)
		self.screen.blit(self.image, self.rect)
		if self.point_me:
			pygame.draw.rect(self.screen, [200, 0, 0], self.rect, 5)
		if self.been_hit:
			self.screen.blit(self.hit, self.hit_rect)

	def update(self):
		"""防止属性变化超过边界"""
		self.hp = max(self.hp, 0)
		self.mp = min(self.mp, self.max_mp)
		self.shield = min(self.shield, self.max_shield)

	def act(self, battle, enemy, p=50):
		if self.mode == "User":
			if battle.waiting == self and self.action_bar.choose != "do nothing":
				temp = self.action_bar.choose
				self.action_bar.choose = "do nothing"
				return temp
			else:
				return "do nothing"
		else:
			if battle.waiting == self:
				return self.fight_strategy(enemy, p)
			else:
				return "do nothing"

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
			return self.minimax(self, enemy, 0, 8, -30, 30)[1];
		if self.mode == "Hard":
			return self.ga_strategy(self, enemy)

	# if self.mode == "User":
	# 	# 询问用户键盘输入操作指令
	# 	act_intro = "(" + "".join([" %s:%s," % (str(value), key) for key, value in self.actions.items() if
	# 							   str(value) in self.act_command]).strip().strip(",") + ")"
	# 	action = cf.choose_input("Choose your next move for %s" % self.name, self.act_command, act_intro)
	# 	# 对特殊技能做判断，若不满足条件则待机
	# 	if int(action) == self.actions["counter attack"] and self.mp < 4:
	# 		print("You can't counter attack now (Your mp is below 4.), you will do nothing in this round.")
	# 		return "do nothing"
	# 	if int(action) == self.actions["super attack"] and self.mp < 6:
	# 		print("You can't super attack now (Your mp is below 4.), you will do nothing in this round.")
	# 		return "do nothing"
	# 	new_action_dict = {v: k for k, v in self.actions.items()}
	# 	return new_action_dict[int(action)]

	def minimax(self, a, b, player, round, alpha, beta):
		if round < 0:
			return [self.eva(a, b), "do nothing"]
		if a.hp <= 0 or b.hp <= 0:
			return [self.eva(a, b), "do nothing"]
		if player == 0:
			move = ["attack", "defend"]
			if a.mp >= 4:
				move.append("counter attack")
			if a.mp >= 6:
				move.append("super attack")
			best_move = move[0]
			for x in move:
				temp_a = TempFighter(a)
				temp_b = TempFighter(b)
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
				temp_a = TempFighter(a)
				temp_b = TempFighter(b)
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
		p = random.randint(1, 10)
		if p <= 5:
			return a.hp - b.hp
		elif p <= 7:
			return a.hp + a.shield - b.hp - b.shield
		elif p <= 9:
			return a.hp + a.mp - b.hp - b.mp
		elif p == 10:
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
		r = random.randint(0, 4)
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


class TempFighter():
	def __init__(self, fighter):
		self.name = fighter.name
		self.hp = fighter.hp
		self.mp = fighter.mp
		self.shield = fighter.shield
		self.counter = fighter.counter
		self.max_hp = fighter.max_hp
		self.max_mp = fighter.max_mp
		self.max_shield = fighter.max_shield
		self.act_command = fighter.act_command
		self.actions = fighter.actions

	def update(self):
		self.hp = max(self.hp, 0)
		self.mp = min(self.mp, self.max_mp)
		self.shield = min(self.shield, self.max_shield)
