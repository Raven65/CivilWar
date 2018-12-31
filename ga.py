# -*- coding: utf-8 -*-
import random


class Ga():
	def __init__(self, settings, population_size):
		self.settings = settings
		self.population = []
		for i in range(population_size):
			temp = []
			for j in range(8):
				temp.append(random.random())
			self.population.append(temp)
		self.normalize_weigh()
		self.next_population = []
		self.prob = [0] * 100

	def normalize_weigh(self):
		for weigh in self.population:
			temp_sum = sum(weigh)
			if temp_sum != 1:
				for i in range(8):
					weigh[i] /= temp_sum

	def shuffle(self):
		random.shuffle(self.population)

	def calculate_p(self, index, test):
		total = 0
		for i in range(len(index)):
			total += test[i][1]
		for i in range(len(index)):
			self.prob[index[i]] = test[i][1] / total

	def copy(self, index):
		for i in index:
			self.next_population.append(self.population[i])

	def choose_parent(self, index, another):
		m = 0
		r = random.random()
		for i in index:
			m += self.prob[i]
			if r <= m and i != another:
				return i

	def cross_over(self, index, p):
		for j in range(40):
			fa = self.choose_parent(index, -1)
			mo = self.choose_parent(index, fa)
			s_point = random.randint(0, 7)
			temp1 = self.population[fa][:s_point] + self.population[mo][s_point:]
			temp2 = self.population[mo][:s_point] + self.population[fa][s_point:]
			self.next_population.append(temp1)
			self.next_population.append(temp2)

		self.population = self.next_population
		self.next_population = []
		self.normalize_weigh()

	def mutation(self, p):
		for i in range(20, 100):
			for k in range(8):
				t = random.random()
				if t < p:
					self.population[i][k] = random.random()
		self.normalize_weigh()

	def strategy(self, w, a, b, t):
		x = []
		x.append(a.hp / self.settings.max_hp)
		x.append(-b.hp / self.settings.max_hp)
		x.append(a.mp / self.settings.max_mp)
		x.append(-b.mp / self.settings.max_mp)
		x.append(a.shield / self.settings.max_shield)
		x.append(-b.shield / self.settings.max_shield)
		x.append(a.counter / 2)
		x.append(-b.counter / 2)
		sum = 0
		for i in range(8):
			sum += x[i] * w[i]
		if sum > t:
			if a.mp < 6:
				return [sum, "attack"]
			else:
				return [sum, "super attack"]
		else:
			if a.mp < 4 or a.counter:
				return [sum, "defend"]
			else:
				return [sum, "counter attack"]
