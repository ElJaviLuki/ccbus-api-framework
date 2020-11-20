import datetime
import xml.etree.ElementTree as ET

import requests


def getTimetable(stopId):
    response = requests.post(
        url='http://atucaceres.cuatroochenta.com/webservice.php/stop-timetable-siri',
        headers={
        'Host': 'atucaceres.cuatroochenta.com',
        'User-Agent': 'Apache-HttpClient/UNAVAILABLE (java 1.4)',
    },
        data={
        'stopId': stopId
    })

    #if {'code': 'SUCCESS'} -> No hay horarios (no habrá servicio)
    root = ET.fromstring(response.content)

    estimations=[]
    for estimation in root.findall('estimation'):
        line=estimation.find('line').text
        destination=estimation.find('destino').text
        times=[]
        for time in estimation.findall('seconds'):
            times.append(int(time.text))
        estimations.append({
            'line': line,
            'destination': destination,
            'times': times
        })

    return {
        'stopId': stopId,
        'estimations': estimations
    }

def getFullTimetable():
    fullTimetable=[]
    for i in range(0,500):
        fullTimetable.append(getTimetable(i))
        print(i)
    return fullTimetable

def formatRemainingTimes(timetable):
    for estimation in timetable['estimations']:
        for i in range(len(estimation['times'])):
            estimation['times'][i]=formatTime(estimation['times'][i])
    return timetable

def formatTime(seconds):
    minutes=int(seconds/60)
    seconds=seconds%60
    hours=int(minutes/60)
    minutes=minutes%60
    return {
        'hours': hours,
        'minutes': minutes,
        'seconds': seconds
    }

def timeToStr(time):
    return str(time['hours']).zfill(2)+':'+str(time['minutes']).zfill(2)+':'+str(time['seconds']).zfill(2)

def datetimeToStr(datetime):
    return str(datetime.hour).zfill(2)+':'+str(datetime.minute).zfill(2)+':'+str(datetime.second).zfill(2)

def formatStopTimes(timetable):
    for estimation in timetable['estimations']:
        for i in range(len(estimation['times'])):
            if(estimation['times'][i]<=0):
                estimation['times'][i]='En unos instantes'
            else:
                estimation['times'][i]=datetimeToStr(datetime.datetime.now()+datetime.timedelta(seconds=estimation['times'][i]))
    return timetable

def getLine(timetable, line):
    #If we find the line
    for estimation in timetable['estimations']:
        if estimation['line']==line:
            return estimation

    #Otherwise...
    return None