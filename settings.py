# -*- coding: utf-8 -*-
import pygame
import common_function as cf
from button import Button


class Settings():
	"""全局设定类
	包含最大回合数，角色各属性边界，角色可用动作，评论长度等
	"""

	def __init__(self):
		self.max_hp = 20
		self.max_mp = 10
		self.max_shield = 10
		self.max_round = 40
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

		self.screen_width = 1280
		self.screen_height = 720
		self.bg_color = (230, 230, 230)
		self.mode_list = ["Easy", "Normal"]
		self.mode = 0

	def prep_draw(self, screen):
		self.set_hp = ChangeableVar(self, "max_hp", screen, screen.get_rect().centerx + 80,
									screen.get_rect().centery - 100)
		self.set_round = ChangeableVar(self, "max_round", screen, screen.get_rect().centerx + 80,
									   screen.get_rect().centery)
		self.set_mode = ChangeableVar(self, "mode", screen, screen.get_rect().centerx + 80,
									  screen.get_rect().centery + 100)
		self.button = Button(self, screen, "Done")
		self.button.rect.centery += 250

	def blitme(self):
		self.set_hp.blitme()
		self.set_mode.blitme()
		self.set_round.blitme()
		self.button.draw_button()

	def check_events(self, stats, battle, tony, steven, mouse_x, mouse_y):
		self.set_hp.check_event(mouse_x, mouse_y)
		self.set_mode.check_event(mouse_x, mouse_y)
		self.set_round.check_event(mouse_x, mouse_y)
		button_clicked = self.button.rect.collidepoint(mouse_x, mouse_y)
		if button_clicked:
			stats.game_state = 1
			battle.round = self.max_round
			tony.hp = self.max_hp
			steven.hp = self.max_hp


class ChangeableVar():
	def __init__(self, settings, name, screen, centerx, centery):
		self.left_button = pygame.image.load('sources/left_arrow.png')
		self.right_button = pygame.image.load('sources/right_arrow.png')
		self.left_rect = self.left_button.get_rect()
		self.right_rect = self.right_button.get_rect()
		self.left_rect.centery = centery
		self.right_rect.centery = centery
		self.left_rect.centerx = centerx - 80
		self.right_rect.centerx = centerx + 80
		self.screen = screen
		self.settings = settings
		self.name = name

	def blitme(self):
		self.screen.blit(self.left_button, self.left_rect)
		self.screen.blit(self.right_button, self.right_rect)
		if self.name == "mode":
			cf.drawText(self.screen, self.settings.mode_list[self.settings.mode], self.left_rect.centerx + 80,
						self.left_rect.centery, fontColor=(150, 0, 0))
		else:
			cf.drawText(self.screen, str(getattr(self.settings, self.name)), self.left_rect.centerx + 80,
						self.left_rect.centery, fontColor=(150, 0, 0))
		cf.drawText(self.screen, self.name.replace("_", " ").title(), self.left_rect.centerx - 120,
					self.left_rect.centery, fontColor=(150, 0, 0))

	def check_event(self, mouse_x, mouse_y):
		left_button_clicked = self.left_rect.collidepoint(mouse_x, mouse_y)
		right_button_clicked = self.right_rect.collidepoint(mouse_x, mouse_y)
		x = getattr(self.settings, self.name)
		if left_button_clicked:
			if self.name != "mode" and x > 1:
				setattr(self.settings, self.name, x - 1)
			elif self.name == "mode" and x > 0:
				setattr(self.settings, self.name, x - 1)
		if right_button_clicked:
			if self.name != "mode":
				setattr(self.settings, self.name, x + 1)
			elif x < 1:
				setattr(self.settings, self.name, x + 1)
