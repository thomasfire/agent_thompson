#!/usr/bin/python3

#posts from sequence

import vk_api
from os import listdir
import re
from fcrypto import fdecrypt,gethash
from logging import exception


#returns list of images from list of files
def getimages(listoffiles):
    images=[".jpg","jpeg",".gif",".png"]
    res=[]
    for x in listoffiles:
        for y in images:
            if y in x.lower():
                res.append(x)
    return res

def main(psswd,resource='geektimes'):
    #vset=open("vk.settings","r")
    settings=fdecrypt("files/vk.settings",psswd)
    #vset.close()
    login="".join(re.findall(r"login=(.+)#endlogin",settings))
    password="".join(re.findall(r"password=(.+)#endpass",settings))
    group="".join(re.findall(r"grouptosend=(\d+)#endgroupid",settings))

    vk_session = vk_api.VkApi(login, password)

    try:
        vk_session.authorization()
    except vk_api.AuthorizationError as error_msg:
        print(error_msg)
        return

    upload = vk_api.VkUpload(vk_session)
    seqfile=open('files/'+resource+".seq","r")
    seq=seqfile.read().split()
    seqfile.close()
    print(" ".join(seq))

    try:
        vk = vk_session.get_api()
    except Exception as e:
        exception(e)


    for x in seq:
        listofatt=[]
        for y in getimages(listdir(x)):
            vkpost=upload.photo_wall(x+'/'+y,group_id=group)
            listofatt.append('photo'+str(vkpost[0]['owner_id'])+'_'+str(vkpost[0]['id']))
        f=open(x+"/"+x+".parsed","r")
        mes=f.read()
        f.close()
        posting=vk.wall.post(owner_id=-int(group),message=mes,attachments=','.join(listofatt))


if __name__ == '__main__':
    main()



def startuploading(psswd,resource='geektimes'):
    print("Uploading....")
    main(psswd,resource)
