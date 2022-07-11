import os.path
import datetime
from dateutil.relativedelta import relativedelta
import sys
from subprocess import check_output, Popen, PIPE

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
	
	def prune(self, now):
		if self.literal:
			return True
		return now <= self.date

	def bump(self, toDate, name):
		if not self.literal and name.strip() == self.text.strip():
			self.date = toDate
			return True;
		return False

class Group:
	def __init__(self, name=None):
		self.name = name
		self.lines = []

	def __str__(self):
		result = ""
		if self.name != None:
			result = self.name + ":\n"
		for line in self.lines:
			result += str(line)
		return result

	def addLine(self, line):
		if (len(line) == 0 or line.startswith("#")):
			self.lines.append(Line(True, None, line))
			return True
		else:
			date = line.split()[0]
			try:
				remainder = line[len(date):]
				self.lines.append(Line(False, date, remainder))
				return True
			except Exception:
				print("Failed to parse date: %s"%date)
				self.lines.append(Line(True, None, line))
				return False
	
	def prune(self, now):
		self.lines = [line for line in self.lines if line.prune(now)]

	def bump(self, toDate, name):
		found = False
		for line in self.lines:
			if line.bump(toDate, name):
				found = True
		return found
	
	def add(self, date, name):
		line = Line(False, date.strftime("%Y-%m-%d"), " " + name)
		for i in range(len(self.lines))[::-1]:
			# insert after the first maintainer line, if there is one
			if not self.lines[i].literal:
				self.lines.insert(i + 1, line)
				return
		self.lines.append(line)

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
			return True
		else:
			return self.groups[-1].addLine(line)
	
	def prune(self, now):
		for group in self.groups:
			group.prune(now)
	
	def bump(self, toDate, name):
		found = False
		for group in self.groups:
			if group.bump(toDate, name):
				found = True
		return found

### Command-line interface

maintainers = Maintainers()

success = True
with open("MAINTAINERS.txt", 'r') as file:
	for line in file:
		if not maintainers.addLine(line):
			success = False
if not success:
	print("Parse error")
	exit(1)

if len(sys.argv) < 2:
	print("parsed OK");
	print("commands: bump, prune")
	exit(0)

def run(commandArray):
    pipe = Popen(commandArray, stdin=PIPE, stdout=PIPE);
    return pipe.communicate()[0].strip().decode('utf-8')

now = datetime.datetime.now()
command = sys.argv[1]
if command == "bump":
	if len(sys.argv) < 4:
		print("maintainers.py bump [6] [months] [?info]")
		exit(1)
	
	if len(sys.argv) < 5:
		name = "%s <%s>"%(
			run(["git", "config", "--get", "user.name"]),
			run(["git", "config", "--get", "user.email"])
		)
	else:
		name = sys.argv[4]
	
	bumpDate = now
	if sys.argv[3].startswith("day"):
		bumpDate += relativedelta(day=int(sys.argv[2]))
	elif sys.argv[3].startswith("month"):
		bumpDate += relativedelta(months=int(sys.argv[2]))
	elif sys.argv[3].startswith("year"):
		bumpDate += relativedelta(years=int(sys.argv[2]))
	
	if not maintainers.bump(bumpDate, name):
		print("Adding new contact for: %s"%name)
		maintainers.groups[0].add(bumpDate, name)
elif command == "prune":
	maintainers.prune(now)
else:
	print("Unknown command: %s"%command)
	exit(1)

# Whatever we did, write the result back
with open("MAINTAINERS.txt", 'w') as file:
	file.write(str(maintainers))
