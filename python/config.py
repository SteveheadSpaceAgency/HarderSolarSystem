import os

class Module(object):
	def __init__(self, header):
		self.header = header
		self.parameters = []
		self.children = []
		self.parent = None
		
	def add_parameter(self, parameter):
		self.parameters.append(parameter)
		
	def add_child(self, child):
		child.parent = self
		self.children.append(child)
		
	def determine_depth(self):
		depth = 0
		parent = self.parent
		while parent is not None:
			depth += 1
			parent = parent.parent
		return depth
		
	def write_to_file(self, file):
		with open(file, 'w') as f:
			f.write(str(self))
		
	def __str__(self):
		depth = self.determine_depth()
		t = "\t" * depth
		output = t + self.header + "\n"
		output += t + "{\n"
		for parameter in self.parameters:
			output += t + "\t" + parameter + "\n"
		for child in self.children:
			output += str(child)
		output += t + "}\n"
		return output