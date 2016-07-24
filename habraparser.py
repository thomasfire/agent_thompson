#!/usr/bin/python3

#this script gets article from URL
"""
###Author: Thomas Fire; URL: https://github.com/thomasfire;
###Author Telegram: @Thomas_Fire;
###Sponsored by academylab.ru
"""


import urllib
import urllib.request
import re
from readability.readability import Document
from os import mkdir, path
from shutil import move as shmove


def removetags(somestrin):
	fg=open(".listoftags","r")
	tags=fg.read().split()
	fg.close()
	for x in tags:
		somestrin=somestrin.replace(x," ")
	return somestrin


def findimg(texthtml):
	a=re.compile(r"""<img.*?src="(.+?)".*?>""", re.DOTALL)
	listofimg=re.findall(a,texthtml)
	return listofimg

def videolink(texthtml):
	a=re.compile(r"""<iframe.*?src="(.+?)".*?>.*?</iframe>""",re.DOTALL)
	b=re.compile(r"""(<iframe.*?src=".+?".*?>.*?</iframe>)""",re.DOTALL)
	listoftags=re.findall(b,texthtml)
	listoflinks=re.findall(a,texthtml)
	for x in range(len(listoftags)):
		texthtml=texthtml.replace(listoftags[x],listoflinks[x])
	return texthtml


def delpoll(text):
	a=re.compile(r"""(<div class="polling">.*</div>)""",re.DOTALL)
	for x in re.findall(a,text):
		text=text.replace(x,'')
	return text

def deletetrash(texthtml,num):
	arttext = Document(texthtml).short_title()+'\n\n'+Document(texthtml).summary()


	listofimg=findimg(arttext)
	a=re.compile(r"""<img.*?src=".+?".*?>""", re.DOTALL)
	arttext=re.sub(a,"",arttext)

	b=re.compile(r"""href="(.*?)">""", re.DOTALL)
	listoflinks=re.findall(b,arttext)
	arttext=re.sub(b,"",arttext)

	f=open(num+".images","w")
	f.write("\n".join(listofimg))
	f.close()

	g=open(num+".links","w")
	g.write("\n".join(listoflinks))
	g.close()
	arttext=videolink(arttext)

	arttext=removetags(arttext)

	#print(arttext)
	return arttext



def formatext(lines):
	x=0
	while x<len(lines):
		#print(x,len(lines))
		if lines[x].isspace():
			i=0
			while lines[x+i].isspace() and x+i<len(lines)-1:
				i+=1
			if i>0:
				del lines[x:i]
			if x+1==len(lines):
				break
		x+=1
	return "".join(lines)


def download_images(num):
	f=open(num+'/'+num+".images","r")
	img_urls=f.read().split()
	for x in img_urls:
		st=" ".join(list(re.findall(r"\w+?/(\w+?\.\w{3})",x)))
		if not st:
			continue
		urllib.request.urlretrieve(x, num+"/"+st)

def main(resource):

	f=urllib.request.urlopen(resource)
	toparse=str(f.read(),encoding='utf8')
	a=re.compile(r"""/(\d+?)/""")
	num=" ".join(list(re.findall(a,resource)))
	f.close()

	g=open(num+".parsed","w")
	g.write(deletetrash(toparse,num))
	g.close()
	g=open(num+".parsed","r")
	lines=list(g.readlines())
	#print(lines)
	g.close()
	g=open(num+".parsed","w")
	g.write(formatext(lines))
	g.close()
	#download_images(num)
	if not path.exists(num):
		mkdir(num)
	shmove(num+".parsed", num+'/'+num+".parsed")
	shmove(num+".images", num+'/'+num+".images")
	shmove(num+".links", num+'/'+num+".links")

if __name__=="__main__":
	from sys import argv
	main(argv[1])

def parsearts(resource):
	print('Parsing articles...')
	main(resource)
