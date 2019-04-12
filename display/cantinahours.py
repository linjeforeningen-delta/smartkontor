# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 19:43:05 2019

@author: jhl
"""

from lxml import html
import requests

HANGAREN_LIST_INDEX = 3
REALFAG_LIST_INDEX = 4

def getCantinaHours():
    
    page = requests.get('https://www.sit.no/mat')
    #page = requests.get('https://bartebuss.no/NSR:Quay:75708')
    
    tree = html.fromstring(page.content)
    
    open_hours_raw = tree.xpath('//div[@class="eat-hours"]/text()')
    
    open_hours = []
    current_search_index = 0
    
    for i in range(len(open_hours_raw)):
        for j, c in enumerate(open_hours_raw[i]):
            if c == 'd':
                current_search_index += 1
                open_hours.append(open_hours_raw[i])
                break
            
    for i, c in enumerate(open_hours[HANGAREN_LIST_INDEX]):
        if c.isdigit():
            hangaren_time_start_index = i
            break
    
    for i, c in enumerate(open_hours[REALFAG_LIST_INDEX]):
        if c.isdigit():
            realfag_time_start_index = i
            break
    
    realfag_hours = ""
    hangaren_hours = ""
    
    for i in range(hangaren_time_start_index,(hangaren_time_start_index + 11)):
        hangaren_hours += open_hours[HANGAREN_LIST_INDEX][i]
        
    for i in range(realfag_time_start_index,(realfag_time_start_index + 11)):    
        realfag_hours += open_hours[REALFAG_LIST_INDEX][i]
    return realfag_hours, hangaren_hours
