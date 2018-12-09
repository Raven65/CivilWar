# -*- coding: utf-8 -*-


class Battle():
	"""战场类
	"""

	def __init__(self, x, y, settings):
		self.fighter_x = x
		self.fighter_y = y
		self.round = settings.max_round

	def check_winner(self):
		"""检查是否分出胜负"""
		if self.round:  # 若战斗没结束
			if not self.fighter_x.hp or not self.fighter_y.hp:
				self.round = 0
			if not self.fighter_x.hp and not self.fighter_y.hp:  # 同归于尽
				print("They both died. There is no winner.")
				return 1
			elif not self.fighter_y.hp:
				print("%s died. The winner is %s." % (self.fighter_y.name, self.fighter_x.name))
				return 1
			elif not self.fighter_x.hp:
				print("%s died. The winner is %s." % (self.fighter_x.name, self.fighter_y.name))
				return 1
			return 0
		else:  # 回合已耗尽
			print("Time's up.")
			if self.fighter_x.hp > self.fighter_y.hp:
				print("The winner is %s." % self.fighter_x.name)
			elif self.fighter_x.hp == self.fighter_y.hp:
				print("There is no winner.")
			else:
				print("The winner is %s." % self.fighter_y.name)
			return 1
