# -*- coding: utf-8 -*-

from settings import Settings
from fighter import Fighter
from battle import Battle
from button import Button
from game_stats import GameStat
from background import Background
from bar import Bar
from bullets import Bullet
import fight_engine as fn
import common_function as cf
import pygame

if __name__ == '__main__':

	tony_mode = "minimax"
	steven_mode = "random"

	# 初始化
	settings = Settings()
	pygame.init()
	pygame.mixer.init()
	s_hit_sound = pygame.mixer.Sound("sources/s_hit.wav")
	s_hit_sound.set_volume(0.2)
	t_hit_sound = pygame.mixer.Sound("sources/t_hit.wav")
	t_hit_sound.set_volume(0.2)
	press_sound = pygame.mixer.Sound("sources/press.wav")
	press_sound.set_volume(0.4)
	pygame.mixer.music.load("sources/Angels Will Rise.mp3")
	pygame.mixer.music.set_volume(0.2)
	screen = pygame.display.set_mode(
		(settings.screen_width, settings.screen_height))
	pygame.display.set_caption("Civil War of the Avengers")
	settings.prep_draw(screen)

	play_button = Button(settings, screen, "Play", y=-30)
	settings_button = Button(settings, screen, "Settings", y=30)
	return_button = Button(settings, screen, "Return to Menu", width=300)
	bg = Background(settings, screen)
	stats = GameStat(settings)
	bar = Bar(settings, screen)
	tony = Fighter("Tony Stark", settings, screen)
	steven = Fighter("Steven Rogers", settings, screen)
	tony_bullets = Bullet(settings, screen, "t", steven, tony)
	steven_bullets = Bullet(settings, screen, "s", steven, tony)
	tony.mp += 3
	battle = Battle(steven, tony, settings)
	act = ""
	while True:
		cf.check_events(settings, screen, stats, bg, battle, tony, steven, play_button, settings_button, return_button,press_sound)
		if pygame.mixer.music.get_busy() == False:
			pygame.mixer.music.play()
		if stats.game_state == 3:
			if battle.waiting == steven:
				pygame.time.wait(50)
				steven_act = steven.act(battle, tony, 50)

				if steven_act != "do nothing":
					if steven_act == "attack" or steven_act == "super attack":
						steven.load_image(5)
					act = steven_act
					stats.game_state = 5
					battle.waiting = tony
					cf.keyboard_output(settings, steven, tony, steven_act, 1)

			elif battle.waiting == tony:
				pygame.time.wait(50)
				tony_act = tony.act(battle, steven, 50)
				if tony_act != "do nothing":
					act = tony_act
					stats.game_state = 5
					battle.waiting = steven
					battle.round -= 1
					cf.keyboard_output(settings, steven, tony, tony_act, 0)
			if battle.check_winner():
				stats.game_state = 4
		if stats.game_state == 5:
			cf.update_bullets(settings, screen, stats, battle, steven, tony, steven_bullets, tony_bullets, act,
							  s_hit_sound,t_hit_sound)

		cf.update_screen(settings, screen, stats, bg, bar, battle, tony, steven, play_button, settings_button,
						 return_button, steven_bullets, tony_bullets)

# TODO:加入获胜视频
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
