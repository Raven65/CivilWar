# -*- coding: utf-8 -*-
import pygame
import common_function as cf


class Bar():
	def __init__(self, settings, screen):
		self.screen = screen
		self.settings = settings
		self.center_x = self.screen.get_rect().centerx
		self.center_y = self.screen.get_rect().centery
		self.x_icon = pygame.image.load('sources/sr_icon.png')
		self.y_icon = pygame.image.load('sources/ts_icon.png')
		self.x_icon_rect = self.x_icon.get_rect()
		self.y_icon_rect = self.y_icon.get_rect()
		self.x_icon_rect.centerx = self.center_x - 500
		self.y_icon_rect.centerx = self.center_x + 500
		self.x_icon_rect.centery = self.center_y - 250
		self.y_icon_rect.centery = self.center_y - 250

		self.x_hp_rect = pygame.Rect(0, 0, 350, 40)
		self.y_hp_rect = pygame.Rect(0, 0, 350, 40)
		self.x_hp_rect.centerx = self.center_x - 250
		self.x_hp_rect.centery = self.center_y - 250
		self.y_hp_rect.centerx = self.center_x + 250
		self.y_hp_rect.centery = self.center_y - 250

		self.shield = pygame.image.load('sources/shield.png')
		self.shield_rect = self.shield.get_rect()

		self.counter = pygame.image.load('sources/counter_1.png')
		self.counter_rect = self.counter.get_rect()
		self.counter.set_alpha(200)

	def blitme(self, x, y):
		self.screen.blit(self.x_icon, self.x_icon_rect)
		self.screen.blit(self.y_icon, self.y_icon_rect)

		self.blit_hp(x, y)
		self.blit_mp(x, y)
		self.blit_shield(x, y)

	def blit_hp(self, x, y):
		pygame.draw.rect(self.screen, [210, 10, 10], self.x_hp_rect, 3)
		pygame.draw.rect(self.screen, [210, 10, 10], self.y_hp_rect, 3)

		x_hp_rect = pygame.Rect(0, 0, 340 * x.hp / self.settings.max_hp, 30)
		x_hp_rect.center = self.x_hp_rect.center
		x_hp_rect.left = self.x_hp_rect.left +3
		pygame.draw.rect(self.screen, [210, 30, 30], x_hp_rect, 0)
		cf.drawText(self.screen, str(x.hp), x_hp_rect.centerx, x_hp_rect.centery, textHeight=40,
					fontColor=(255, 255, 255))

		y_hp_rect = pygame.Rect(0, 0, 340 * y.hp / self.settings.max_hp, 30)
		y_hp_rect.center = self.y_hp_rect.center
		y_hp_rect.right = self.y_hp_rect.right -3
		pygame.draw.rect(self.screen, [210, 30, 30], y_hp_rect, 0)
		cf.drawText(self.screen, str(y.hp), y_hp_rect.centerx, y_hp_rect.centery, textHeight=40,
					fontColor=(255, 255, 255))

	def blit_mp(self, x, y):
		for i in range(self.settings.max_mp):
			pygame.draw.circle(self.screen, [0, 100, 190], [self.center_x - 400 + i * 30, 150], 10, 2)
			pygame.draw.circle(self.screen, [0, 100, 190], [self.center_x + 400 - i * 30, 150], 10, 2)
		for i in range(x.mp):
			pygame.draw.circle(self.screen, [0, 100, 210], [self.center_x - 400 + i * 30, 150], 7, 0)
		for i in range(y.mp):
			pygame.draw.circle(self.screen, [0, 100, 210], [self.center_x + 400 - i * 30, 150], 7, 0)

	def blit_shield(self, x, y):

		self.shield_rect.centery = 70
		for i in range(x.shield):
			self.shield_rect.centerx = self.center_x - 400 + i * 25
			self.screen.blit(self.shield, self.shield_rect)
		for i in range(y.shield):
			self.shield_rect.centerx = self.center_x + 400 - i * 25
			self.screen.blit(self.shield, self.shield_rect)


