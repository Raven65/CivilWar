# -*- coding: utf-8 -*-
import pygame


class Background():
	def __init__(self, settings, screen):
		self.screen = screen
		self.title = pygame.image.load('sources/title.jpg')
		self.title_rect = self.title.get_rect()
		self.icon = pygame.image.load('sources/icon.png')
		self.icon_rect = self.icon.get_rect()
		self.icon_rect.centerx = screen.get_rect().centerx
		self.icon_rect.centery = 100
		self.bg_rect = pygame.Rect(0, 0, 1152, 648)
		self.bg_rect.center = screen.get_rect().center
		self.bg = pygame.image.load('sources/bg.jpg')
		self.bg.set_alpha(200)

	def blitme(self, stats):
		self.screen.blit(self.title, self.title_rect)
		if stats.game_state != 1:
			self.screen.blit(self.bg, self.bg_rect)
			self.screen.blit(self.icon, self.icon_rect)
			pygame.draw.rect(self.screen, [200, 0, 0], self.bg_rect, 5)
