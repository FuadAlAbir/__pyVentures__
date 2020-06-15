import requests
import bs4
from time import sleep
import os

                    
url = 'https://www.coursera.org/learn/introduction-genomics/home/week/1'

try:
    resource = requests.get(url, timeout = 3.0)
except requests.ConnectionError as e:
    print(url + ',CONNECTION ERROR: ' + str(e) + '\n')
    
except requests.Timeout as e:
    print(url + ',TIMEOUT: ' + str(e) + '\n')
    
except requests.RequestException as e:
    print(url + ',ERROR: ' + str(e) + '\n')
    
except KeyboardInterrupt:
    print('KEYBOARD INTERRUPT,NONE\n')
    
soup = bs4.BeautifulSoup(resource.text, 'lxml')
n_news_container = soup.findAll('li', {'class':'rc-NamedItemList'})
print(n_news_container)
