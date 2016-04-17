#!/usr/bin/env python
import sys
import os
from os import path
import acme_tiny
import urllib

STORE_PATH = path.dirname(path.abspath(__file__))
USERKEY = path.join(STORE_PATH, "keys", "user.key")
OUT_PATH='/etc/certs'

INTERMEDIATE_KEY_URL = "https://letsencrypt.org/certs/lets-encrypt-x3-cross-signed.pem"

def sh(cmd): os.system(cmd)

def ask(question):
	while True:
		val = raw_input(question  + " [Y/N]: ").lower()
		if 'y' in val: return True
		if 'n' in val: return False

def getHttp(url):
	try:
		f = urllib.urlopen(url)
		return f.read()
	except: return None

def createOrRenew(domain, userkey="keys/user.key", with_www=False, interactive=False, renewalOnly=False):
	DOMAIN_PATH=path.join(STORE_PATH, "keys", domain)
	CHALLENGE_PATH=path.join(STORE_PATH, "challenges", domain)
	isNew = False

	print "Domain: %s" % domain

	if interactive:
		if not ask("Proceed?"): return False

	if not path.isdir(DOMAIN_PATH):
		if renewalOnly:
			print "Set to renewal only, refusing to create new key"
			return False

		print "Directory not found, creating..."
		os.mkdir(DOMAIN_PATH)
		isNew = True

	if not path.isdir(CHALLENGE_PATH):
		print "Creating challenge dir..."
		os.mkdir(CHALLENGE_PATH)
		isNew = True

	#Fetch intermediate
	print "Downloading intermediate certificate..."
	intermediateKey = getHttp(INTERMEDIATE_KEY_URL)
	if not intermediateKey:
		print "Failed to download intermediate certificate"
		return False

	# Check for user key
	if not path.isfile(USERKEY):
		if not ask("No user key was found, generate?"): return False
		print "Generating user key: %s..." % USERKEY
		sh("openssl genrsa 4096 > %s" % USERKEY)

	# Build CSR
	_baseName = "%s/%s" % (DOMAIN_PATH, domain)
	KEY=_baseName + ".key"
	CSR=_baseName + ".csr"
	CRT=_baseName + ".crt"

	if not path.isfile(KEY):
		print "Generating private key..."
		sh("openssl genrsa 4096 > %s" % KEY)
	else: print "  Existing private key found"

	if not path.isfile(CSR):
		print "Generating certificate signing request (csr)..."
		if with_www:
			print "  Set www=true"
			sh('openssl req -new -sha256 -key %s -subj "/" -reqexts SAN -config <(cat /etc/ssl/openssl.cnf <(printf "[SAN]\nsubjectAltName=DNS:%s,DNS:www.%s")) > %s' % (KEY, domain, domain, CSR))
		else:
			sh('openssl req -new -sha256 -key %s -subj "/CN=%s" > %s' % (KEY, domain, CSR))
	else: print "  Existing CSR found."

	if isNew and interactive:
		print
		print "At this point, make sure your web server is correctly set up"
		print "to point the the challenge directory:"

		print "http://%s/.well-known/acme-challenge/ -> %s" % (domain, CHALLENGE_PATH)
		try: raw_input("[Press enter to continue]")
		except: return False

	# Create certificate
	try:
		acme_tiny.get_crt(USERKEY, CSR, CHALLENGE_PATH)
	except Exception as e:
		print "Error getting certificate"
		print e
		return False

	# Concat and output certs to /etc/certs
	OUT = path.join(OUT_PATH, domain + ".pem")

	print "Writing full key to %s..." % OUT
	FULL_KEY = open(KEY).read() + open(CRT).read() + intermediateKey
	open(OUT, 'w').write(FULL_KEY)

	return True

def main(args):
	if len(args) != 1:
		print "Must provide domain name as argument"
		sys.exit(1)
	ret = createOrRenew(args[0], interactive=True)
	sys.exit(0 if ret else 1)

if __name__ == "__main__":
	main(sys.argv[1:])