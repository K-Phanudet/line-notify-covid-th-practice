import requests,time
from datetime import datetime
from pytz import timezone
from os import environ
from config.envConfig import *

tmpDateTime = ""

def getDateAPI(dateTimeBkk):
    data = requests.get('https://covid19.th-stat.com/api/open/today/')

    print('Get data from API')
    updateDate = data.json()['UpdateDate']

    print('Checking API update with current date :: Now {} :: API Update {} '.format(dateTimeBkk,updateDate))
    if(str(updateDate.split()[0])== dateTimeBkk):
        confirmed = data.json()['Confirmed']
        recovered = data.json()['Recovered']
        hospitalized = data.json()['Hospitalized']
        deaths = data.json()['Deaths']
        newConfirmed = data.json()['NewConfirmed']
        newRecovered = data.json()['NewRecovered']
        newDeaths = data.json()['NewDeaths']
        source = data.json()['Source']
        text_mes = """
ยอดผู้ป่วยโควิดรายวันในไทย 
---------------------
+ ติดเชื้อสะสม     {}(เพิ่มขึ้น {})
+ รักษาตัวอยู่ รพ   {}
+ หายแล้ว        {}(เพิ่มขึ้น {})
+ เสียชีวิต        {}(เพิ่มขึ้น {})
+ อัตราการเสียชีวิต  {}
+ อัตราการหาย     {}
+ อัพเดตเมื่อ       {}
+ ข้อมูลโดย       {}
DevNotify by FlyInSpace
""".format(str(confirmed),str(newConfirmed),str(hospitalized)
        ,str(recovered),str(newRecovered),str(deaths),str(newDeaths)
        ,str(round((deaths*100)/confirmed,2)),str(round((recovered*100)/confirmed,2))
        ,str(updateDate),str(source))     

        return text_mes
    else:
        return 'wait for update'

while(True):    
    print('processing ...')
    nowUtc = datetime.now(timezone('UTC'))
    nowBkk = nowUtc.astimezone(timezone('Asia/Bangkok'))
    dateNow = nowBkk.date().strftime("%d/%m/%Y")

    print("Current Date {} and Tamp Date {}".format(nowBkk.strtime("%d/%m/%Y %H:%M:%S"),tmpDateTime))

    if(tmpDateTime != dateNow):

        msg = getDateAPI(dateNow)
        print("Get data :: {} ".format(msg))

        if(msg != 'wait for update'):
            
            reqMsg = requests.post(url, headers=headers, data = {'message':msg})
            tmpDateTime = dateNow
            print('Result post request :: {}'.format(reqMsg))
            print('Delay 3 hour ...')
            time.sleep(3600*3)

        else:

            print('Delay 5 minute ...')
            time.sleep(60*5)


