# -*- coding: utf-8 -*-
"""
Created on Sun Nov 29 13:01:11 2020

@author: Maxence
"""

import requests
from bs4 import BeautifulSoup
from urllib.request import urlretrieve
from os import system

def find_card(card_name) :
    URL = 'https://www.scryfall.com/search?q=' + '+'.join(card_name)
    result = requests.get(URL)
    soup = BeautifulSoup(result.content, 'html.parser')
    cards = soup.find_all(class_= "card-grid-item-card")

    if cards != [] :
        parsedURLs =[card.get('href').split('/') for card in cards]
        for i, url in enumerate(parsedURLs) :
            if url[-1] == '-'.join(card_name) :
                return requests.get('/'.join(url))
    else :
        return result

deck = 'brudiclad'
download_path = deck + '_img/'
command = 'mkdir ' + download_path.rstrip('/')
system(command)
#system('mkdir test')

with open('/Users/Maxence/Desktop/MTG Lists/' + deck + '.txt', 'r') as f :
    liste_lignes = f.readlines()
cards_list = []
for line in liste_lignes[1:] :
    if '(' in line :
        line, _ = line.split('(')
    line = line.replace(',', '')
    line = line.replace("'s", "s")
    line = line.replace(' // ', ' ')
    line = line.rstrip(' ')
    line = line.lower()
    if line != '' and '\n' not in line:
        cards_list.append(' '.join(line.split(' ')[1:]))
#print(cards_list)

for name in cards_list :
    card_name = name.split(' ')
    card_page = find_card(card_name)
        
    soup = BeautifulSoup(card_page.content, 'html.parser')
    front_img = soup.find(class_="card-image-front")
    image = front_img.find('img')
    urlretrieve(image.get('src'), download_path + name + '.png')
    
    back_img = soup.find(class_="card-image-back")
    if back_img != None :
        image = back_img.find('img')
        urlretrieve(image.get('src'), download_path + name + '_back.png')
        
    tokens = soup.find_all('td')
    for i, token in enumerate(tokens) :
        try :
            if token.find('a').get('href').split('/')[-1] != '-'.join(card_name) :
                urlretrieve(token.find('a')["data-card-image"], download_path + name + '_token{}.png'.format(i))
        except :
            pass
