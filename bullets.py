# -*- coding: utf-8 -*-
import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):

	def __init__(self, settings, screen, key, steven, tony):
		super().__init__()
		self.screen = screen
		self.key = key
		self.flag = False
		if key == "t":
			self.fighter = tony
			self.rect = pygame.Rect(0, 0, 20, 30)
			self.rect.centery = tony.rect.centery - 40
			self.rect.right = tony.rect.left
			self.x = float(self.rect.x)

			self.color = (255, 0, 51)
			self.speed_factor = 30
			self.partner = pygame.image.load('sources/wm.png')
			self.partner_rect = self.partner.get_rect()
			self.partner_rect.center = tony.rect.center
			self.partner_rect.centerx += 200
			self.temp_rect = pygame.Rect(0, 0, self.rect.width, self.rect.height)
			self.temp_rect.center = self.rect.center
			self.temp_rect.centery += 30

		elif key == "s":

			self.fighter = steven
			self.bullet = pygame.image.load('sources/sr_bullet.png')
			self.rect = self.bullet.get_rect()
			self.rect.centery = steven.rect.centery - 50
			self.rect.left = steven.rect.right
			self.speed_factor = 20
			self.partner = pygame.image.load('sources/ws.png')
			self.partner_rect = self.partner.get_rect()
			self.partner_rect.center = self.rect.center
			self.partner_rect.centerx -= 70

	def update(self):
		if self.key == "t":
			self.rect.width += self.speed_factor
			self.rect.right = self.fighter.rect.left
		elif self.key == "s":
			self.rect.x += self.speed_factor
			self.partner_rect.x += self.speed_factor

	def reset(self):
		if self.key == "t":
			self.rect.width = 20
			self.rect.right = self.fighter.rect.left
		elif self.key == "s":
			self.rect.left = self.fighter.rect.right
			self.partner_rect.center = self.rect.center
			self.partner_rect.centerx -= 70
		self.flag = False

	def draw_bullet(self):
		if self.key == "t":
			pygame.draw.rect(self.screen, self.color, self.rect)
			if self.flag:
				self.screen.blit(self.partner, self.partner_rect)
				self.temp_rect.width = self.rect.width
				self.temp_rect.right = self.fighter.rect.left
				pygame.draw.rect(self.screen, (51, 153, 255), self.temp_rect)
		else:
			self.screen.blit(self.bullet, self.rect)
			if self.flag:
				self.screen.blit(self.partner, self.partner_rect)
