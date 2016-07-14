#!/usr/bin/python3

#makes sequence from .keywords and Telegram validation
"""
###Author: Thomas Fire; URL: https://github.com/thomasfire;
###Author Telegram: @Thomas_Fire;
###Sponsored by academylab.ru
"""

from os import listdir
import re
from tlapi import getchoice

def loadkeys():
	f=open(".keywords","r")
	res=re.findall(r":(\w+?){.*?}",f.read())
	f.close()
	return res

def getlistofarts():
	dirs=listdir(".")
	res=[]
	for x in dirs:
		if x.isdigit():
			res.append(x)
	return res

def checkart(num,keys):
	f=open(num+'/'+num+'.parsed','r')
	text=f.read().lower()
	f.close()
	for x in keys:
		if x in text:
			return True
	return False

def addtags(seq):
	f=open(".keywords","r")
	keys=f.read()
	f.close()
	res=re.findall(r":(.+?){(.*?)}",keys)
	auto=''.join(re.findall(r"::{(.*?)}",keys))
	hashtags=[]
	for x in seq:
		g=open(x+'/'+x+'.parsed','r')
		buff=g.read()
		g.close()
		g=open(x+'/'+x+'.parsed','a')
		for y in res:
			if y[0] in buff:
				hashtags.append(y[1])
		#print(hashtags)
		g.write('\n'+' '.join(hashtags))
		g.close()

def main(resource,tlurl,lastid):
	keys=loadkeys()
	arts=getlistofarts()
	g=open('files/'+resource+'.seq','r')
	nst=g.read()
	g.close()
	g=open('files/'+resource+'.posted','a')
	g.write("\n"+nst)
	g.close()
	f=open('files/'+resource+'.seq','w')
	g=open('files/'+resource+'.posted','r')
	posted=g.read().split()
	g.close()
	seq=[]
	for x in arts:
		if checkart(x,keys) and x not in posted:
			seq.append(x)
	print(seq)
	if seq:
		seq,lastid=getchoice(tlurl,seq,lastid)
	f.write('\n'.join(seq))
	f.close()
	addtags(seq)
	return lastid

if __name__ == '__main__':
	main()


def makeseq(resource,tlurl,lastid):
	print("Making sequence....")
	main(resource,tlurl,lastid)
