#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 28 14:15:52 2019

@author: manzar
"""

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
from urllib.parse import urljoin

url = "http://www.britishsoftdrinks.com/Membership-Directory"
wb = webdriver.Chrome()
wb.get(url)

for i in range(12):
    first = int(i*1000)
    second = int(first + 1000)
    #print(first, second)
    time.sleep(1)
    wb.execute_script("window.scrollTo("+str(first)+", "+str(second)+")") 
html = wb.execute_script('return document.documentElement.outerHTML')

soup = BeautifulSoup(html, 'lxml')
divs = soup.findAll('div', {'class': 'ql_res_item member_item'})
links = []
for div in divs:
    links.append(urljoin(url, div.a.attrs['href']))

header = "Company name, Telephone, Email, Website, Contact person\n"
file = open('assignment.csv', 'w')
file.write(header)
for link in links:
    wb.get(link)
    html = wb.execute_script('return document.documentElement.outerHTML')
    soup = BeautifulSoup(html, 'lxml')
    
    name = soup.findAll('h2')
    name = name[0].span.text.lstrip().replace(',', '')#
    
    telephone = soup.findAll('div', {'class': 'field_cont lf_telephone'})
    email = soup.findAll('div', {'class': 'field_cont lf_email'})
    website = soup.findAll('div', {'class': 'field_cont lf_website'})
    contact_person = soup.findAll('div', {'class': 'field_cont lf_contact_person'})
    try:
        tel = telephone[0].span.text
    except:
        tel = 'NaN'
        
    try:
        web = website[0].a.attrs['href']
    except:
        web = 'NaN'
        
    try:
        email = email[0].a.attrs['href'].split('mailto:')[1]
    except:
        email = 'NaN'
        
    try:
        person = contact_person[0].span.text
    except:
        person = 'NaN'
    #print(tel, email, person, web)
    print(name)
    file.write(name + ', ' + tel + ', ' + email + ', ' + web + ', ' + person + '\n')
file.close()
    
    

