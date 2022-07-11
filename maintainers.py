import os.path
import datetime
import sys

if not os.path.exists("MAINTAINERS.txt"):
	print("Missing MAINTAINERS.txt")
	exit(1);

class Line:
	def __init__(self, literal, date, text):
		if not literal:
			try:
				date = datetime.datetime.strptime(date, "%Y-%m-%d")
			except Exception:
				print("Failed to parse date: %s"%date)
				text = date + text
				literal = True
		self.literal = literal
		self.date = date
		self.text = text

	def __str__(self):
		if self.literal:
			return self.text + "\n"
		else:
			return self.date.strftime("%Y-%m-%d") + self.text + "\n";

class Group:
	def __init__(self, name=None):
		self.name = name
		self.lines = []
	
	def addLine(self, line):
		if (len(line) == 0 or line.startswith("#")):
			self.lines.append(Line(True, None, line))
		else:
			date = line.split()[0]
			try:
				remainder = line[len(date):]
				self.lines.append(Line(False, date, remainder))
			except Exception:
				print("Failed to parse date: %s"%date)
				self.lines.append(Line(True, None, line))

	def __str__(self):
		result = ""
		if self.name != None:
			result = self.name + ":\n"
		for line in self.lines:
			result += str(line)
		return result

class Maintainers:
	def __init__(self):
		self.groups = [Group()]
	
	def __str__(self):
		result = ""
		for group in self.groups:
			result += str(group)
		return result
	
	def addLine(self, line):
		line = line.strip()
		if line.endswith(":") and not line.startswith("#"):
			trimmed = line[:-1]
			self.groups.append(Group(trimmed))
		else:
			self.groups[-1].addLine(line)
	

maintainers = Maintainers()

with open("MAINTAINERS.txt", 'r') as file:
	for line in file:
		maintainers.addLine(line)

print(maintainers)
