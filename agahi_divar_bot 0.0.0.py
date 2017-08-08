import requests
from datetime import date
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import telegram
import time
import sqlite3
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
#_________________________________________________________________________________________________________________________________________________
#________________________________________________________User Side _______________________________________________________________________________
#_________________________________________________________________________________________________________________________________________________



        
def insert2DB(ID,name,telegramID,reagent,isAdmin,payed,payedThisMount,regDate):
    try:
        db="soverflow.sqlite"
        dbconnect = sqlite3.connect(db)
        c = dbconnect.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS customer
                    (id int not null primary key, name varchar(50), telegramID varchar(30),reagent int(20) not null DEFAULT 175224774,isAdmin bool not null DEFAULT 0,
                    `payed` INTEGER DEFAULT 0,`payedThisMount`	INTEGER DEFAULT 0,`regDate` TEXT,`lastPaymentDate`	TEXT DEFAULT '2016-01-01')""")
        c.execute("""INSERT INTO customer (id,name,telegramID,reagent,isAdmin,payed,payedThisMount,regDate) VALUES (?,?,?,?,?,?,?,?)""",
                  (ID,name,telegramID,reagent,isAdmin,payed,0,regDate))
        dbconnect.commit()
        c.close()
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
def start(bot, update):
    try:  
        reagentID = (update.message.text)[7:]
        user_ID=update.message.from_user.id
        telegramID = update.message.from_user.username
        txt1=' سلام '
        name=" "
        if(update.message.from_user.first_name):
                name += str(update.message.from_user.first_name)
        if(update.message.from_user.last_name):
                name+=' '+ str(update.message.from_user.last_name)
        txt1+=name + ' '
        txt1 += 'عزيز'+'\n' + 'به فایلینگ املاک و مسکن ملت فایل خوش آمدید. برای یک هفته عضویت و دریافت فایل شماره تماس زیر را ذخیره و پیام بعدی را برایش فوروارد کنید. با تشکر \nشماره تماس ملت فایل 09195835818\nآی دی ملت فایل در تلگرام @AdminMelatFile'
        txt2=' شماره عضویت ' + name +'\n' + str(update.message.from_user.id)+'\n' +' بنده تقاضای عضویت و دریافت فایل دارم '
        #txt3=''
        #txt4=(update.message.text[7:])
        #txt5= 'شما تاکنون 0 نفر را دعوت کرده ايد'
        
        
        if(bool(existUser(user_ID))):
               update.message.reply_text('شما پيش از اين عضو سيستم شده ايد، براي دريافت بنر تبليغاتي اختصاصي خودتان /eshterak را لمس کنيد.')
               update.message.reply_text('/commands : دستورات بات')
               
        elif bool(reagentID) and not(existUser(user_ID)):
            print('shoma tavassote in id moarrefi shodeiid: ' + str(reagentID))
            #insert new user to data base
            insert2DB(user_ID,name,telegramID,reagentID,isAdmin='0',payed='0',payedThisMount='0',regDate=date.today())
            print('voroode ettelaat movafagh bood')
            update.message.reply_text(txt1 +'\n' +'\n' +'\n' +'\n')
            update.message.reply_text(txt2)
            #update.message.reply_text('/commands : دستورات بات')
            
        elif(not(reagentID) and not(existUser(user_ID))):    
            print('shoma tavassote kasi moarrefi nashodeiid!')
            print('dar hale vared kardan be DB.')
            insert2DB(user_ID,name,telegramID,reagent='175224774',isAdmin='0',payed='0',payedThisMount='0',regDate=date.today())
            print('Succussfuly inserted!')
            update.message.reply_text(txt1 +'\n' +'\n' +'\n' +'\n')
            update.message.reply_text(txt2)
            #update.message.reply_text('/commands : دستورات بات')
    except Exception as e:
        print("can't access to DB, Error: "+str(e))
    #viewButtons(bot, update,'start')
    

    

    
def eshterak(bot, update):
    txt1='تبريک! \n لينک اختصاصي بات شما فعال شد.'
    txt2='جهت معرفی ربات به دوستانتان ،پیام پایین را برایشان ارسال کنید.'
    update.message.reply_text(txt1 +'\n'+txt2 +'\n')
    
    time.sleep(1)
    
    txt3='اين ربات فايلاي روزنامه ها رو هر روز صبح، و آگهي هاي ديوار رو به محض تاييد  شدن براتون ارسال ميکنه، اونم رايگان!!!'
    
    txt6='https://telegram.me/agahi_amlak_bot?start='+str(update.message.from_user.id)#update.message.from_user.id
    bot.sendPhoto(update.message.from_user.id,photo='http://imgur.com/a/EVVqV',caption='\n' +'\n'+txt3 + '\n'+txt6)
    time.sleep(1)
    update.message.reply_text('/commands : دستورات بات')
    #update.message.reply_text(txt3 +'\n'+txt4 +'\n'+txt5 + '\n'+txt6)
def ozv(bot, update):
    print(update.message.from_user)
    try:
        #update.message.reply_text('hi')
        db="soverflow.sqlite"
        dbconnect = sqlite3.connect(db)
        c = dbconnect.cursor()
        a=c.execute("""SELECT id,telegramID FROM customer WHERE reagent = ?""",(update.message.from_user.id,))
        rows = a.fetchall()
        i=0
        for row in rows:
            i+=1
            update.message.reply_text(str(i)+' - ' + str(row))
        print(i)
        #update.message.reply_text('Ok') 
        dbconnect.commit()
        c.close() 
        update.message.reply_text(' شما تا کنون '  +str(i)+ 'نفر را عضو کرده ايد، ليست افرادي که توسط شما عضو شده اند را در بالا مشاهده کنيد.')
        update.message.reply_text('/commands : دستورات بات')
    except Exception as e:
        update.message.reply_text('در اتصال به پايگاه داده مشکلي پيش امده است، لطفا صبور باشيد و چند دقيقه بعد امتحان کنيد.')
        update.message.reply_text('/commands : دستورات بات')
        print(str(e))
        
def activeUsers(bot, update):
    try:
        db="soverflow.sqlite"
        dbconnect = sqlite3.connect(db)
        c = dbconnect.cursor()
        a=c.execute("""SELECT id,telegramID FROM customer WHERE reagent = ? AND payed=1""",(update.message.from_user.id,))
        rows = a.fetchall()
        i=0
        if(rows):        
            for row in rows:
                i+=1
                update.message.reply_text(str(i)+' - ' + str(row))
        dbconnect.commit()
        c.close()
        if(update.message.from_user.first_name):
            txt1= str(update.message.from_user.first_name)
        if(update.message.from_user.last_name):
            txt1+=' '+ str(update.message.from_user.last_name)
        txt1 += 'عزيز'+'\n'
        update.message.reply_text(txt1 + ' تا کنون '  +str(i)+ ' نفر از افرادي که شما جذب کرده ايد، از ما خريد داشته اند.')
        update.message.reply_text('/commands : دستورات بات')
        
    except Exception as e:
        update.message.reply_text('در اتصال به پايگاه داده مشکلي پيش امده است، لطفا صبور باشيد و چند دقيقه بعد امتحان کنيد.')
        update.message.reply_text('/commands : دستورات بات')
        print(str(e))
        


def commands(bot, update):
    txt1='دستورات ربات:\n\n'
    txt2='/eshterak : مشاهده بنر اختصاصيتان جهت ارسال به دوستان \n\n'
    txt3='/ozv : مشاهده ي تمامي افرادي که جذب کرده ايد. \n\n'
    txt4='/activeusers : مشاهده افرادي که توسط شما جذب شده اند و از ما خريد کرده اند. \n\n'
    txt5='/showID دريافت کد کاربري\n\n'
    update.message.reply_text(txt1+txt5+txt3+txt2+txt4)
    #viewButtons(bot, update,'')


def showId(bot, update):
    if(update.message.from_user.first_name):
            txt1= str(update.message.from_user.first_name)
    if(update.message.from_user.last_name):
            txt1+=' '+ str(update.message.from_user.last_name)
    txt1 += 'عزيز'+'\n' + 'کد کاربري شما \n'
    txt2= update.message.from_user.id
    txt3=' ميباشد. ' 
    update.message.reply_text(txt1)
    update.message.reply_text(txt2)
    update.message.reply_text(txt3)
    time.sleep(1)
    update.message.reply_text('/commands : دستورات بات')


        
token='418884169:AAHkhQ7zbTR4Jlc985kZ2pENRHWHm6guax4'#token: agahi_amlak_bot 
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




#_____________________________User side Fuctions_______________________
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('eshterak', eshterak))
updater.dispatcher.add_handler(CommandHandler('ozv', ozv))
updater.dispatcher.add_handler(CommandHandler('commands', commands))
updater.dispatcher.add_handler(CommandHandler('activeusers', activeUsers))
updater.dispatcher.add_handler(CommandHandler('showId', showId))


#updater.dispatcher.add_handler(CallbackQueryHandler(button))
#_______________________________________________________________________
#_______________________________________________________________________








#_______________________________________________________________________
updater.start_polling()
updater.idle()









