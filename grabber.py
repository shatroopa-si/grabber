import variables
import mapper
import saveFiles
import crawler
import urllib.request
import os

def grab(siteUrl):
    """downloads the website"""

    #give values to the resource & crawlFrontier lists => crawl
    siteName = mapper.extractName(siteUrl)[0]
    crawler.crawlSite(siteUrl, siteName)

    for url in variables.crawlFrontier:
        print(url)
    """
    # sort all the links & resources in decreasing order
    variables.allPaths = variables.crawlFrontier + variables.resources
    variables.allPaths.sort(reverse = True)

    #make a directory
    try:
        os.mkdir(siteName)
    except:
        pass
    finally:
        os.chdir(siteName)

    #first download all the pages
    for x in variables.allPaths:
        saveFiles.save1(x, siteName)

        """

#-----------DRIVER CODE-----------
try:
    #take input for home directory and switch to it

    variables.homeDirectory = input('Enter the directory in which you want the site to be downloaded. \nIt must exist.>')

    #in case nothing is specified, consider the current working directory
    if variables.homeDirectory == '':
        variables.homeDirectory = os.getcwd()   

    #must end with '\'
    if variables.homeDirectory[-1] != '\\':
        variables.homeDirectory += '\\'

    os.chdir(variables.homeDirectory)

    #take input for the site
    variables.seed = input('Enter the website(url of homepage) you wish to download> ')
    
    #must star with a protocol
    if 'http://' not in variables.seed and 'https://' not in variables.seed:
        variables.seed = 'http://' + variables.seed

    #must end with '/'
    if variables.seed[-1] != '/':
        variables.seed += '/'

    #start downloading
    grab(variables.seed)

finally:
    print('Resources= ',variables.resources)
    print('Links= ',variables.crawlFrontier)
