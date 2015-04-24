#performs various maps from url to system

import urllib.request
import os

def extractNewName(url):
	"""differentiate b/w: techtrishna.in & 2013.techtrishna.in"""

	name = ''

	if 'http:' in url:
		index = url.index('http://') + len('http://')

	elif 'https:' in url:
		index = url.index('https://') + len('https://')

	else:
		index = 0

	#slice out the name
	ch = url[index]
	while index < len(url) - 1 and ch != '/':
		name += ch
		index += 1
		ch = url[index]
	
	#for cases such as xyz.abc ie. those not ending with '/'
	if url[index] != '/':
		name += url[index]
		index += 1


	return name



def extractName(url):
	"""extracts name of a website from it's url(only the one having home page).
	Also returns the index of 1st character after 1st '/'.
	Returns whether url ends with '/' or not. """

	name = ''
	slash = True
	
	if 'www.' in url:
		index = url.index('www.') + len('www.')

	elif 'http:' in url:
		index = url.index('http://') + len('http://')

	elif 'https:' in url:
		index = url.index('https://') + len('https://')

	else:
		index = 0

	#slice out the name
	ch = url[index]
	while index < len(url) - 1 and ch != '/':
		name += ch
		index += 1
		ch = url[index]
	
	#for cases such as xyz.abc ie. those not ending with '/'
	if url[index] != '/':
		name += url[index]
		index += 1
		slash = False

	return name, index, slash


def extractPathFromUrl(url):
	"""extracts complete path of a file from url"""

	name, index, slash = extractName(url)
	
	#slice out the complete path until a '?' is observed
	if '?' in url:
		qIndex = url.index('?')
	else:
		qIndex = len(url)

	if slash:
	#path must not start with '/'
		if url[index] == '/':
			index += 1			

	#extract full path => filename inclusive
	filePath = url[index: qIndex]

	return filePath

#print(extractPathFromUrl('www.facebook.com'))
#print(extractPathFromUrl('www.facebook.com/'))
#print(extractPathFromUrl('www.facebook.com/shatroopa.si'))
#print(extractPathFromUrl('www.facebook.com/shatroopa.si/'))
#print(extractPathFromUrl('www.facebook.com/shatroopa.si/has.fes'))
#print(extractPathFromUrl('www.facebook.com/shatroopa.si/has.fes?ew'))
#print(extractPathFromUrl('http://silive.in/Home/About'))
#print(extractPathFromUrl('http://www.facebook.com'))
#print(extractPathFromUrl('http://www.facebook.com/'))
#print(extractPathFromUrl('http://www.facebook.com/shatroopa.si'))
#print(extractPathFromUrl('http://www.facebook.com/shatroopa.si/'))
#print(extractPathFromUrl('http://www.facebook.com/shatroopa.si/sgwe.wg'))
#print(extractPathFromUrl('http://www.facebook.com/shatroopa.si/sgwe.wg?sv'))

#print(extractPathFromUrl('https://www.facebook.com'))
#print(extractPathFromUrl('https://www.facebook.com/'))
#print(extractPathFromUrl('https://www.facebook.com/shatroopa.si'))
#print(extractPathFromUrl('https://www.facebook.com/shatroopa.si/'))
#print(extractPathFromUrl('https://www.facebook.com/shatroopa.si/fg.seg'))
#print(extractPathFromUrl('https://www.facebook.com/shatroopa.si/fg.seg?sdg'))
#print(extractName('https://www.facebook.net'))
#print(extractName('https://www.facebook.net/'))
#print(extractName('https://www.facebook.net/shatroopa.si/'))

