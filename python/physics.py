import math

class Vector(object):
	def __init__(self, x, y, z):
		self.x = x
		self.y = y
		self.z = z
		
	def rotate(self, x_rot=None, y_rot=None, z_rot=None):
		if x_rot is not None:
			rot = math.radians(x_rot)
			new_y = self.y * math.cos(rot) - self.z * math.sin(rot)
			new_z = self.y * math.sin(rot) + self.z * math.cos(rot)
			self.y = new_y
			self.z = new_z
		if y_rot is not None:
			rot = math.radians(y_rot)
			new_x = self.x * math.cos(rot) + self.z * math.sin(rot)
			new_z = self.z * math.cos(rot) - self.x * math.sin(rot)
			self.x = new_x
			self.z = new_z
		if z_rot is not None:
			rot = math.radians(z_rot)
			new_x = self.x * math.cos(rot) - self.y * math.sin(rot)
			new_y = self.x * math.sin(rot) + self.y * math.cos(rot)
			self.x = new_x
			self.y = new_y
			
	def force_non_zero(self):
		if self.x == 0:
			self.x = 0.000000000000001
		if self.y == 0:
			self.y = 0.000000000000001
		if self.z == 0:
			self.z = 0.000000000000001