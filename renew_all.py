#!/usr/bin/env python
import os, sys
from os import path
from create_or_renew import createOrRenew

BASE_PATH = path.dirname(path.abspath(__file__))
KEY_PATH = path.join(BASE_PATH, "keys")

failures = 0

for file in os.listdir(KEY_PATH):
	if path.isdir(path.join(KEY_PATH, file)):
		print "Renewing %s..." % file
		if not createOrRenew(file, interactive = False, renewalOnly=True):
			print "FAILED TO RENEW %s" % file
			failures += 1

sys.exit(failures)