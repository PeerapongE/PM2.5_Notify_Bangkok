# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 21:44:11 2018

@author: PeerapongE
"""

import urllib
import urllib.parse
import json
import time
import requests

start_time = time.time()
time_old = ''


#LINE_ACCESS_TOKEN = '' # Individual
LINE_ACCESS_TOKEN = 'bNZ5dgvoKGtxiQ4peBolX4fqoj9bxWU6VnlSvFU9oLu' # PM2.5 Alert
# from http://aqicn.org/data-platform/token/#/


AQI_TOKEN  = '17ad20c5ee5c3a8d264063fef00af604e24e33d5'   #peeraponge@gmail.com
#AQI_TOKEN2 = '17ad20c5ee5c3a8d264063fef00af604e24e33d5'  #peeraponge@pttep.com

url_page = 'https://api.waqi.info/search/?token=' + AQI_TOKEN + '&keyword=Chulalongkorn%20Hospital'

# https://api.waqi.info/search/?token=327a2f67c821f02e6a40c0851aa6240bf46a4889&keyword=Chulalongkorn%20Hospital

# Function to get data from AQI

# Example:
# https://api.waqi.info/search/?token=327a2f67c821f02e6a40c0851aa6240bf46a4889&keyword=Chulalongkorn%20Hospital
# https://api.waqi.info/search/?token=327a2f67c821f02e6a40c0851aa6240bf46a4889&city=Bangkok
def clear():
    print('\n'*50)
    
def func_get_aqi(url_page):
    json_page = urllib.request.urlopen(url_page)
    json_data = json.loads(json_page.read().decode())


    aqi = json_data['data'][0]['aqi']
    place = json_data['data'][0]['station']['name']

    date = json_data['data'][0]['time']['stime'].split(' ')[0]
    time_data = json_data['data'][0]['time']['stime'].split(' ')[1]
    
    aqi_num = int(aqi)
    
    if aqi_num < 50:
        quality = 'Good'
    elif aqi_num < 100:
        quality = 'Moderate'
    elif aqi_num < 150:
        quality = 'Unhealthy for sensitive group'
    elif aqi_num < 200:
        quality = 'Unhealthy'
    elif aqi_num < 300:
        quality = 'Very Unhealthy'
    else :
        quality = 'Harzardous'    
        
    return(aqi,place,date,time_data,quality)




def func_line_notify(message, LINE_ACCESS_TOKEN):
    url = 'https://notify-api.line.me/api/notify'
    msg = '' # Modify this line as header data
    msg = urllib.parse.urlencode({'message': msg})
    send_msg = msg + message
    LINE_HEADERS = {'Content-Type': 'application/x-www-form-urlencoded',
                    'Authorization': 'Bearer '+ LINE_ACCESS_TOKEN}
    session = requests.Session()
    response = session.post(url, headers=LINE_HEADERS, data=send_msg)
    return response

# begin loop here
for i in range(0,20000): 
    print('----- Step : ' + str(i) + ' ----- ' + 'Current time : ' + time.ctime() + ' -----') # to keep tracking running activity
    
    #Error handling for aqi scraping
    try:
        aqi,place,date,time_data,quality = func_get_aqi(url_page)
    except (RuntimeError, TypeError, NameError, ValueError, urllib.error.URLError):
        time_data = time_old # to keep forward
        aqi = '0'
        print('error catched')
        
    #print(aqi)
    #print(type(aqi))
    #print(float(aqi) > 80)
    Threshold = 100
    if (time_data != time_old) and (float(aqi) > Threshold): #if time change, then send line message
    
        aqi_msg = 'Date : '+ date + ' , Time : ' + time_data + ' , At ' + place + ' , PM-2.5 = ' + aqi + ' , Quality is ' + quality

        ## Line notify
##
##        url = 'https://notify-api.line.me/api/notify'
##        msg = '' # Modify this line as header data
##        msg = urllib.parse.urlencode({'message': msg})
##        send_msg = msg + aqi_msg
##        LINE_HEADERS = {'Content-Type': 'application/x-www-form-urlencoded',
##                        'Authorization': 'Bearer '+LINE_ACCESS_TOKEN}
##        session = requests.Session()
##        response = session.post(url, headers=LINE_HEADERS, data=send_msg)
##        
        response = func_line_notify(aqi_msg, LINE_ACCESS_TOKEN)
        
        print(response.text)# to check status of LINE notify
        print(aqi_msg)
        time_old = time_data # Keep update old time
    else:
        if (time_data == time_old) : # time does not change
            print('No new update')
        else: # time change, but not exceed threshold
            print('PM2.5 = ' + str(aqi) + ', does not exceed Threshold')
            time_old = time_data # Keep update old time
    
    
    time.sleep(5) # 600 seconds = 10 minutes