import random
import hashlib
import numpy as np


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

m = pow(2, 255) - 19
secret = 100
t = 300
N = 1000
vss = VSS(m, secret, t, N)
Beta = vss.gen_shares()
print(len(Beta))


class MoneroAddress():
	def __init__(self, m):
		self.m = m
		self.d = -121665 * self.mod_inverse(121666)

	def r(self):  # random in the field
		return random.randint(0, self.m-1)

	def compute_one_time_address(self, Kv, Ks):  # Kv, Ks are 2D
		r = self.r()
		G = (self.r(), self.r())
		print('here 1')
		R = self.alpha_G(r, Kv)
		print('here 2')
		# it may not fit the defintion
		# but for evaluting performance, it will work
		R = (self.hash(R[0]) + self.hash(R[1])) % self.m
		print('here 3')
		print(R, G)
		K1 = self.alpha_G(R, G)
		print('here 4')
		Ko = self.ed25519_add(K1, Ks)
		print(K1, Ks)
		return Ko

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
		d = -121665/121666
		x1, y1 = P[0], P[1]
		x2, y2 = Q[0], Q[1]

		x = ((x1*y2+x2*y1) * self.mod_inverse(1+d*x1*x2*y1*y2)) % self.m
		y = ((y1*y2-a*x1*x2) * self.mod_inverse(1-d*x1*x2*y1*y2)) % self.m

		return (x, y)


# Mon = MoneroAddress(m=199)
# Kv, Ks = (100, 120), (122, 500)
# print(Mon.compute_one_time_address(Kv, Ks))


class Regulation:
	def __init__(self):
		self.m = pow(2, 255)-19  # order of the field
		self.d = -121665 * self.mod_inverse(121666)
		self.vss = None
		self.Monero = None

	def initialize(self):
		self.vss = Vss(m=self.m, secret=689, )

	def gen_users_address():
		return

	def gen_bundle():
		return



# g = Regulation()
# G = (1, 1)
# print(g.ed25519_add(G, G))
# print(list(range(0, 5000)))