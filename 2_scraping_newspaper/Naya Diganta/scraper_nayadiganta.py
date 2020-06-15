import requests
import bs4
from time import sleep
import os
from datetime import datetime

def get_resource( url ):
    try:
        resource = requests.get(url)
    except requests.ConnectionError as e:
        e_file.write(url + ',CONNECTION ERROR: ' + str(e) + '\n')
        # continue
    except requests.Timeout as e:
        e_file.write(url + ',TIMEOUT: ' + str(e) + '\n')
        # continue
    except requests.RequestException as e:
        e_file.write(url + ',ERROR: ' + str(e) + '\n')
        # continue
    except KeyboardInterrupt:
        e_file.write('KEYBOARD INTERRUPT,NONE\n')
    return resource

year = '2019'

filename = 'nayadiganta-' + year + '-05' + '.csv'
if os.path.exists(filename):
    mode = 'a'
else:
    mode = 'w'
d_file = open(filename, mode)

exceptionFilename = 'exceptions-nayadiganta-' + year + '.csv'
e_file = open(exceptionFilename, mode)

dnFilename = 'deadNews-nayadiganta-2019.csv'
dead_file = open(dnFilename, 'a')

if (mode == 'w'):
    d_file.write('date,title,subtitle,author,content,ref,section,tags,time\n')
    e_file.write('url,exceptions\n')
    dead_file.write('date,title,ref,time\n')


for month in range(5, 6):
    if month < 10:
        month = '0' + str(month)
    else:
        month = str(month)
    for day in range(1, 32):
        if day < 10:
            day = '0' + str(day)
        else:
            day = str(day)

        date = year + '-' + month + '-' + day

        url = 'http://www.dailynayadiganta.com/archive/' + date

        resource = get_resource(url)
            
        soup = bs4.BeautifulSoup(resource.text, 'lxml')
        n_news_container = soup.find('ol', {'class':'margin archive-news-list'})
        n_news_list = n_news_container.findAll('li', {'class':''})


        for i in range(len(n_news_list)):
            title = n_news_list[i].a.find('h1', {'class': 'title'}).text.strip()
            ref = n_news_list[i].a['href']
            section = ref.split('/')[3]
            time = n_news_list[i].a.find('span', {'class': 'time'}).text.strip()
            
            url = ref
            resource = get_resource(url)
            soup = bs4.BeautifulSoup(resource.text, 'lxml')
            
            news_content = soup.find('div', {'class':'news-content'})
            if news_content is not None:
                news_content_list = news_content.findAll('p', {'class':''})
                content = ''
                for p in range(len(news_content_list)):
                    content = content + news_content_list[p].text + ' '
                    
                author_tag = soup.find('div', {'class':'col-md-6 col-sm-6'})
                author = author_tag.ul.find('li', {'class':''}).text
                
                subtitle_tag = soup.find('span', {'class':'hanger'})
                if subtitle_tag is not None:
                    subtitle = subtitle_tag.text
                else:
                    subtitle = ''
                
                tags = soup.find('div', {'class':'col-md-12 tags'})
                tag = ''
                if tags is not None:
                    tags_list = tags.ul.findAll('li', {'class':''})
                    for t in range(len(tags_list)):
                        tag = tag + tags_list[t].text + '|' 
                
                print (date + ' ' + datetime.now().strftime('%H:%M:%S') + ' : ' + title)
                d_file.write(date + ',' + title.replace(',', '.') + ',' + subtitle.replace(',', '.') + ',' + author.replace(',', '.') + ',' + content.replace(',', '.') + ',' + ref.replace(',', '.') + ',' + section.replace(',', '.') + ',' + tag.replace(',', '.') + ',' + time.replace(',', '.') + '\n')
                # sleep(.3)
            else:
                dead_file.write(date + ',' + title + ',' + ref + ',' + time + '\n')

dead_file.close()
e_file.close()
d_file.close()
