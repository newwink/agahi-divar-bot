import requests
from datetime import date
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import telegram
import time
import sqlite3
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from threading import Thread


token='402534967:AAH-vMKfI1OlpNnusY0HD5kpWDGn2QJl3AA'
updater = Updater(token)



#_________________________________________________________________________________________________________________________________________________
#________________________________________________________Admin Side _______________________________________________________________________________
#_________________________________________________________________________________________________________________________________________________
def start(bot, update):
    token='418884169:AAHkhQ7zbTR4Jlc985kZ2pENRHWHm6guax4'
    try:
        response = requests.post(
                                    url='https://api.telegram.org/bot{0}/{1}'.format(token, 'sendMessage'),
                                    data={'chat_id': '136614002', 'text':'hi'}
                                    ).json()
        print(response)
    except Exception as e:
        print(str(e))
def existUser(user_ID):
    try:
        db="soverflow.sqlite"
        dbconnect = sqlite3.connect(db)
        c = dbconnect.cursor()
        a=c.execute("""SELECT * FROM customer WHERE id = ?""",(user_ID,))
        if bool(a.fetchone()):
            dbconnect.commit()
            c.close()
            return True
        else:
            dbconnect.commit()
            c.close()
            return False
    except Exception as e:
        print(str(e))

def extractUserInfo(id):
    print('')
    db="soverflow.sqlite"
    dbconnect = sqlite3.connect(db)
    c = dbconnect.cursor()
    a=c.execute("""SELECT * FROM customer WHERE id = ?""",(id,))
    a=a.fetchone()
    id=a[0]
    name=a[1]
    telegramID=a[2]
    reagent=a[3]
    isAdmin=a[4]
    payed=a[5]
    payedThisMount=a[6]
    regDate=a[7]
    lastPaymentDate=a[8]  
    dbconnect.commit()
    c.close()
    return id,name,telegramID,reagent,isAdmin,payed,payedThisMount,regDate,lastPaymentDate

#def kick(channel,users,bot,update,c):
        #
        #for user in users:
           # print('\n..'+user[6])


def isAdmin(bot, update):
    
    try:
        db="soverflow.sqlite"
        #print('here3')
        dbconnect = sqlite3.connect(db)
        c = dbconnect.cursor()
        #print('here2')
        a=c.execute("""SELECT isAdmin
                              FROM customer
                              WHERE id=?""",(update.message.from_user.id,))
        user = a.fetchone()
        dbconnect.commit()
        c.close()
        if(user[0]==0):
            return False
        elif(user[0]==1):
            return True
        
    except Exception as e:
      update.message.reply_text('خطا در برقراري ارتباط... لطفا چند دقيقه صبر کنيد و دوباره امتحان کنيد.')

            
    

def kickUser(bot, update):
    
    try:
        token='418884169:AAHkhQ7zbTR4Jlc985kZ2pENRHWHm6guax4'
        db="soverflow.sqlite"
        dbconnect = sqlite3.connect(db)
        c = dbconnect.cursor()
        a=c.execute("""SELECT regDate,id,isAdmin,payed,payedThisMount,lastPaymentDate,name FROM customer """)
        users = a.fetchall()
        print('aa')
        i=0
        print('_______________')
        for user in users:
            print('\n  '+str(user[1]))
            id=user[1]
            
            dbconnect = sqlite3.connect(db)
            c = dbconnect.cursor()
            numOfIntroduced=len(c.execute("""SELECT id FROM customer WHERE reagent = ?""",(id,)).fetchall())#tedade kasani ke tavassote in id moarrefi shodeand
            dbconnect.commit()
            c.close()
            regDate=user[0]
            name=user[6]
            yy=int(regDate[0:4])
            mm=int(regDate[5:7])
            dd=int(regDate[8:10])
            allUsingDays=(date.today()- date(yy,mm,dd)).days

            lastPaymentDate=user[5]
            lastPaymentYear=int(lastPaymentDate[0:4])
            lastPaymentMount=int(lastPaymentDate[5:7])
            lastPaymentDay=int(lastPaymentDate[8:10])
            payedUsingDays=(date.today()- date(lastPaymentYear,lastPaymentMount,lastPaymentDay)).days

            isAdmin=user[2]
            payed=user[3]
            payedThisMount=user[4]
            lastPaymentDate=user[5]
            method='sendMessage'
            print(channelAddress)
            for channel in channelAddress:
                #channel='@testchannel12365478954'
                print(channel)
                chatTitle=bot.getChat(channel)["title"]
                userStatusInChannel=bot.getChatMember(channel,id)["status"]
                if not(userStatusInChannel == 'member'):print(str(channel)+'    '+userStatusInChannel)
                print('allUsingDays: '+str(allUsingDays))
                time.sleep(1)    
                if (userStatusInChannel == 'member'):
                        if (payed==0):
                            if(allUsingDays > 2):
                                
                                print('\nusers allUsingDays > 1 and numOfIntroduced<5' + str(id))
                                txt1=' ' + name + ' '
                                txt1 += ' عزيز \n '
                                txt1 += ' مهلت استفاده رايگان شما از کانال ' +   chatTitle +'  به پايان رسيده است، براي خريد اشتراک به @onlineFileAdmin پيام بدهيد. \n'
                                response = requests.post(
                                url='https://api.telegram.org/bot{0}/{1}'.format(token, method),
                                data={'chat_id': id, 'text':txt1}
                                ).json()
                                bot.kickChatMember(channel,id)
                                break
                        elif (payed==1):
                            if(payedUsingDays> 30):
                                if(update.message.from_user.first_name):
                                    txt1 = str(update.message.from_user.first_name)
                                if(update.message.from_user.last_name):
                                    txt1+=' '+ str(update.message.from_user.last_name)
                                txt1 += ' عزيز \n '
                                    
                                txt2=' اشتراک شما براي استفاده از کانال '+ chatTitle +'  تمام شده است، براي خريد اشتراک با @onlineFileAdmin در تماس باشيد. '
                                print('Account credit was finished! '+ str(id))
                                response = requests.post(
                                url='https://api.telegram.org/bot{0}/{1}'.format(token, method),
                                data={'chat_id': id, 'text':txt1+txt2}
                                ).json()
                                bot.kickChatMember(channel,id)
                                break
                            if(payedUsingDays == 30):
                                txt1=('از اشتراک شما جهت استفاده از کانال '+ chatTitle +' تنها يک روز باقي مانده است، جهت خريد اشتراک با @onlineadminFile در تماس باشيد.')          
                

        dbconnect.commit()
        c.close()
        
        
    
        #bot.kickChatMember('-1001095318509','114594756')
    except Exception as e:
        print(str(e))

        

def pay(bot, update):#sabte afradi ka Pardakht dashtehand    
    try:
        if(isAdmin(bot, update)):
        
            if(update.message.text[0:4]=='/pay' and update.message.text[5:7]=='id' ):
                  
                if(update.message.text[8:].isdigit() and existUser(int(update.message.text[8:]))):
                   #HERE: Admin send a message like ('/pay id xxxx')
                    
                    try:                            
                       db="soverflow.sqlite"
                       dbconnect = sqlite3.connect(db)
                       c = dbconnect.cursor()
                       todayDate=str(date.today())
                       print(todayDate)
                       #a=c.execute("UPDATE customer SET (payed,lastPaymentDate)=( '1' , " +todayDate+ " ) WHERE id=?",(int(update.message.text[8:])),)
                       a=c.execute("""UPDATE customer SET  payed=1,payedThisMount=1,lastPaymentDate='""" +str(date.today())+"""' WHERE id=?""",(update.message.text[8:],))
                       if(c.rowcount):
                           update.message.reply_text('عمليات با موفقيت انجام شد.')
                       else:
                           update.message.reply_text('در عمليات بروز رساني مشکلي پيش آمده لطفا چند دقيقه صبر کنيد و دوباره امتحان کنيد')
                       dbconnect.commit()
                       c.close()
                    except Exception as e:
                        update.message.reply_text('در ارتباط با پايگاه داده مشکلي بوجود آمده، لطفا چند دقيقه صبر کنيد و دوباره امتحان کنيد')
                        print('::: '+str(e))
                else:# HERE: if import id isn't Int or id not exist
                    update.message.reply_text('لطفا آي دي را به درستي وارد کنيد.\n'+str(update.message.text[8:] + ' موجود نميباشد.'+'\n.'))
        else:
                update.message.reply_text(update.message.text)
    except Exception as e:
        update.message.reply_text('در اجرای عملیات مشکلي بوجود آمده، لطفا چند دقيقه صبر کنيد و دوباره امتحان کنيد')
        print(str(e))




token='402534967:AAH-vMKfI1OlpNnusY0HD5kpWDGn2QJl3AA'
updater = Updater(token)

rowData=open('original_adress_test.txt','r').read().split('#')
splitedData=[]
for line in rowData:
    #split columns of txt file by 
    splitedData.append(line.split(';'))
print(len(splitedData))
channelAddress=[]
for i in range(int(len(splitedData)-1)):#int(len(splitedData)-10)
    channelAddress.append(splitedData[i+1][1])


#_____________________________Admin side Fuctions_______________________
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('pay', pay))
updater.dispatcher.add_handler(MessageHandler(Filters.text, pay))
updater.dispatcher.add_handler(CommandHandler('kickuser', kickUser))



updater.start_polling()
updater.idle()









