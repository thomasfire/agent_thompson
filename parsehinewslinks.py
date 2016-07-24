#!/usr/bin/python3

#this script gets list of articles from http://hi-news.ru/robots
"""
###Author: Thomas Fire; URL: https://github.com/thomasfire;
###Author Telegram: @Thomas_Fire;
###Sponsored by academylab.ru
"""

import urllib
import urllib.request
import re

# gets list of links to articles
def extractlinks(texthtml):
	a=re.compile(r"""<a href="(http://.*?)" rel="nofollow"l>""")
	listoflinks=re.findall(a,texthtml)
	return listoflinks[:10]

def main():
	f=urllib.request.urlopen('http://hi-news.ru/robots')
	toparse=str(f.read(),encoding='utf8')
	f.close()

	links=extractlinks(toparse)
	g=open('files/hi-news.links',"w")
	g.write("\n".join(links)+"\n")
	g.close()

if __name__ == '__main__':
	main()
