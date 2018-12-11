# -*- coding: utf-8 -*-

# 定义各个技能效果
# 每个函数中只考虑对方生命值以及自己怒气值和冷却的变化


def do_nothing(src, dst):
	"""待机
	Args:
		src: 技能释放者
		dst: 释放对象
		dst_action: 对方动作
	"""
	return


"""
普通攻击，对方掉3点血，先扣护盾再扣生命值，增加2点mp
"""


def simple_attack(src, dst):
	"""普通攻击"""
	if dst.counter:
		if src.shield >= 4:
			src.shield -= 4
		else:
			src.hp -= (4 - src.shield)
			src.shield = 0
			src.mp += 1
		dst.counter = 0

	elif dst.shield >= 3:
		dst.shield -= 3
	else:
		dst.hp -= (3 - dst.shield)
		dst.shield = 0
		dst.mp += 1
	if src.counter:
		src.counter -= 1
	src.mp += 1
	src.update()
	dst.update()


"""
防御，为自己增加2点护盾, 增加1点mp
"""


def simple_defend(src, dst):
	"""普通防御"""
	if src.counter:
		src.counter -= 1
	src.shield += 2
	src.mp += 1
	src.update()
	dst.update()


"""
为自己增加2点护盾值并增加一个持续2回合的反弹护盾，对方的普通攻击同时会使对方护甲/生命值减少4点
"""


def counter_attack(src, dst):
	"""防守反击"""
	if src.mp < 4:
		do_nothing(src, dst)
	else:
		src.shield += 2
		src.counter = 2
		src.mp -= 4
	src.update()
	dst.update()


"""
超级攻击，无视护盾值直接使对方生命值减少6点，若对方身上有反弹护盾，则使对方生命值减少2点并抵消反弹护盾。
"""


def super_attack(src, dst):
	"""超级攻击"""
	if src.counter:
		src.counter -= 1
	if src.mp < 6:
		do_nothing(src, dst)
	else:
		src.mp -= 6
		if not dst.counter:
			dst.hp -= 6
		else:
			dst.hp -= 2
			dst.counter = 0
		dst.mp += 1

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
