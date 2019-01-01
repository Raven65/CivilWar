# -*- coding: utf-8 -*-
from button import Button


class ActionBar():
	def __init__(self, settings, screen, fighter):
		self.fighter = fighter
		self.actions = ["attack", "defend", "counter attack", "super attack"]
		self.actions_flag = [1, 1, 0, 0]

		self.settings = settings
		self.screen = screen
		self.actions_buttons = []
		self.prep()
		self.choose = "do nothing"

	def prep(self):
		if self.fighter.name == "Steven Rogers":
			x = -480
		else:
			x = 480

		for i, action in enumerate(self.actions):
			if self.actions_flag[i]:
				self.actions_buttons.append(
					Button(self.settings, self.screen, action, width=150, height=40, font_height=24,
						   button_color=(140, 0, 0), x=x,
						   y=- 170 + i * 50))
			else:
				self.actions_buttons.append(
					Button(self.settings, self.screen, action, width=150, height=40, font_height=24,
						   button_color=(40, 40, 40), x=x,
						   y=- 170 + i * 50))

	def blitme(self):
		if self.fighter.mp >= 6:
			self.actions_flag[3] = 1
		else:
			self.actions_flag[3] = 0
		if self.fighter.mp >= 4:
			self.actions_flag[2] = 1
		else:
			self.actions_flag[2] = 0

		for i, action_button in enumerate(self.actions_buttons):
			if i >= 2:
				if self.actions_flag[i]:
					action_button.button_color = (140, 0, 0)
					action_button.prep_msg()
				else:
					action_button.button_color = (40, 40, 40)
					action_button.prep_msg()
			action_button.draw_button()

	def check_point(self, mouse_x, mouse_y):
		for action_button in self.actions_buttons:
			action_button.check_point(mouse_x, mouse_y)

	def check_choose(self, stats, mouse_x, mouse_y):
		for i, action_button in enumerate(self.actions_buttons):
			action_button_choose = action_button.rect.collidepoint(mouse_x, mouse_y)
			if action_button_choose and self.actions_flag[i]:
				self.choose = action_button.msg
