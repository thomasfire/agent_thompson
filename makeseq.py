#!/usr/bin/python3

#makes sequence from .keywords and Telegram validation
"""
### Author: Thomas Fire; URL: https://github.com/thomasfire;
### Author Telegram: @Thomas_Fire;
### Sponsored by academylab.ru
"""

from os import listdir
import re
from tlapi import getchoice
from habraparser import download_images

# checks if smstring is hexademical
def ishexademical(smstring):
	try:
		int(smstring, 16)
		if len(smstring)==32:
			return True
	except ValueError:
		return False


# returns list of keywords.loadkeys() is used in checking article for theme
def loadkeys():
	f=open(".keywords","r")
	res=re.findall(r":(\w+?){.*?}",f.read())
	f.close()
	return res


# returns list of directries, that consist articles
def getlistofarts():
	dirs=listdir(".")
	res=[]
	for x in dirs:
		if ishexademical(x):
			res.append(x)
	return res

# checks art if it consists keywords from .keywords
def checkart(num,keys):
	# opening article
	f=open(num+'/'+num+'.parsed','r')
	text=f.read().lower()
	f.close()

	# cycling through keywords
	for x in keys:
		if x in text:
			return True
	return False


# writes tag in dependence of what keyword is in text
"""
seq - sequence of numbers of articles
"""
def addtags(seq):
	# loading list of keywords
	f=open(".keywords","r")
	keys=f.read()
	f.close()

	# list of thematical keywords
	res=re.findall(r":(.+?){(.*?)}",keys)

	# list of keywords,that must be added anyway
	auto=''.join(re.findall(r"::{(.*?)}",keys))

	hashtags=[]

	# cycling through articles that must be posted
	for x in seq:
		# reading article
		g=open(x+'/'+x+'.parsed','r')
		buff=g.read() # buffered article
		g.close()

		# adding tag to article
		g=open(x+'/'+x+'.parsed','a')
		for y in res:
			if y[0] in buff:
				hashtags.append(y[1])
		g.write('\n'+' '.join(hashtags))
		g.close()


# writes list of what to post to vk. needs validation through Telegram
"""
resource - 'habrahabr' or 'geektimes' or 'megamozg'
tlurl - 'https://api.telegram.org/bot<token>/' , where <token> is token, given by FatherBot or another bot
lastid - id of last update in Telegram
"""
def main(resource,tlurl,lastid=0):
	keys=loadkeys()
	arts=getlistofarts()
	g=open('files/'+resource+'.seq','r')
	nst=g.read()
	g.close()
	g=open('files/'+resource+'.posted','a')
	g.write("\n"+nst)
	g.close()
	f=open('files/'+resource+'.seq','w')

	# loading list of posted files
	g=open('files/'+resource+'.posted','r')
	posted=g.read().split()
	g.close()

	#g=open('files')

	seq=[]
	for x in arts:
		if checkart(x,keys) and x not in posted:
			seq.append(x)
	print(seq)
	if seq:
		seq,lastid=getchoice(tlurl,seq,lastid)

	# downloading images for choosen articles
	for x in seq:
		download_images(str(x))

	f.write('\n'.join(seq))
	f.close()
	addtags(seq)
	return lastid

if __name__ == '__main__':
	main()


def makeseq(resource,tlurl,lastid):
	print("Making sequence....")
	main(resource,tlurl,lastid)
