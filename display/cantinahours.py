# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 19:43:05 2019

@author: jhl
"""

from lxml import html
import requests

HANGAREN_INDEX = 12
REALFAG_INDEX = 16

def getCantinaInfo():
    
    page = requests.get('https://www.sit.no/mat')
    #page = requests.get('https://bartebuss.no/NSR:Quay:75708')
    
    tree = html.fromstring(page.content)
    
    open_hours = tree.xpath('//div[@class="eat-hours"]/text()')
    for i, c in enumerate(open_hours[REALFAG_INDEX]):
        if c.isdigit():
            time_start_index = i
            break
    realfag_hours = ""
    hangaren_hours = ""
    for i in range(time_start_index,(time_start_index + 11)):
        realfag_hours += open_hours[REALFAG_INDEX][i]
        hangaren_hours += open_hours[HANGAREN_INDEX][i]
    
    
    daily_dishes = tree.xpath('//li[contains(@class, \'current-day\')]//li[@class="dishes__dishes__dish dishes__dishes__dish--new-day"]/text()')
    realfag_food = ""
    hangaren_food = ""
    
    return realfag_hours, hangaren_hours, realfag_food, hangaren_food