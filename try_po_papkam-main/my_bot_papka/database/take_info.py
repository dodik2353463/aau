import requests
from bs4 import BeautifulSoup
import re


lst = ['<a href="/holidays/january/">Январь</a>',
    '<a href="/holidays/february/">Февраль</a>',
    '<a href="/holidays/march/">Март</a>',
    '<a href="/holidays/april/">Апрель</a>',
    '<a href="/holidays/may/">Май</a>',
    '<a href="/holidays/june/">Июнь</a>',
    '<a href="/holidays/july/">Июль</a>',
    '<a href="/holidays/august/">Август</a>',
    '<a href="/holidays/september/">Сентябрь</a>',
    '<a href="/holidays/october/">Октябрь</a>',
    '<a href="/holidays/november/">Ноябрь</a>',
    '<a href="/holidays/december/">Декабрь</a>']

def find_info_day(day, month):
    responce2 = requests.get('https://www.calend.ru' + lst[month-1].split('"')[1])
    if responce2.status_code == 200:
        responce2.encoding = 'utf-8'
        bs2 = BeautifulSoup(responce2.text, features="html.parser")
        table2 = bs2.find_all(name='li', attrs={'class': 'full'})
        
        prazdnik = ''
        for row in table2:
            if row.find(name='span', attrs={'class': 'dataNum'}).find(name='a').get('href') == f'/day/2024-{month}-{day}/':
                #print(listik_all_prazdn_of_day.append(row.find_all(name='span', attrs={'class': 'caption'})))
                prazdnik = row.find_all(name='span', attrs={'class': 'caption'})[0].find(name='a').get('href')
                break
    
    responce = requests.get(prazdnik)
    if responce.status_code == 200:
        responce.encoding = 'utf-8'
        bs = BeautifulSoup(responce.text, features="html.parser")
        title = bs.find(name='h1', attrs={'itemprop': 'name headline'}).text
        phars = bs.find(name='div', attrs={'class': 'maintext'}).find_all(name='p')
        return title, re.sub(r'<.*?>', "", str(phars[0]))
