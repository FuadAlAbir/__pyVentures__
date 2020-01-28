import pandas as pd
import requests
import bs4
from time import sleep
import os

def get_resource( url ):
    try:
        resource = requests.get(url)
    except requests.ConnectionError as e:
        e_file.write(url + ',CONNECTION ERROR: ' + str(e) + '\n')
        return
    except requests.Timeout as e:
        e_file.write(url + ',TIMEOUT: ' + str(e) + '\n')
        return
    except requests.RequestException as e:
        e_file.write(url + ',ERROR: ' + str(e) + '\n')
        return
    except KeyboardInterrupt:
        e_file.write('KEYBOARD INTERRUPT,NONE\n')
        return
    return resource


filename = 'nayadiganta-deadNews.csv'

if os.path.exists(filename):
    mode = 'a'
else:
    mode = 'w' 
       
d_file = open(filename, mode)

headers = 'date,title,ref\n'

if (mode == 'w'):
    d_file.write(headers)


for month in range(1, 8):
    if month < 10:
        month = '0' + str(month)
    else:
        month = str(month)
    for day in range(1, 32):
        if day < 10:
            day = '0' + str(day)
        else:
            day = str(day)
        date = '2019-' + month + '-' + day
        flag = 0
        
        url = 'http://www.dailynayadiganta.com/archive/' + date
        resource = get_resource(url)
        soup = bs4.BeautifulSoup(resource.text, 'lxml')
        n_news_container = soup.find('ol', {'class':'margin archive-news-list'})
        n_news_list = n_news_container.findAll('li', {'class':''})
        for i in range(1, len(n_news_list)):
            title = n_news_list[i].a.find('h1', {'class': 'title'}).text.strip()
            ref = n_news_list[i].a['href']
            if title.find('%', 0, len(title)) != -1:
                flag = 1
                print(date + ': ' + title)
                d_file.write(date + ',' + title + ',' + ref + '\n')
        if (flag == 0):
            print(date + ': None')
                
d_file.close()
