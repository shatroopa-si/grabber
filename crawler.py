#crawls through a website

import urllib.request
import variables

def addLinkToFrontier(link):
	"""adds an absolute link to crawl frontier avoiding redundancy"""

	if link not in variables.crawlFrontier:
		variables.crawlFrontier.append(link)


def addLinkToResource(link):
	"""adds an absolute link to resources avoiding redundancy"""

	if link not in variables.resources:
		variables.resources.append(link)


def genAbsoluteLink(plink, link):
	"""generates an absolute link from relative"""

	toCrawl = True

	if link != '':
		if link[0] == '/':								#starts with '/'
			link = variables.seed + link[1:]		    #avoid 2 '/'

		elif link not in variables.relatives:			#Default.aspx
			variables.relatives.append(link)
			if plink[-1] == '/':
				link = plink + link
			else:
				link = plink + '/' + link

		else:
			toCrawl = False

	return link, toCrawl


def resource(plink, link, siteName):
	"""manages resource links"""


	#absolute path
	if siteName in link:
		addLinkToResource(link)								#add link
	#relative path
	elif siteName not in link:
		if 'http:' not in link and 'https:' not in link:	#must not be an external/online resource
			link, toCrawl = genAbsoluteLink(plink, link)	#form absolute path
			if toCrawl:
				addLinkToResource(link)						#add link


def extractParentLink(url):
	"""removes file name if any and returns the remaining link."""

	test = ''
	btest = ''
	
	i = len(url) - 1
	
	if i >= 0:
		ch = url[i]

		#check if there is any file specified in url
		while ch != '/' and i >= 0:
			test += ch
			i -= 1
			ch = url[i]
		btest = url[: i + 1]
	
	# '.' in btest signifies that there is some domain name in the remaining URL.
	#check if it is a valid file name. If yes, splice it out!
	if '.' in btest and '.' in test:
			return url[: i + 1]
	else:
		return url
		


def extractValue(line, attribute):
	"""extracts the value of attributes in an html tag"""
	
	myValue = ''

	#to avoid attributes in javascript or normal text
	if attribute + '="' in line or attribute + "='" in line:
		aIndex = line.index(attribute)
	else:
		aIndex = None
	
	#attribute exists and it's a tag
	if aIndex != None:
	
		#traverse upto the value
		ch = line[aIndex]
		while ch != '"' and ch != "'":
			aIndex += 1
			ch = line[aIndex]

		aIndex += 1
		ch = line[aIndex]
		
		# extract the value
		while ch != "'" and ch != '"':
			myValue += ch
			aIndex += 1
			ch = line[aIndex]

	return myValue

		
def scanPage(url, siteName):
	"""scans through a web page for links & resources"""
	
	try:
		#generate urlPage object
		urlPage = urllib.request.urlopen(url)

		#read through it line by line
		line = urlPage.readline().decode('utf-8')

		#traverse until you reach EOF
		while line != '':

			#2 possibilities of references: href & src
			if 'href' in line:
				link = extractValue(line, 'href')
	
				#2 possibilities of tags: <a> & <link>
				if '<a' in line:
					#absolute path
					if siteName in link and 'mailto:' not in link and '#' not in link and 'javascript:' not in link:
						addLinkToFrontier(link)									#add link

					#relative path
					elif siteName not in link:
						if 'http:' not in link and 'https:' not in link:		#must not be an external link
							plink = extractParentLink(url)
							link, toCrawl = genAbsoluteLink(plink, link)		#form absolute path

							#add a proper url to be crawled in the crawl frontier list
							if toCrawl and link != '' and 'mailto:' not in link and '#' not in link and 'javascript:' not in link:
								addLinkToFrontier(link)

				elif '<link' in line:
					#resource exists
					if len(link) != 0:
						plink = extractParentLink(url)
						resource(plink, link, siteName)

			elif 'src' in line and ('<img' in line or '<script' in line):
				link = extractValue(line, 'src')

				#resource exists
				if len(link) != 0:
					plink = extractParentLink(url)
					resource(plink, link, siteName)
	

			line = urlPage.readline().decode('utf-8')
	except:
		pass


def crawlSite(siteUrl, siteName):
	"""crawls through the complete Website"""

	#add the site to crawl & resources list. Also get the site name
	variables.crawlFrontier = [siteUrl]
	variables.resources = [siteUrl]

	#scan the site's home page
	scanPage(siteUrl, siteName)

	#repeatedly scan all the pages in crawlFrontier
	posLink = 1		#at 0th index is the site's home page

	while posLink < len(variables.crawlFrontier):
		print('url=',variables.crawlFrontier[posLink])

		url = variables.crawlFrontier[posLink]
		scanPage(url, siteName)

		posLink += 1
