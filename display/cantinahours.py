# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 19:43:05 2019

@author: jhl
"""

from lxml import html, etree
import requests

HANGAREN_INDEX = 13
REALFAG_INDEX = 17

def getOpeningHours():
    
    page = requests.get('https://www.sit.no/mat')
    #page = requests.get('https://bartebuss.no/NSR:Quay:75708')
    
    tree = html.fromstring(page.content)
    
    open_hours = tree.xpath('//div[@class="eat-hours"]/text()')
    realfag_hours = ""
    hangaren_hours = ""
    for i in range(12,23):
        realfag_hours += open_hours[REALFAG_INDEX][i]
        hangaren_hours += open_hours[HANGAREN_INDEX][i]
    return realfag_hours, hangaren_hours
    