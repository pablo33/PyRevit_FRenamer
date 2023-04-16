# -*- encoding: utf-8 -*-
""" Point ans Line intersection	"""
__author__ = 'pablo33'


class point():
	"""Define a point"""
	def __init__(self, p):
		self.x = round(p[0],10)	# x coordinate
		self.y = round(p[1],10)	# y coordinate
		self.name = ""			# name

	def __eq__(self, obj):
		if isinstance(obj, point):
			if obj.x == self.x and obj.y == self.y:
				return True
		return False
	
	def __ne__(self, obj):
		return not self.__eq__(obj)
	
	def __str__(self):
		return f"({self.x}, {self.y})"

class recta():
	""" This is a line on the space """
	# function y = m*x + n

	def __init__ (self):
		self.m = None	# slope
		self.n = None	# n correction when x=0
		self.x = None	# it has a value if recta is x=value 
		self.y = None	# it has a value if recta is y=value
		self.name = ""	# Name of the line

	def bytwopoints (self, a,b):
		""" You can create a line given 2 points, each point is a point object """
		if not (isinstance(a,point) and isinstance(b,point)):
			print ("Two points instances are required")
			return
		if a == b:
			self.x = a.x
			self.y = b.y
			return
		elif a.x - b.x == 0:
			self.x = a.x
		elif a.y - b.y == 0:
			self.y = a.y
			self.m = 0
			self.n = a.y
		else:
			self.m = (a.y - b.y)/(a.x - b.x)
			self.n = b.y -self.m * b.x
 
	@property
	def isapoint (self):
		"True if this recta is a point"
		if self.x != None and self.y != None:
			return True

	def intersect(self, s):
		"""Intersection of two rectas"""
		if not isinstance(s,recta):
			print("a recta must be given")
			return
		
		if self.isapoint or s.isapoint:
			print ("One of the rectas is a point or it is not defined")
			return 

		if self.m == s.m:
			print ("Las rectas con paralelas")
			if self.n == s.n or (self.x == s.x and self.x != None) or (self.y == s.y and self.y != None):
				print ("Las rectas son la misma")
			return None
		
		i = point((0,0),)
		if self.m == None:
			# self tipo de recta vertical x=constante
			i.x = self.x
			i.y = s.m * i.x + s.n
			# Naming the intersection
			i.name = s.name + self.name

		elif s.m == None:
			# s tipo de recta vertical x = constante
			i.x = s.x
			i.y = self.m * i.x + self.n
			# Naming the intersection
			i.name = self.name + s.name

		else:
			i.x = (s.n - self.n) / (self.m - s.m)
			i.y = self.m * i.x + self.n
			# naming the intersection
			if self.m <= s.m:
				i.name = self.name + s.name
			else:
				i.name = s.name + self.name

		return (i)

	def info(self):
		print (f"self.m = {self.m}")
		print (f"self.n = {self.n}")
		print (f"self.x = {self.x}")
		print (f"self.y = {self.y}")

"""
puntoa = point((-157.9762216291486, 		207.16241643172955)	,)
puntob = point((-157.97622162914928, 	-210.01388439790136),)
puntoc = point((212.55204836863564, 		194.12012736412038)	,)
puntod = point((-215.60481288150888, 	194.12012736412177)	,)
"""
"""
puntoa = point((-157.976, 	207.162)	,)
puntob = point((-157.976, 	-210.013)	,)
puntoc = point(( 212.552, 	194.120)	,)
puntod = point((-215.6048, 	194.120)	,)

rectaA, rectaB = recta(), recta()

rectaA.bytwopoints(puntoa, puntob)
puntoI = rectaA.intersect(rectaB)
print (puntoI)
"""

puntoa = point((-157.9762216291486, 	207.16241643172955)	,)
puntob = point((-157.97622162914928, 	 -210.01388439790136)	,)
puntoc = point(( 212.55204836863564, 	196.94165137801156)	,)
puntod = point((-215.60481288150888, 	196.94165137801156)	,)

rectaA, rectaB = recta(), recta()
rectaA.bytwopoints(puntoa, puntob)
rectaB.bytwopoints(puntoc, puntod)

puntoI = rectaA.intersect(rectaB)
print (puntoI)
