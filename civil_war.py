# -*- coding: utf-8 -*-

from settings import Settings
from fighter import Fighter
from battle import Battle
from button import Button
from game_stats import GameStat
from background import Background
from bar import Bar
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
	settings.prep_draw(screen)

	play_button = Button(settings, screen, "Play", y=-30)
	settings_button = Button(settings, screen, "Settings", y=30)
	return_button = Button(settings,screen,"Return to Menu",width=300)
	bg = Background(settings, screen)
	stats = GameStat(settings)
	bar = Bar(settings, screen)
	tony = Fighter("Tony Stark", settings, screen)
	steven = Fighter("Steven Rogers", settings, screen)
	tony.mp += 3
	battle = Battle(steven, tony, settings)

	while True:
		cf.check_events(settings, screen, stats, bg, battle, tony, steven, play_button, settings_button, return_button)
		if stats.game_state == 3:
			if battle.waiting == steven:
				steven_act = steven.act(battle, tony, 50)
				fn.fight_function[steven_act](steven, tony)
				if steven_act != "do nothing":
					battle.waiting = tony
					cf.keyboard_output(settings, steven, tony, steven_act, 1)

			elif battle.waiting == tony:
				tony_act = tony.act(battle, steven, 50)
				fn.fight_function[tony_act](tony, steven)
				if tony_act != "do nothing":
					battle.waiting = steven
					battle.round -= 1
					cf.keyboard_output(settings, steven, tony, tony_act, 0)
			if battle.check_winner():
				stats.game_state = 4

		cf.update_screen(settings, screen, stats, bg, bar, battle, tony, steven, play_button, settings_button,return_button)

# TODO:加入战斗动画
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
