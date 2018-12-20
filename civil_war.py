# -*- coding: utf-8 -*-

from settings import Settings
from fighter import Fighter
from battle import Battle
from button import Button
from game_stats import GameStat
from background import Background
import fight_engine as fn
import common_function as cf
import pygame

if __name__ == '__main__':

	tony_mode = "minimax"
	steven_mode = "random"

	# 初始化
	settings = Settings()
	pygame.init()
	screen = pygame.display.set_mode(
		(settings.screen_width, settings.screen_height))
	pygame.display.set_caption("Civil War of the Avengers")

	play_button = Button(settings, screen, "Play")

	bg = Background(settings,screen)
	stats = GameStat(settings)

	tony = Fighter("Tony Stark", settings, screen)
	steven = Fighter("Steven Rogers", settings, screen)
	steven.mp += 3
	battle = Battle(tony, steven, settings)
	while True:


		cf.check_events(settings, screen, stats, bg, tony, steven, play_button)
		cf.update_screen(settings, screen, stats, bg, tony, steven, play_button)

# # 获取战斗策略
# tony_act = tony.fight_strategy(steven, tony_mode, 50)
# # 进行战斗
# fn.fight_function[tony_act](tony, steven)
# # 键盘输出
# # cf.keyboard_output(settings, tony, steven, tony_act, 1)
# winner = battle.check_winner()
# # if winner:
# # 	break
# # 获取战斗策略
# steven_act = steven.fight_strategy(tony, steven_mode, 50)
# # 进行战斗
# fn.fight_function[steven_act](steven, tony)
# # 键盘输出
# # cf.keyboard_output(settings, tony, steven, steven_act, 0)
# # 判断胜负
# battle.round -= 1
# winner = battle.check_winner()
# # if winner:
# # 	break
