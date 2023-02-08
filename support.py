#!/usr/bin/env python3
"""
Tool for inspecting/updating SUPPORT.txt

	support.py [command]

Commands:
	check: (default)
		prints a short summary of support period(s)
	bump:
		extends the support date(s) for a maintainer
	create:
		creates a new SUPPORT.txt
	prune:
		removes support entries in the past
"""

import os.path
import datetime
from dateutil.relativedelta import relativedelta
import sys
from subprocess import check_output, Popen, PIPE

now = datetime.datetime.now()
expiredEntries = False
class Line:
	def __init__(self, literal, date, text):
		if not literal:
			try:
				date = datetime.datetime.strptime(date, "%Y-%m-%d")
				if now > date:
					print("Entry expired: %s"%text)
					expiredEntries = True
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
		self.latestDate = now

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
				entry = Line(False, date, remainder)
				self.lines.append(entry)
				if entry.date > self.latestDate:
					self.latestDate = entry.date
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

class Support:
	def __init__(self):
		self.sections = [Group()]
	
	def __str__(self):
		result = ""
		for section in self.sections:
			result += str(section)
		return result
	
	def addLine(self, line):
		line = line.strip()
		if line.endswith(":") and not line.startswith("#"):
			trimmed = line[:-1]
			self.sections.append(Group(trimmed))
			return True
		else:
			return self.sections[-1].addLine(line)
	
	def prune(self, now):
		for section in self.sections:
			section.prune(now)
	
	def bump(self, toDate, name):
		found = False
		for section in self.sections:
			if section.bump(toDate, name):
				found = True
		return found

### Command-line interface

def run(commandArray):
    pipe = Popen(commandArray, stdin=PIPE, stdout=PIPE);
    return pipe.communicate()[0].strip().decode('utf-8')

support = Support()
command = "check"
if len(sys.argv) >= 2:
	command = sys.argv[1]

if os.path.exists("SUPPORT.txt"):
	success = True
	with open("SUPPORT.txt", 'r') as file:
		for line in file:
			if not support.addLine(line):
				success = False
	if not success:
		print("SUPPORT.txt parse error")
		exit(1)
elif command != "create":
	print("No SUPPORT.txt")
	exit(1);

if command == "check":
	print("support promised for %i days"%(support.sections[0].latestDate - now).days)
	for section in support.sections[1:]:
		print("\n%s:\n\tpromised for %i days"%(section.name, (section.latestDate - now).days))
	if expiredEntries:
		print("\nSUPPORT.txt has outdated entries")
	exit(0)

if command == "create":
	support.addLine("# https://github.com/geraintluff/SUPPORT.txt")

if command == "bump" or command == "create":
	if len(sys.argv) < 4:
		print("support.py %s [6] [months/days] [?info]"%command)
		exit(1)
	
	if len(sys.argv) < 5:
		name = "%s <%s>"%(
			run(["git", "config", "--get", "user.name"]),
			run(["git", "config", "--get", "user.email"])
		)
	else:
		name = sys.argv[4]
	
	bumpDate = now
	if sys.argv[3].startswith("d"): # days
		bumpDate += relativedelta(day=int(sys.argv[2]))
	elif sys.argv[3].startswith("m"): # months
		bumpDate += relativedelta(months=int(sys.argv[2]))
	elif sys.argv[3].startswith("y"): # years
		bumpDate += relativedelta(years=int(sys.argv[2]))
	
	if not support.bump(bumpDate, name):
		print("Adding new contact for: %s"%name)
		support.sections[0].add(bumpDate, name)
elif command == "prune":
	support.prune(now)
else:
	print("Unknown command: %s"%command)
	exit(1)

# Whatever we did, write the result back
with open("SUPPORT.txt", 'w') as file:
	file.write(str(support))
