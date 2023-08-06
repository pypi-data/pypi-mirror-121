#!/usr/bin/env python

import subprocess
import os
import re


def acquireCliProgramVersion(s):
	"""
	Acquire the version of a cli program

	param s: The output of the programm version string.

	example: 'gcc --version'
	"""
	regex = r"(\d+)(\.\d+)(\.\d+)?"
	matches = re.finditer(regex, s, re.MULTILINE)
	version = None
	for matchNum, match in enumerate(matches, start=1):
		version = match.group()

	return version


def toString(obj):
	"""
	Convert an object to string representation

	param obj: The object to convert to string
	"""
	rv = ""
	if obj is None:
		pass
	elif isinstance(obj, list):
		rv = " ".join(obj)
	elif isinstance(obj, set):
		rv = " ".join(obj)
	else:
		rv = str(obj)
	return rv


def run_command(cmd):
	"""
	Run a shell command
	The stdout is shown.

	Returns the error code
	"""

	rv = subprocess.call(cmd, shell=True)
	return rv


def run_command2(cmd):
	"""
	Run a shell command

	Returns the stdout
	"""

	cmdList = cmd.split(" ")
	rv = None
	try:
		rv = subprocess.run(cmdList, stdout=subprocess.PIPE).stdout.decode('utf-8')
	except FileNotFoundError:
		pass

	return rv


def listPortNames():
	"""
	Returns the available port names in the project.

	Ports are directories inside the 'root/port/' directory (if available).
	Port names are the name of those directories.

	Returns:
	- list of port name strings (if available).
	- None if port dir is not available or if not any ports are available.
	"""
	rv = None
	portNameList = list()
	portPath = "port"
	if os.path.isdir(portPath):
		dirCandidateList = os.listdir(portPath)
		for dirCandidate in dirCandidateList:
			dirCandidatePath = os.path.join(portPath, dirCandidate)
			if os.path.isdir(dirCandidatePath):
				portNameList.append(dirCandidate)
		portNameList.sort()

	if len(portNameList) != 0:
		rv = portNameList

	return rv


def egrep(keywords, whole_words=False):
	"""
	Runs egrep

	param: keywords       Keywords to search for
	param: whole_words    Search for whole words
	"""
	grep_flags = "-i -nr -R --color --no-messages"

	if whole_words:
		grep_flags += " -w"

	cmd = f"grep -E {grep_flags} '{keywords}' src/ inc/ port/ || true"
	rv = run_command(cmd)
	return rv
