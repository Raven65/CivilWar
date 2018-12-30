# -*- coding: utf-8 -*-
class GameStat():
	def __init__(self, settings):
		self.settings = settings
		self.game_state = 1

	def reset_games(self,settings, bg, battle, tony, steven):
		battle.reset(settings)
		bg.reset()
		steven.reset(settings)
		tony.reset(settings)
		tony.mp +=3
		self.game_state =1
