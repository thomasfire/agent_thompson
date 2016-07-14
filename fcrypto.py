#!/usr/bin/python3
# -*- coding: utf-8 -*-

#this is lib for easy using Twofish encryption
"""
###Author: Thomas Fire; URL: https://github.com/thomasfire;
###Author Telegram: @Thomas_Fire;
###Sponsored by academylab.ru
"""

from twofish import Twofish
from hashlib import sha512,sha256
from codecs import decode
from sys import argv
from getpass import getpass
from os import urandom

#returns secure hash
def gethash(smstr, mode='token'):
	salt=sha512(b'fghjfjkjlktycvq/.,ASS ON KEYBOARD t567 tx546e!@$^*#)%&/*-+-thgklh;xmnvhgjfty'+
	smstr.encode('ascii')).hexdigest()
	nhash=sha256(salt.encode('ascii')+smstr.encode('ascii')).hexdigest()
	for x in range(2**18):
		nhash=sha256(salt.encode('ascii')+nhash.encode('ascii')).hexdigest()
	return sha256(salt.encode('ascii')+nhash.encode('ascii')).digest()
	

#encrypts file via password
def fencrypt(filen,password):
	f=open(filen,'r')
	smstr=f.read()
	f.close()
	if len(smstr)%16:
		nstr=str(smstr+'%'*(16-len(smstr)%16)).encode('utf-8')
	else:
		nstr=smstr.encode('utf-8')

	psswd=Twofish(password)
	encredstr=b''

	for x in range(int(len(nstr)/16)):
		encredstr+=psswd.encrypt(nstr[x*16:(x+1)*16])

	f=open(filen,'wb')
	f.write(encredstr)
	f.close()

#decrypts file via password,returns decrypted text
def fdecrypt(filen,password):
	f=open(filen,'rb')
	smstr=f.read()
	f.close()
	psswd=Twofish(password)
	decredstr=b''

	for x in range(int(len(smstr)/16)):
		decredstr+=psswd.decrypt(smstr[x*16:(x+1)*16])

	return decode(decredstr,'utf-8').strip('%')


def main():
	if len(argv)>1 and argv[1]=='-setup':
		vari=False
		while not vari:
			inone=getpass('Password to encrypt files: ')
			intwo=getpass('Re-enter : ')
			if inone==intwo:
				password=gethash(inone)
				vari=True
			else:
				print('Wrong validation,retry\n')

		f=open('files/vk.settings','w')
		print('Configuring VK...')
		f.write(input('Resource(habrahabr or geektimes or megamozg): ')+'\n')
		f.write('grouptosend={0}#endgroupid\n'.format(input('Enter group id: ')))
		f.write('login={0}#endlogin\n'.format(input('Enter login: ')))
		f.write('password={0}#endpass\n'.format(getpass('Enter password: ')))
		f.write('ACHTUNG!THIS IS UNENCRYPTED TEXT!')
		f.close()
		fencrypt('files/vk.settings',password)

		f=open('files/telegram.token','w')
		f.write('token={0};'.format(input('Enter token of your TelegramBot: ')))
		f.write('\nACHTUNG!THIS IS UNENCRYPTED TEXT!')
		f.close()
		fencrypt('files/telegram.token',password)
		print('Now you can run posting via $ python3 runposting.py')

	else:
		print('Usage: python3 fcrypto.py -setup')



if __name__ == '__main__':
	main()
