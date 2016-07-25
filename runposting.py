#!/usr/bin/python3

"""
###Author: Thomas Fire; URL: https://github.com/thomasfire;
###Author Telegram: @Thomas_Fire;
###Sponsored by academylab.ru
"""


from fcrypto import fdecrypt,gethash
from tlapi import geturl
import vkupload as vup
import habraparser as hper
import parsehabrlinks as phlinks
import makeseq as mkseq
import parsehinewslinks as parsehnl
import hinewsparser as hinper
from shutil import rmtree
from time import sleep
from random import randint
from os import listdir
from logging import exception,basicConfig,WARNING,DEBUG
from getpass import getpass


#configuring logs
basicConfig(format = '%(levelname)-8s [%(asctime)s] %(message)s',
level = DEBUG, filename = 'logs/logs.log')

def main():
	psswd=gethash(getpass())

	resource=fdecrypt("files/vk.settings",psswd).split()[0]


	url=geturl(psswd)
	lastid=0


	#starting bot in server mode
	while True:

		#deleting trash
		print("Deleteing old files....")
		dirs=listdir(".")
		for x in dirs:
			if x.isdigit():
				rmtree(x)
		#parsing links and making list of what to download
		try:
			phlinks.parselinks(resource)
		except Exception as e:
			print("Somethings wrong,maybe it's bad connection")
			print("Retrying in 30 seconds...")
			exception(e)
			sleep(30)
			continue

		try:
			parsehnl.main()
		except Exception as e:
			print("Somethings wrong,maybe it's bad connection")
			print("Retrying in 30 seconds...")
			exception(e)
			sleep(30)
			continue


		#refreshing links list
		f=open('files/'+resource+".links",'r')
		links=f.read().split()
		f.close()

		#downloading all articles
		try:
			for x in links:
				hper.parsearts(x)
		except Exception as e:
			print("Somethings wrong,maybe it's bad connection")
			print("Retrying in 30 seconds...")
			exception(e)
			sleep(30)
			continue

		#refreshing links list
		f=open("files/hi-news.links",'r')
		hinewslinks=f.read().split()
		f.close()

		#downloading all articles
		try:
			for x in links:
				hinper.main(x)
		except Exception as e:
			print("Somethings wrong,maybe it's bad connection")
			print("Retrying in 30 seconds...")
			exception(e)
			sleep(30)
			continue

		#making sequence what to post to VK
		lastid=mkseq.makeseq(resource,url,lastid)

		#uploading to VK
		vup.startuploading(psswd,resource)

		#sleeping for 0.5-1 hour
		sltime=1800 + randint(1,1800)
		print("Sleeping for {0} seconds".format(sltime))
		sleep(sltime)



		print("\n")

if __name__=="__main__":
	main()
