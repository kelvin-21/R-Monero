import random
import hashlib
import pandas as pd
import numpy as np
import time
import sys
import os


class VSS:
	def __init__(self, m, secret, t, N):
		self.m = m
		self.secret = secret
		self.t = t
		self.N = N

	def r(self):  # random in the field
		return random.randint(0, self.m-1)

	def f(self, A, s, x):
		y = 0
		y += s
		for i in range(0, self.t-1):
			y += A[i] * pow(x, i+1)
		return y

	def gen_shares(self):
		A = []
		for i in range(0, self.t-1):
			A.append(self.r())

		Beta = []
		for i in range(0, self.N):
			print(i)
			x = self.r()
			y = self.f(A, self.secret, x)
			Beta.append((x, y))
		return Beta



class MoneroAddress():
	def __init__(self, m):
		self.m = m
		self.d = -121665 * self.mod_inverse(121666)

	def r(self):  # random in the field
		return random.randint(0, self.m-1)

	def compute_one_time_address(self, Kv, Ks):  # Kv, Ks are 2D
		r = self.r()
		G = (self.r(), self.r())

		R = self.alpha_G(r, Kv)

		# it may not fit the defintion
		# but for evaluting performance, it will work
		R = (self.hash(R[0]) + self.hash(R[1])) % self.m

		print(R, G)
		K1 = self.alpha_G(R, G)

		Ko = self.ed25519_add(K1, Ks)

		return Ko, self.alpha_G(r, G)

	def alpha_G(self, alpha, G):
		result = (0, 0)
		for i in range(0, alpha):
			result = self.ed25519_add(result, G)
			print(i, alpha)
		return result

	def hash(self, num):
		# hash int to int
		string = str(num).encode('ASCII')
		h = hashlib.sha256(string).hexdigest()
		return int(h, 16)

	def egcd(self, a, b):
		if a == 0:
			return (b, 0, 1)
		else:
			g, y, x = self.egcd(b % a, a)
			return (g, x - (b // a) * y, y)

	def mod_inverse(self, a):
		m = self.m
		g, x, y = self.egcd(a, m)
		if g != 1:
			print('modular inverse does not exist')
			return 3.14
		else:
			return x % m

	def ed25519_add(self, P, Q):
		# ed25519
		a = -1
		d = self.d
		x1, y1 = P[0], P[1]
		x2, y2 = Q[0], Q[1]

		x = ((x1*y2+x2*y1) * self.mod_inverse(1+d*x1*x2*y1*y2)) % self.m
		y = ((y1*y2-a*x1*x2) * self.mod_inverse(1-d*x1*x2*y1*y2)) % self.m

		return (x, y)


class Regulation:
	def __init__(self):
		self.m = pow(2, 255)-19  # order of the field
		self.t = 100
		self.N = 1000
		self.vss = VSS(m=self.m, secret=self.r(), t=self.t, N=self.N)
		self.moneoro = MoneroAddress(self.m)
		self.user_addresses = None

	def r(self):  # random in the field
		return random.randint(0, self.m-1)

	def gen_users_address(self, num):
		for i in range(num):
			Kv = (self.r(), self.r())
			Ks = (self.r(), self.r())
			self.user_addresses.append(Kv, Ks)
		return

	def gen_bundle():
		Beta = vss.gen_shares()
		one_time_addresses = []
		for i in range(N):
			user_addr = self.user_addresses[i]
			one_time_addr, rG = moneoro.compute_one_time_address(Kv, Ks)
			one_time_addresses.append((one_time_addr, rG))
		return	Beta, one_time_addresses


class Experiment():
	def _init__(self, N_list, t_factors, num_trial):
		self.df = None
		self.N_list = N_list
		self.t_factors = t_factors
		self.num_trial = num_trial
		self.regulation = Regulation()

	def initialize(self):
		if os.path.exists('data.csv'):
			self.df = pd.read_csv('data.csv')
		else:
			self.df = pd.DataFrame(columns=['t', 'N', 'time_used', 'size'])

	def run_experiment(self):
		for N in self.N_list:
			for t_factor in self.t_factors:
				for i in range(self.num_trial):

					start = time.time()
