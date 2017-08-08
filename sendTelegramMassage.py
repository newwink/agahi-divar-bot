
import schedule
import time
import requests
from bs4 import BeautifulSoup as soup
import requests as req
import html2text
import re
import time
filePath='logs.log'
phoneLogs='phoneLogs.log'

def getAdsURL(firstPageURL):# This function get all ads url adres's
    
    html =req.get(firstPageURL).text
    href =soup(html,'html5lib').find_all('a',{'class':'post-card-link'})
    return href

def getShortURL(longURL):
    
    html =req.get(longURL).text
    href =soup(html,'html5lib').find_all('a',{'class':'share-link'})
    testH ='https://divar.ir'+href[0].get('href')
    return testH[50:]

def GetContent(adsURL):# This function Get phone, area and comment of ads
    testH ='https://divar.ir'+adsURL.get('href')
    #Get comment area_________________________
    html=req.get(testH).text
    #print(html)
    temp=soup(html,'html5lib').find('div',{'class':'ui fluid card post-description'})
    comments=str(temp)
    comments=(html2text.html2text(comments))
    return comments
    

def contentNotExistInBlackList(content,shortURL,rentOrSale):
    try:
        #______ agar agahi ghablan ferestade shode bashad return False
        #if shortURL in open(str(filePath)).read().split():
         #           print('Exist Ads')
          #          return False
        
        #______ agar shomare telefone hamrah dar matn bashad return False                
        phoneNumber=re.findall(r'09\d{9}', content)
        elevenNumber=re.findall(r'\d{11}', content)
        blackList=['املا','مشاور','گروه','مشاورشما','مشاور شما','مشاور املا','مشاوراملا','بازديد=خريد','بازديد =خريد','بازديد= خريد','بازديد = خريد','ارشناس',
                   'امپراطور','رابينسون','وروش','دلتا','راگا','شارمن','شار ',' شار',' شار ','آلفا','الفا','مسکن','ويلا']
        

        
        #if bool(phoneNumber or elevenNumber):
        if True:    
            try:
                
                #HERE: write phone number to phoneLog file and shortURL to exist file
                #with open(str(filePath), "a+") as text_file:
                 #       print('here')
                  #      text_file.write("\n"+str(shortURL))
                
                if (phoneNumber):
                    with open(str(phoneLogs), "a+") as text_file:
                        text_file.write("\n"+str(phoneNumber))
                    with open(str(filePath), "a+") as text_file:
                        text_file.write("\n"+str(shortURL))
                    print('contetn exist phone number'+' '+ str(phoneNumber[0]))
                    text='___________________________________________'+'\n'+shortURL+"\n"+content+"\n"
                    response = requests.post(
                             url='https://api.telegram.org/bot{0}/{1}'.format('402534967:AAH-vMKfI1OlpNnusY0HD5kpWDGn2QJl3AA', 'sendMessage'),
                             data={'chat_id':rentOrSale, 'text': text}
                             ).json()
                    return False
                elif (elevenNumber):

                    with open(str(phoneLogs), "a+") as txtFile:
                        txtFile.write("\n0"+str(int(elevenNumber[0])))

                    with open(str(filePath), "a+") as text_file:
                        text_file.write("\n"+str(shortURL))

                    print('contetn exist phone number'+' 0'+ str(int(elevenNumber[0])))

                    text='___________________________________________'+'\n'+shortURL+"\n"+content+"\n"
                    
                    response = requests.post(
                             url='https://api.telegram.org/bot{0}/{1}'.format('402534967:AAH-vMKfI1OlpNnusY0HD5kpWDGn2QJl3AA', 'sendMessage'),
                             data={'chat_id':rentOrSale, 'text': text}
                             #data={'chat_id': '-1001113850377', 'text': text}
                             ).json()
                    return False
                #HERE:__________________________________
                    
                for word in blackList:
                    if(word in content):
                            print('A word of black list: '+str(word))
                            with open(str(filePath), "a+") as text_file:
                                text_file.write("\n"+str(shortURL))
                            #HERE: check if phone number and black word is in conent, return false
                            text='___________________________________________'+'\n'+shortURL+"\n"+content+"\n"
                            response = requests.post(
                             url='https://api.telegram.org/bot{0}/{1}'.format('402534967:AAH-vMKfI1OlpNnusY0HD5kpWDGn2QJl3AA', 'sendMessage'),
                             data={'chat_id':rentOrSale, 'text': text}
                             #data={'chat_id': '-1001113850377', 'text': text}
                             ).json()
                            return False
                return True        

            except Exception as e:
                print('cant Write exist ads or phone number to file ' + str(e))   
                return False    
 
            


        
        
        
        #______ if word of black list is in content return False 
        
        #blackList=open('blackList.txt','r',encoding='utf8').read().split(',')                
        #blackList.remove('')
        #blackList.remove('\ufeff')
        
        
        #______ agar matn az tamami filterha oboor konad angah return True
        #return True
    
    except Exception as e:
        print('cant run contentNotExistInBlackList function!!!\n '+str(e))
        return True



def mainFunc(channelAddress,divarURL,rentOrSale):
   try:
    token='402534967:AAH-vMKfI1OlpNnusY0HD5kpWDGn2QJl3AA'
    method='sendMessage'
    
    aaa=divarURL
    href=getAdsURL(firstPageURL=aaa)
    i=0
    for item in href:
     content=GetContent(item)
     shortURL=getShortURL('https://divar.ir'+item.get('href'))
     i+=1
     if shortURL in open(str(filePath)).read().split():
         print('Exist Ads '+str(i))
         #with open(str(filePath), "a+") as text_file:
          #   text_file.write("\n"+str(shortURL))
         break
     if(contentNotExistInBlackList(content,shortURL,rentOrSale)):#send contetn for check in BlackList and URL for not exist
        print('Sending! Please wait...')
        try:
             with open(str(filePath), "a+") as text_file:
                text_file.write("\n"+str(shortURL))
        except Exception as e:
             print('cant Write exist ads to file ' + str(e))
        try:
             text='___________________________________________'+'\n'+shortURL+"\n"+content+"\n"
             response = requests.post(
             url='https://api.telegram.org/bot{0}/{1}'.format(token, method),
             data={'chat_id':channelAddress, 'text': text}
             ).json()
        except Exception as e:
            print('cant send data '+str(e))
   except Exception as e:
       print('cant execute code : '+ str(e))
       print(channelAddress)



TimePerSec=360
#split lines of txt file by # sign 
rowData=open('original_adress_test.txt','r').read().split('#')
splitedData=[]
for line in rowData:
    #split columns of txt file by 
    splitedData.append(line.split(';'))

    
for i in range(int(len(splitedData)-1)):#int(len(splitedData)-10)
    channelAddress = str(splitedData[i+1][1])
    divarURL=str(splitedData[i+1][2])
    rentOrSale=splitedData[i+1][0][0]#if rentOrSale=a -> sale; if ==b -> rent
    
    if(rentOrSale=='a'):
            rentOrSale='@hazfiaat'
    elif(rentOrSale=='b'):
            rentOrSale='@rentDeleted'
            print(str(i)+'- '+rentOrSale)
#    print(channelAddress+' '+rentOrSale)
    schedule.every(TimePerSec).seconds.do(mainFunc,channelAddress , divarURL,rentOrSale)   

while 1:
    time.sleep(3)
    schedule.run_pending()
  

"""
for i in range(int(len(adressChUrl))):
    token='402534967:AAH-vMKfI1OlpNnusY0HD5kpWDGn2QJl3AA'
    method='sendMessage'
    channelAddress = str(adressChUrl.iloc[i,0])
    
    response = requests.post(
            url='https://api.telegram.org/bot{0}/{1}'.format(token, method),
            data={'chat_id': '-1001113850377', 'text': 'testing...'}
            ).json()
    print(str(response) + ' ' + str(channelAddress))
    """
"""

token='402534967:AAH-vMKfI1OlpNnusY0HD5kpWDGn2QJl3AA'
method='sendMessage'
response = requests.post(
            url='https://api.telegram.org/bot{0}/{1}'.format(token, method),
            data={'chat_id': '@adada123', 'text': 'testing...'}
            ).json()
print(str(response) )

"""

















    
