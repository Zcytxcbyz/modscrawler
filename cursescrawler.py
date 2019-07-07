# -*- coding: UTF-8 -*-
import os
import re
import requests
import lxml
import time
import random
from bs4 import BeautifulSoup

#Geting information
def scrawler():
    cout=int(input('Number of pages:'))
    print('Executing...')
    a=1
    while a<=cout:
        try:
            response=requests.get(str('https://www.curseforge.com/minecraft/mc-mods?page='+str(a)))
            content=response.content.decode("utf-8")
            soup=BeautifulSoup(content,"lxml")
            #result=soup.find_all('a')
            result=soup.find_all('h3',class_="text-primary-500 font-bold text-lg hover:no-underline")
            #pattern1 = re.compile(r'(?<=href=").*(?=")')
            #pattern2 = re.compile(r'(?<=<h3 class="text-primary-500 font-bold text-lg hover:no-underline">).*(?=</h3>)')
            jsoncode='{'
            for i in result:
                if(re.search('h3',str(i))):
                    #matcher1=re.search(pattern1,str(i.parent))
                    #if(matcher1 and matcher2):
                    #if(matcher1):
                    print(i.text+" "+i.parent['href'])
                    jsoncode+='"'+i.text+'":"https://www.curseforge.com'+i.parent['href']+'",'
            jsoncode=jsoncode[:len(jsoncode)-1]+'}'
            filename=os.getcwd()+'\\Temp\\'+str(a)+'_'+str(int(time.time()))+str(random.randint(0,9))+str(random.randint(0,9))+".json"
            if(not os.path.exists(os.getcwd()+'\\Temp\\')):
                os.makedirs(os.getcwd()+'\\Temp\\')
            fo = open(filename, "w")
            fo.write(jsoncode)
            fo.close()
            print('Write to file "'+filename+'"')
        except:
            print('Raised an exception')
        finally:
            a+=1

#Process the file.
def mergefiles():
    try:
        fileslist=os.listdir('Temp')
        filename='modslist.json'
        l=len(fileslist)
        a=1
        fo=open(filename,"w")
        fo.write('{')
        fo.close()
        while a<=l:
            for i in fileslist:
                num=re.search(re.compile(r'\d+(?=_)'),i).group(0)
                if(num==str(a)):
                    print('Temp\\'+i+'->'+filename)
                    f=open('Temp\\'+i,"r")
                    text=f.read()
                    if(a==l):
                        text=text[1:len(text)-1]
                    else:
                        text=text[1:len(text)-1]+','
                    f.close()
                    fo=open(filename,"a")
                    fo.write(text)
                    fo.close()
            a+=1
        fo=open(filename,"a")
        fo.write('}')
        fo.close()
        for item in fileslist:
            os.remove('Temp\\'+item)
        os.rmdir('Temp')
        print('Clean up files')
    except:
        print('Raised an exception')

#Reprocess the file.
def formatfiles():
    try:
        print('Process the file')
        fop=open("modslist.json","r")
        sr=fop.read()
        fop.close()
        fope=open("modslist.json","w")
        wr=re.sub('",,"','","',sr)
        fope.write(wr)
        fope.close()
        fo=open("modslist.json","r")
        read=fo.read()
        result=re.sub('",','",\n  ',read)
        pattern1=r"(?<!.){"
        pattern2=r"}(?!.)"
        result=re.sub(pattern1,'{\n  ',result)
        result=re.sub(pattern2,'\n}  ',result)
        fo.close()
        print('Generate file "modslist_format.json"')
        f=open("modslist_format.json","w")
        f.write(result)
        f.close()
    except:
        print('Raised an exception')

#Main program
if __name__ == '__main__':
    try:
        scrawler()
        mergefiles()
        formatfiles()
        print('The run is complete.')
    except:
        print('Raised an exception')
    finally:
        input('Press any key to continue.')