# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 23:35:34 2017

@author: dmitrys
"""

####################
#### НКО парсер ####
####################


import sys
sys.path.append('/Users/dmitrys/anaconda2/lib/python2.7/site-packages')
import re
from bs4 import BeautifulSoup
import time
import pandas as pd
import numpy as np
from urllib.request import Request, urlopen
import requests

from user_agent import generate_user_agent


def html_stripper(text):
    return re.sub('<[^<]+?>', '', str(text))

main_url = "http://ivsezaodnogo.ru/foundations?search_by=name&page={}"
sub_url = "http://ivsezaodnogo.ru/foundations/{}"
img_url = "http://ivsezaodnogo.ru/uploads/foundation/logo/{}/thumb_profilepic.jpg"

nko_urls = set()

def getUrls(page):
    req = Request(main_url.format(page), headers={'User-Agent': generate_user_agent()})
    webpage = urlopen(req).read()
    soup = BeautifulSoup(webpage, "lxml")
    urls_block = soup.find('div', attrs={'class':'js-lazy-loader b-foundations-list'}).findAll('a', attrs={'class':'link'})
    nko_urls = re.findall(r'\d+', str(urls_block))
    return nko_urls
    
for i in range(1,40):
    urls = getUrls(i)
    time.sleep(0.3)
    if len(urls)!=0:
        nko_urls.update(urls)
    else:
        break
    
nko_urls = list(nko_urls)


def getPage(page):
    req = Request(sub_url.format(page), headers={'User-Agent': generate_user_agent()})
    webpage = urlopen(req).read()
    soup = BeautifulSoup(webpage, "lxml")
    return soup

class pageNKO:
    def __init__(self, number):
        self.number = number
    

        
        
page = getPage(nko_urls[0])

organization_name = html_stripper(page.find("h1"))

information = page.find("div", attrs={'class':'groups'})

information = re.split("Решает проблемы|Кому оказывается помощь", str(information))

problems_solving = html_stripper(information[1]).split('\n')
problems_solving = [x for x in problems_solving if x] # удаляем пустые значения
problems_solving = list(set(problems_solving)) # удаляем дубликаты
problems_solving.remove("показать все")
problems_solving.remove('свернуть ↑')

audience = html_stripper(information[2]).split('\n')
audience = [x for x in audience if x]

def getImage(number):
    img_data = requests.get(img_url.format(number)).content
    with open('/Users/dmitrys/Desktop/DataProjects/OpenDataNKO/images/nko_img_{}.jpg'.format(number), 'wb') as handler:
        handler.write(img_data)

