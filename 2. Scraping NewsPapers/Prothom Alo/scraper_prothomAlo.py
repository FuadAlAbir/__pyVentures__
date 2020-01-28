import requests
import bs4
from time import sleep
import os

page = 0
edition = ['print', 'online']
whiteFlag = 0 # for the month's days greater than usual, used at the start of while

for year in range(2019, 2020):
    filename = 'prothomAlo-2019-07x.csv'
    if os.path.exists(filename):
        mode = 'a'
    else:
        mode = 'w'    
    f = open(filename, mode)
    headers = 'date,title,subtitle,author,comment,ref,section,media,page\n'
    if (mode == 'w'):
        f.write(headers)
        
    exceptionFilename = 'exceptions-' + str(year)+ '.csv'
    e_file = open(exceptionFilename, 'w')
    e_file.write('url,exceptions\n')

    logFilename = 'log-' + str(year) + '.csv'
    log_file = open(logFilename, 'w')
    log_file.write('date,media,page\n')

    for months in range(7, 8):
        if months < 10:
            months = '0' + str(months)
        for days in range(21, 32):
            if days < 10:
                days = '0' + str(days)
            date = str(year) + '-' + str(months) + '-' + str(days)
            for m in range(len(edition)):
                media = edition[m]
                
                while True:
                    if whiteFlag:
                        whiteFlag = 0
                        page = 0
                        break
                    page = page + 1
                    
                    url = 'https://www.prothomalo.com/archive/' + str(date) + '?edition=' + media + '&page=' + str(page)

                    try:
                        resource = requests.get(url, timeout = 3.0)
#                        sleep(0.3)
                    except requests.ConnectionError as e:
                        e_file.write(url + ',CONNECTION ERROR: ' + str(e) + '\n')
                        continue
                    except requests.Timeout as e:
                        e_file.write(url + ',TIMEOUT: ' + str(e) + '\n')
                        continue
                    except requests.RequestException as e:
                        e_file.write(url + ',ERROR: ' + str(e) + '\n')
                        continue
                    except KeyboardInterrupt:
                        e_file.write('KEYBOARD INTERRUPT,NONE\n')
                        
                    soup = bs4.BeautifulSoup(resource.text, 'lxml')
                    n_news_container = soup.findAll('div', {'class':'content_type_article'})
                    
                    if (len(n_news_container) == 0):
                        log_file.write(date + ',' + media + ',' + str(page - 1) + '\n')
                        print("DONE: " + date + ' ' + media)
                        #sleep(1.0)
                        page = 0
                        break

                    for i in range(len(n_news_container)):
                        if n_news_container[i].div.h2 is not None:
                            title = n_news_container[i].div.h2.find('span', {'class': 'title'}).text

                            subtitle = n_news_container[i].div.h2.find('span', {'class': 'subtitle'})
                            if subtitle is not None:
                                subtitle = subtitle.text
                            else:
                                subtitle = ''
                                
                            author = n_news_container[i].div.div.span
                            if author is not None:
                                author = author.text
                            else:
                                author = ''
                                
                            comment = n_news_container[i].div.div.a
                            if comment is not None:
                                comment = comment.text.split(' ')[0]
                            else:
                                comment = ''
                                
                            offset = 'https://www.prothomalo.com'
                            ref = offset + n_news_container[i].a['href']
                            section = ref.split('/')[3]
                            
                            f.write(date + ',' + title.replace(',', '.') + ',' + subtitle.replace(',', '.') + ',' + author.replace(',', '.') + ',' + comment + ',' + ref + ',' + section + ',' + media + ',' + str(page) + '\n')
                        else:
                            whiteFlag = 1
                            e_file.write(url + ',DATE NOT VALID:' + date + ' page:' + str(page) + '\n')
                            break

    log_file.close()
    e_file.close()
    f.close()
