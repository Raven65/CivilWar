import pygame.font
import sys


class Button():
	def __init__(self, settings, screen, msg, font_height=32, width=200, height=50, x=0, y=0, button_color=(160, 0, 0),
				 text_color=(255, 255, 255)):
		self.screen = screen
		self.screen_rect = screen.get_rect()

		self.width, self.height = width, height
		self.button_color = button_color
		self.text_color = text_color
		self.font = pygame.font.Font("No-move.ttf", font_height)

		self.rect = pygame.Rect(0, 0, self.width, self.height)
		self.rect.center = (self.screen_rect.centerx + x, self.screen_rect.centery + y)
		self.point_me = False
		self.msg = msg
		self.prep_msg()

	def prep_msg(self):
		self.msg_image = self.font.render(self.msg, True, self.text_color,
										  self.button_color)
		self.msg_image_rect = self.msg_image.get_rect()
		self.msg_image_rect.center = self.rect.center

	def draw_button(self):
		self.msg_image_rect.center = self.rect.center
		self.screen.fill(self.button_color, self.rect)
		self.screen.blit(self.msg_image, self.msg_image_rect)
		if self.point_me:
			pygame.draw.rect(self.screen, [240, 240, 240], self.rect, 5)

	def check_point(self, mouse_x, mouse_y):
		point = self.rect.collidepoint(mouse_x, mouse_y)
		if point:
			self.point_me = True
		else:
			self.point_me = False
