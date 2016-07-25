#!/usr/bin/python3
# -*- coding: utf-8 -*-

#this is API for bot in Telegram. See https://core.telegram.org/bots/api for detailed information
"""
### Author: Thomas Fire; URL: https://github.com/thomasfire;
### Author Telegram: @Thomas_Fire;
### Sponsored by academylab.ru
"""

from requests  import get as urlget
from datetime import datetime
from fcrypto import fdecrypt
from logging import exception,basicConfig,WARNING
from urllib.parse import quote, urlsplit, urlunsplit


#url of api Telegram
'''
password - password that files encrypted with. In my case it is sha256sum of string
'''
def geturl(password):
	url=('https://api.telegram.org/bot'+
	fdecrypt('files/telegram.token',password).split()[0].replace('token=','').replace(';','')+'/')
	return url


#sends a message to Telegram
'''
url - 'https://api.telegram.org/bot<token>/', where <token> is token, given by FatherBot or another bot
chatid - chat`s id, where to send
text - what should be sent
'''
def sendmsg(url,chatid,text):
	ntextparted=[]

	if len(text)>2048:
		for x in range(int(len(text)/2048)):
			if (x+1)*2048<len(text):
				ntextparted.append(quote(text[x*2048:(x+1)*2048].encode('utf-8')))
			else:
				ntextparted.append(quote(text[x*2048:].encode('utf-8')))
	else:
		ntextparted.append(quote(text.encode('utf-8')))

	for x in ntextparted:
		try:
			requ=urlget(url+'sendMessage?chat_id='+str(chatid)+'&text='+x)
		except Exception as msg_error:
			print(' sendMessage have gone wrong; ')
			exception(msg_error)
			return 'error'


	return



#gets and logs new messages to file
'''
url - 'https://api.telegram.org/bot<token>/', where <token> is token, given by FatherBot or another bot
offset - id of last update. Needs for optimization
'''
def getmsg(url,offset=0):
	try:
		requ=urlget(url+'getUpdates'+'?offset='+str(offset)).json()
		f=open('files/tl_msgs.db','r')
		msglist=f.read()
		f.close()
		f=open('files/tl_msgs.db','a')
		#logging to file
		for x in requ['result']:
			#checking if it allowed command
			if (('@ msg_id='+str(x['message']['message_id']) not in msglist and
			(x['message']['text'][0:4]=='/art'))
			and ';\n@' not in x['message']['text']):

				f.write('@ msg_id='+str(x['message']['message_id'])+' :: '+
				str(x['message']['from']['id'])+' :: '+
				datetime.fromtimestamp(x['message']['date']).strftime('%Y-%m-%d %H:%M:%S')+' :: '+
				x['message']['text']+' ;\n')

		f.close()
	except Exception as e:
		exception(' A error occured while getting updates in Telegram:\n')
		return 'error'
	if len(requ['result']):
		return requ['result'][-1]['update_id']
	return 0


#cleans up logs to make them small
def cleanup():
	f=open('files/tl_msgs.db','r')
	listofmsgs=f.read().split(' ;\n@ ')
	f.close()
	if len(listofmsgs)>1000:
		f=open('files/tl_msgs.db','w')
		f.write('@ '+' ;\n@ '.join(listofmsgs[-100:]))
		f.close()

	f=open('files/tl_msgs.made','r')
	listofmsgs=f.read().split()
	f.close()
	if len(listofmsgs)>1000:
		f=open('files/tl_msgs.made','w')
		f.write(' '.join(listofmsgs[-100:]))
		f.close()


#getting choice of what to send to VK
'''
url - 'https://api.telegram.org/bot<token>/', where <token> is token, given by FatherBot or another bot
listofart - list of candidate arts
offset - id of last update. Needs for optimization
'''
def getchoice(url,listofart,offset=0):
	f=open('files/admins.db','r')
	odmins=f.read().strip().split()
	f.close()
	f=open('files/tl_msgs.made','r')
	maden=f.read()
	f.close()

	print(len(listofart))
	print(listofart)

	for x in odmins:
		sendmsg(url,x,'Choose from these articles. Type "/art none" if you want to send no articles. Type numbers of articles separated by whitespaces.')
		for y in range(len(listofart)):
			f=open(listofart[y]+'/'+listofart[y]+'.parsed','r')
			text=f.read()
			f.close()
			sendmsg(url,x,'Article #'+str(y)+' : \n'+text)

	while True:
		lastid=getmsg(url,offset)
		f=open('files/tl_msgs.db','r')
		listofmsgs=f.read().split(' ;\n@ ')
		f.close()
		if not lastid==offset:
			for y in listofmsgs[-10:]:
				currmsg=y.split(' :: ')
				if currmsg[1] in odmins and currmsg[0] not in maden and currmsg[3][:4]=='/art':
					if currmsg[3][4:].strip().strip(';').strip()=='none':
						f=open('files/tl_msgs.made','a')
						f.write(' '+currmsg[0])
						f.close()
						return [],lastid
					f=open('files/tl_msgs.made','a')
					f.write(' '+currmsg[0])
					f.close()
					newlist=[]
					for x in currmsg[3][4:].strip().strip(';').strip().split():
						print(x,listofart)
						newlist.append(listofart[int(x)])
					return newlist,lastid
