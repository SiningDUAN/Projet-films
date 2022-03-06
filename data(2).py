#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar  6 16:13:55 2022

@author: zhangyajie
"""

from bs4 import BeautifulSoup
import re

def clean(text):
    soup =  BeautifulSoup(text, 'html.parser')
    soup.find_all('div', class_= "info-wrapper main")
    #get grade
    content = soup.find_all('ul', class_ = 'no-bullets film-score color--main-blue d-none')
    grade = len(re.findall("plein", str(content)))
    #get title
    title = soup.find('h1', class_ = 'block--title color--dark-blue text-uppercase').text
    #get publication date
    contents=soup.find_all('p', class_ = 'color--grey')
    date,director,actors=None,None,None
    for content in contents:
        # print(content.text)
        
        if 'Sortie le' in content.text:
            part_2_content=content.find_all('span')
            # print(part_2_content)
            date = part_2_content[0].text
            # type = part_2_content[1].text
        #Directeur
        if re.findall(r'\bDe\b', content.text):
            director = content.find('span').text
        #Acteur
        if re.findall(r'\bAvec\b', content.text):
            actors = content.find('span').text
    #synopsis
    synopsis_div = soup.find_all('div', class_ = 'group-info d-none d-md-block')
    for div in synopsis_div:
        if 'Synopsis' in div.text:
            synopsis = div.find('p',class_='color--dark-blue').text
    # print(synopsis_div)
    
    type=soup.find('p', class_ = 'color--dark-blue').text
    return grade,title,date,type,director,actors,synopsis