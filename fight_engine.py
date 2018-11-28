# -*- coding: utf-8 -*-

# 定义各个技能效果
# 每个函数中只考虑对方生命值以及自己怒气值和冷却的变化


def do_nothing(src, dst, dst_action):
	"""待机
	Args:
		src: 技能释放者
		dst: 释放对象
		dst_action: 对方动作
	"""
	return


def simple_attack(src, dst, dst_action):
	"""普通攻击"""
	if dst_action != "counter attack" and dst_action != "defend":
		dst.hp -= 2
	elif dst_action == "counter attack":
		dst.hp -= 1

	src.mp += 1
	src.update()
	dst.update()


def simple_defend(src, dst, dst_action):
	"""普通防御"""
	src.cd -= 1
	src.update()
	dst.update()


def counter_attack(src, dst, dst_action):
	"""防守反击"""
	if dst_action == "attack":
		dst.hp -= 7
	src.cd = 4
	src.update()
	dst.update()


def super_attack(src, dst, dst_action):
	"""超级攻击"""
	if dst_action == "defend":
		dst.hp -= 3
	else:
		dst.hp -= 8
	src.mp -= 4

	src.update()
	dst.update()


# 利用字典达到函数指针的效果
fight_function = {
	"do nothing": do_nothing,
	"attack": simple_attack,
	"defend": simple_defend,
	"counter attack": counter_attack,
	"super attack": super_attack
}
