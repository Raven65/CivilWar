# -*- coding: utf-8 -*-
"""定义通用函数"""
import pygame
import sys
import fight_engine as fn


def choose_input(message, limit_list, intro):
	"""询问用户选择输入
	Args:
		message: 第一次询问时的信息
		limit_list: 输入选择限定列表
		intro: 对输入的说明，用户输入错误，重新询问时需要展示
	Returns:
		value: 用户输入的值
	"""
	value = input(message + " " + intro + ": ").strip().lower()
	if value == "q" or value == "quit":  # 输入q则退出程序
		quit()
	if len(limit_list) > 0:
		while value not in limit_list:  # 若用户输入不在可输入范围，则重新询问
			value = input("Please check your input." + intro + ": ").strip().lower()
			if value == "q" or value == "quit":  # 输入q则退出程序
				quit()
	return value


def keyboard_output(settings, fighter_x, fighter_y, action, flag):
	"""询问用户选择输入
	Args:
		settings: 设定信息，获取预设评论长度等
		fighter_x, fighter_y: 对战双方
		action_x, action_y: 本回合的动作
	"""
	# 获取名字简写，更改动作时态
	simple_name_x = "".join([name[0:1] for name in fighter_x.name.split()])
	simple_name_y = "".join([name[0:1] for name in fighter_y.name.split()])
	if action == "do nothing":
		action = "did nothing"
	else:
		action += "ed"
	if flag:
		commentary = fighter_x.name + " " + action + "."
	else:
		commentary = fighter_y.name + " " + action + "."

	# 计算空格长度
	blank_len = settings.max_comment - 2 * settings.sta_length - len(commentary)
	blank1 = " " * (blank_len // 2)
	blank2 = " " * (blank_len - blank_len // 2)
	print("%s|%02d|%02d|%02d|%d%s%s%s%d|%02d|%02d|%02d|%s" % (
		simple_name_x, fighter_x.hp, fighter_x.shield, fighter_x.mp, fighter_x.counter,
		blank1, commentary, blank2,
		fighter_y.counter, fighter_y.mp, fighter_y.shield, fighter_y.hp, simple_name_y))


def check_events(settings, screen, stats, bg, battle, tony, steven, play_button, settings_button, return_button,
				 press_sound):
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		elif event.type == pygame.MOUSEBUTTONDOWN and stats.game_state == 0:
			mouse_x, mouse_y = pygame.mouse.get_pos()
			settings.check_events(stats, battle, tony, steven, mouse_x, mouse_y)
			press_sound.play()
		elif event.type == pygame.MOUSEBUTTONDOWN and stats.game_state == 1:
			mouse_x, mouse_y = pygame.mouse.get_pos()
			check_button(settings, screen, stats, bg, battle, tony, steven, play_button, settings_button, return_button,
						 mouse_x, mouse_y)
			press_sound.play()
		elif event.type == pygame.MOUSEMOTION and stats.game_state == 2:
			mouse_x, mouse_y = pygame.mouse.get_pos()
			check_choose_point(settings, screen, stats, tony, steven, mouse_x, mouse_y)
		elif event.type == pygame.MOUSEBUTTONDOWN and stats.game_state == 2:
			mouse_x, mouse_y = pygame.mouse.get_pos()
			check_choose_side(settings, screen, stats, bg, tony, steven, mouse_x, mouse_y)
			press_sound.play()
		elif event.type == pygame.MOUSEMOTION and stats.game_state == 3:
			mouse_x, mouse_y = pygame.mouse.get_pos()
			check_choose_point(settings, screen, stats, tony, steven, mouse_x, mouse_y)
		elif event.type == pygame.MOUSEBUTTONDOWN and stats.game_state == 3:
			mouse_x, mouse_y = pygame.mouse.get_pos()
			check_button(settings, screen, stats, bg, battle, tony, steven, play_button, settings_button, return_button,
						 mouse_x, mouse_y)
			press_sound.play()
		elif event.type == pygame.MOUSEBUTTONDOWN and stats.game_state == 4:
			mouse_x, mouse_y = pygame.mouse.get_pos()
			check_button(settings, screen, stats, bg, battle, tony, steven, play_button, settings_button, return_button,
						 mouse_x, mouse_y)
			press_sound.play()


def check_button(settings, screen, stats, bg, battle, tony, steven, play_button, settings_button, return_button,
				 mouse_x,
				 mouse_y):
	if stats.game_state == 1:
		play_button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
		settings_button_clicked = settings_button.rect.collidepoint(mouse_x, mouse_y)
		if play_button_clicked:
			stats.game_state = 2
		elif settings_button_clicked:
			stats.game_state = 0
	elif stats.game_state == 3:
		if tony.mode == "User" and battle.waiting == tony:
			tony.action_bar.check_choose(stats, mouse_x, mouse_y)
		elif steven.mode == "User" and battle.waiting == steven:
			steven.action_bar.check_choose(stats, mouse_x, mouse_y)
	elif stats.game_state == 4:
		return_button_clicked = return_button.rect.collidepoint(mouse_x, mouse_y)
		if return_button_clicked:
			stats.reset_games(settings, bg, battle, tony, steven)


def check_choose_point(settings, screen, stats, tony, steven, mouse_x, mouse_y):
	if stats.game_state == 2:
		point_s = steven.rect.collidepoint(mouse_x, mouse_y)
		point_t = tony.rect.collidepoint(mouse_x, mouse_y)
		if point_s:
			steven.point_me = True
		else:
			steven.point_me = False
		if point_t:
			tony.point_me = True
		else:
			tony.point_me = False
	elif stats.game_state == 3:
		if tony.mode == "User":
			tony.action_bar.check_point(mouse_x, mouse_y)
		elif steven.mode == "User":
			steven.action_bar.check_point(mouse_x, mouse_y)


def check_choose_side(settings, screen, stats, bg, tony, steven, mouse_x, mouse_y):
	point_s = steven.rect.collidepoint(mouse_x, mouse_y)
	point_t = tony.rect.collidepoint(mouse_x, mouse_y)
	if point_s or point_t:
		stats.game_state = 3
		tony.load_image(stats.game_state)
		steven.load_image(stats.game_state)
		bg.bg = pygame.image.load('sources/bg_3.jpg')
		bg.bg.set_alpha(230)
		if point_t:

			tony.mode = "User"
			steven.mode = settings.mode_list[settings.mode]
			tony.point_me = False
		else:
			steven.mode = "User"
			tony.mode = settings.mode_list[settings.mode]
			steven.point_me = False


def drawText(screen, text, posx, posy, textHeight=32, fontColor=(0, 0, 0), backgroudColor=(255, 255, 255)):
	fontObj = pygame.font.Font("No-move.ttf", textHeight)  # 通过字体文件获得字体对象
	textSurfaceObj = fontObj.render(text, True, fontColor, backgroudColor)  # 配置要显示的文字
	textRectObj = textSurfaceObj.get_rect()  # 获得要显示的对象的rect
	textRectObj.center = (posx, posy)  # 设置显示对象的坐标
	textSurfaceObj.set_colorkey((255, 255, 255))
	screen.blit(textSurfaceObj, textRectObj)  # 绘制字


def update_screen(settings, screen, stats, bg, bar, battle, tony, steven, play_button, settings_button, return_button,
				  steven_bullets, tony_bullets):
	bg.blitme(stats)
	if stats.game_state == 0:
		settings.blitme()
	elif stats.game_state == 1:
		play_button.draw_button()
		settings_button.draw_button()
	else:
		tony.blitme()
		steven.blitme()

	if stats.game_state == 2:
		drawText(screen, "Choose Your Side!", 640, 230, fontColor=(150, 0, 0))
	if stats.game_state == 3:
		drawText(screen, str(battle.round), 640, 170, fontColor=(150, 0, 0))
		bar.blitme(steven, tony)
		if tony.mode == "User" and battle.waiting == tony:
			tony.action_bar.blitme()
		elif steven.mode == "User" and battle.waiting == steven:
			steven.action_bar.blitme()
	if stats.game_state == 5:
		drawText(screen, str(battle.round), 640, 170, fontColor=(150, 0, 0))
		bar.blitme(steven, tony)
		if battle.waiting == tony:
			steven_bullets.draw_bullet()
		elif battle.waiting == steven:
			tony_bullets.draw_bullet()
	if stats.game_state == 4:
		if battle.winner == 3:
			drawText(screen, "There is no winner.", screen.get_rect().centerx, screen.get_rect().centery - 150)
		elif battle.winner == 1:
			drawText(screen, "The winner is Steven Rogers.", screen.get_rect().centerx, screen.get_rect().centery - 150)
		elif battle.winner == 2:
			drawText(screen, "The winner is Tony Starks.", screen.get_rect().centerx, screen.get_rect().centery - 150)
		return_button.draw_button()

	pygame.display.flip()


def update_bullets(settings, screen, stats, battle, steven, tony, steven_bullets, tony_bullets, act, s_hit_sound,
				   t_hit_sound):
	if battle.waiting == tony:
		if act == "attack" or act == "super attack":
			if act == "super attack":
				steven_bullets.flag = True
			steven_bullets.update()
			if steven_bullets.rect.x > 850:
				tony.been_hit = True
				s_hit_sound.play()
			if steven_bullets.rect.x > 880:
				steven_bullets.reset()
				stats.game_state = 3
				steven.load_image(3)
				pygame.time.wait(300)
				fn.fight_function[act](steven, tony)
				tony.been_hit = False
		else:
			fn.fight_function[act](steven, tony)
			pygame.time.wait(300)
			stats.game_state = 3

	else:
		if act == "attack" or act == "super attack":
			if act == "super attack":
				tony_bullets.flag = True
			tony_bullets.update()
			if tony_bullets.rect.left < 350:
				steven.been_hit = True
				t_hit_sound.play()
			if tony_bullets.rect.left < 320:
				tony_bullets.reset()
				stats.game_state = 3
				pygame.time.wait(200)
				fn.fight_function[act](tony, steven)
				steven.been_hit = False
		else:
			fn.fight_function[act](tony, steven)
			pygame.time.wait(300)
			stats.game_state = 3
