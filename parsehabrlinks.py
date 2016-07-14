#!/usr/bin/python3

#this script parses links to the articles
"""
###Author: Thomas Fire; URL: https://github.com/thomasfire;
###Author Telegram: @Thomas_Fire;
###Sponsored by academylab.ru
"""



import urllib
import urllib.request
import re

def extractlinks(texthtml):
	a=re.compile(r"""<a class="button" href="(https://.*?)#habracut">""",re.DOTALL)
	listoflinks=re.findall(a,texthtml)
	return listoflinks

def main(resource):
	resource="https://"+resource+".ru/all/"
	f=urllib.request.urlopen(resource)
	toparse=str(f.read(),encoding='utf8')
	f.close()

	links=extractlinks(toparse)
	a=re.compile(r"""https://(\w+?).ru""")
	source=" ".join(list(re.findall(a,resource)))
	g=open('files/'+source+".links","w")
	g.write("\n".join(links)+"\n")
	g.close()

if __name__ == '__main__':
	main()

def parselinks(resource):
	print("Parsing links....")
	main(resource)
