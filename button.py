import pygame.font


class Button():
	def __init__(self, settings, screen, msg, button_color=(160, 0, 0), text_color=(255, 255, 255)):
		self.screen = screen
		self.screen_rect = screen.get_rect()

		self.width, self.height = 200, 50
		self.button_color = button_color
		self.text_color = text_color
		self.font = pygame.font.Font("No-move.ttf", 32)

		self.rect = pygame.Rect(0, 0, self.width, self.height)
		self.rect.center = self.screen_rect.center

		self.prep_msg(msg)

	def prep_msg(self, msg):
		self.msg_image = self.font.render(msg, True, self.text_color,
										  self.button_color)
		self.msg_image_rect = self.msg_image.get_rect()
		self.msg_image_rect.center = self.rect.center

	def draw_button(self):
		self.msg_image_rect.center = self.rect.center
		self.screen.fill(self.button_color, self.rect)
		self.screen.blit(self.msg_image, self.msg_image_rect)
