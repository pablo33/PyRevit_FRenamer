# -*- encoding: utf-8 -*-
__doc__ 	= 'Informs Grid names on Structural Foundation Mark parameter'	# Infor for the tooltip
__title__ 	= 'SFRenamer'	# Button title, you can use \n for new line
__author__ 	= 'pablo33'	# Command author
__helpurl__ = 'https://github.com/pablo33/PyRevit_FRenamer'	# Help url

from Autodesk.Revit.DB import *		# Api de Revit
# from Autodesk.Revit.UI.Selection import *
# from pyrevit import forms

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument



#Todas las rejillas modeladas
rejillas = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Grids).WhereElementIsNotElementType().ToElements()
rejillas = list(rejillas)

### Clases punto y recta para efectuar intersecciones.
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
		return "(" + str(self.x) + ", " + str(self.y)

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
			if abs(self.m) <= abs(s.m):
				i.name = self.name + s.name
			else:
				i.name = s.name + self.name
		return (i)

	def info(self):
		print ("self.m = " + str(self.m))
		print ("self.n = " + str(self.n))
		print ("self.x = " + str(self.x))
		print ("self.y = " + str(self.y))

# Intersecting grids
crosspoints = list()
counter = 0
for r_A in rejillas:
	line_A = r_A.Curve
	pointa= point((line_A.GetEndPoint(0).X ,line_A.GetEndPoint(0).Y ),)
	pointb= point((line_A.GetEndPoint(1).X ,line_A.GetEndPoint(1).Y ),)
	rectaA = recta()
	rectaA.bytwopoints(pointa, pointb)
	rectaA.name = r_A.Name
	counter += 1
	
	for r_B in rejillas[counter:]:
		line_B = r_B.Curve
		result = line_A.Intersect(line_B)
		if result == SetComparisonResult.Overlap:
			pointc= point((line_B.GetEndPoint(0).X ,line_B.GetEndPoint(0).Y ),)
			pointd= point((line_B.GetEndPoint(1).X ,line_B.GetEndPoint(1).Y ),)
			rectaB = recta()
			rectaB.bytwopoints(pointc, pointd)
			rectaB.name = r_B.Name
			puntoI = rectaA.intersect(rectaB)
			crosspoints.append((
				puntoI,
				XYZ(puntoI.x, puntoI.y, 0),
				# rectaA,
				# rectaB,
				# r_A,
				#r_B,
				),
				)

#Transaction start
T = Transaction(doc, "PyRevit: Structural Foundation renamed")
T.Start()
# Retrieve all foundations instances
cimentaciones = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_StructuralFoundation).WhereElementIsNotElementType().ToElements()
commit_counter = 0
for z in cimentaciones:
	location = z.Location.Point
	XYlocation = XYZ(location.X, location.Y, 0)
	# check distance to intersection grids
	min = None
	Spoint = None
	for i in crosspoints:
		ipoint = i[1]
		dst = XYlocation.DistanceTo(ipoint)
		if min != None:
			if dst < min:
				min = dst
				Spoint = i[0]
		else:
			min = dst
	if Spoint != None:
		# Renaming 'Mark / Marca' parameter with values
		param = z.GetParameter(ForgeTypeId('autodesk.revit.parameter:doorNumber-1.0.0'))
		value = param.AsString()
		if param.AsString() != Spoint.name:
			param.Set(Spoint.name)
			commit_counter += 1
			print (value + " > " + Spoint.name)

T.Commit()
print (str(commit_counter) + " Foundations renamed")