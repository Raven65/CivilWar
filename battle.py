# -*- coding: utf-8 -*-


class Battle():
	"""战场类
	"""

	def __init__(self, x, y, settings):
		self.fighter_x = x
		self.fighter_y = y
		self.waiting = x
		self.round = settings.max_round
		self.winner = 0
	def reset(self, settings):
		self.waiting = self.fighter_x
		self.round = settings.max_round
		self.winner = 0

	def check_winner(self):
		"""检查是否分出胜负"""
		if self.round:  # 若战斗没结束
			if not self.fighter_x.hp or not self.fighter_y.hp:
				self.round = 0
			if not self.fighter_x.hp and not self.fighter_y.hp:  # 同归于尽
				print("They both died. There is no winner.")
				self.winner = 3
				return 3
			elif not self.fighter_y.hp:
				print("%s died. The winner is %s." % (self.fighter_y.name, self.fighter_x.name))
				self.winner = 1
				return 1
			elif not self.fighter_x.hp:
				print("%s died. The winner is %s." % (self.fighter_x.name, self.fighter_y.name))
				self.winner = 2
				return 2
			return 0
		else:  # 回合已耗尽
			print("Time's up.")
			if self.fighter_x.hp > self.fighter_y.hp:
				print("The winner is %s." % self.fighter_x.name)
				self.winner = 1
				return 1
			elif self.fighter_x.hp == self.fighter_y.hp:
				self.winner = 3
				print("There is no winner.")
				return 3
			else:
				print("The winner is %s." % self.fighter_y.name)
				self.winner = 2
				return 2
