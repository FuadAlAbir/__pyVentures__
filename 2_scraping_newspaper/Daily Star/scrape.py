from bs4 import BeautifulSoup
import pandas as pd
import os
import requests
from datetime import datetime
from playsound import playsound
import time


def formatStr(string):
    return " ".join(string.replace(',', '').strip().split())

def get_resource(url):
    try:
        resource = requests.get(url)
        return resource
    except requests.ConnectionError as e:
        e_file.write(date + url + ',CONNECTION ERROR: ' + str(e) + '\n')
    except requests.Timeout as e:
        e_file.write(date + url + ',TIMEOUT: ' + str(e) + '\n')
    except requests.RequestException as e:
        e_file.write(date + url + ',ERROR: ' + str(e) + '\n')
    except ConnectionResetError as e:
        e_file.write(date + url + ',CONNECTION RESET ERROR: ' + str(e) + '\n')
    except urllib3.exceptions.ProtocolError as e:
        e_file.write(date + url + ',PROTOCOL ERROR: ' + str(e) + '\n')
    except requests.exceptions.ConnectionError as e:
        e_file.write(date + url + ',CONNECTION ERROR: ' + str(e) + '\n')
    except OSError as e:
        e_file.write(date + url + ',OSError: ' + str(e) + '\n')
    except ValueError as e:
        e_file.write(date + url + ',ValueError: ' + str(e) + '\n')
    except AttributeError as e:
        e_file.write(date + url + ',AttributeError: ' + str(e) + '\n')
    except KeyboardInterrupt:
        e_file.write('NONE,KEYBOARD INTERRUPT,NONE\n')

def url_to_soup(url):
    resource = get_resource(url)
    if resource is not None:
        soup = BeautifulSoup(resource.text, 'lxml')
        return soup
    else:
        return None
    
def fileMode(filename):
    if os.path.exists(filename):
        return 'a'
    else:
        return 'w'


year = '2011'
directory = './' + year + '/'
if not os.path.exists(directory):
    os.makedirs(directory)
    
offset = 'https://www.thedailystar.net'

exceptionFilename = './' + year + '/exceptions-' + year + '.csv'
logFileName = './' + year + '/log-' + year + '.csv'

e_file = open(exceptionFilename, fileMode(exceptionFilename))
l_file = open(exceptionFilename, fileMode(logFileName))

if (fileMode(exceptionFilename) == 'w'):
    e_file.write('date,url,exceptions\n')

if (fileMode(logFileName) == 'w'):
    l_file.write('date,time_dur\n')

days = ['31', '29', '31', '30', '31', '30', '31', '31', '30', '31', '30', '31']

for m in range(5, 6):
    if m < 10:
        months = '0' + str(m)
    else:
        months = str(m)
    for day in range(1, int(days[m - 1]) + 1):
        if day < 19:
            #day = 0' + str(day)
            continue
        date = str(year) + '-' + str(months) + '-' + str(day)
        start = time.time()
        
        url = 'https://www.thedailystar.net/newspaper?date=' + date
        soup = url_to_soup(url)
        if soup is not None:
            
            df = pd.DataFrame()
            _id = []
            _date = []
            _title = []
            _subtitle = []
            _pretitle = []
            _author = []
            _section = []
            _tag = []
            _ref = []
            _content = []
            _o_time = []
            _u_time = []
            
            title = soup.findAll('h5', {'':''})
            section = soup.findAll('h2', {'':''})

            div = soup.findAll('div', {'class':'row border-right-inner equalHeight'})
            for i in range(len(section)):
                for j in range(len(div[i].findAll('li'))):
                    _section.append(section[i].text)

            for i in range(len(title)):
                _ref.append(title[i].a['href'])
                _id.append(title[i].a['href'].split('-')[-1])
                _date.append(date)

                url = offset + title[i].a['href']
                soup = url_to_soup(url)
                if soup is not None:
                    details = soup.find('div', {'class':'detailed-page'})
                
                if details is not None:
                    if details.find('h1', {'itemprop':'headline'}) is not None:
                        _title.append(formatStr(details.find('h1', {'itemprop':'headline'}).text))
                    else:
                        _title.append('')
                        
                    if details.find('div', {'class':'small-text'}) is not None:
                        _time = formatStr(details.find('div', {'class':'small-text'}).text)
                        _o_time.append(formatStr(_time.split('/')[0]))
                        _u_time.append(formatStr(_time.split('/')[1].split('D:')[1]))
                    else:
                        _o_time.append('')
                        _u_time.append('')

                    if details.find('h2', {'class':'h5'}) is not None:
                        _subtitle.append(formatStr(details.find('h2', {'class':'h5'}).text))
                    elif details.find('h2', {'class':'margin-bottom-big'}) is not None:
                        _subtitle.append(formatStr(details.find('h1', {'class':'margin-bottom-big'}).text))
                    else:
                        _subtitle.append('')

                    if details.find('h4', {'class':'uppercase'}) is not None:
                        _pretitle.append(formatStr(details.find('h4', {'class':'uppercase'}).text))
                    elif details.find('h4', {'class':'shoulder'}) is not None:
                        _pretitle.append(formatStr(details.find('h4', {'class':'shoulder'}).text))
                    else:
                        _pretitle.append('')
                        
                    if details.find('div', {'class':'author-name margin-bottom-big'}) is not None:
                        _author.append(formatStr(details.find('div', {'class':'author-name margin-bottom-big'}).find('span' , {'itemprop':'name'}).text))
                    else:
                        _author.append('')

                    content = ''
                    if details.find('div', {'class':'node-content'}) is not None:
                        contents = details.find('div', {'class':'node-content'}).findAll('p')
                        for p in range(len(contents)):
                            content = content + formatStr(contents[p].text) + ' '
                    elif details.find('div', {'class':'field-body'}) is not None:
                        contents = details.find('div', {'class':'field-body'}).findAll('p')
                        for p in range(len(contents)):
                            content = content + formatStr(contents[p].text) + ' '
                    elif details.find('div', {'class':'description'}) is not None:
                        contents = details.findAll('div', {'class':'description'})
                        for p in range(len(contents)):
                            content = content + formatStr(contents[p].find('p').text) + ' '
                    _content.append(formatStr(content))    


                    if details.findAll('li', {'class':'bg-sky italic'}) is not None:
                        tags = details.findAll('li', {'class':'bg-sky italic'})
                        tag = ''
                        for t in range(len(tags)):
                            if (t == 0):
                                tag = tags[t].text
                            else:
                                tag = tag + '|' + tags[t].text
                        _tag.append(formatStr(tag))
                    else:
                        _tag.append('')
                    print(date + datetime.now().strftime(' %H:%M:%S ') + str(len(_date)) + '-' + str(len(_title)) + '/' + str(len(title)) + ' ' + formatStr(title[i].text)[:40])
                        
                        
                elif soup is not None:
                    if soup.find('h1', {'class':'margin-bottom-big'}) is not None:
                        _title.append(formatStr(soup.find('h1', {'class':'margin-bottom-big'}).text))
                    else:
                        _title.append('')
                    
                    if soup.find('div', {'class':'small-text'}) is not None:
                        _time = formatStr(soup.find('div', {'class':'small-text'}).text)
                        _o_time.append(formatStr(_time.split('/')[0]))
                        _u_time.append(formatStr(_time.split('/')[1].split('D:')[1]))
                    else:
                        _o_time.append('')
                        _u_time.append('')

                    if soup.find('h2', {'class':'h5'}) is not None:
                        _subtitle.append(formatStr(soup.find('h2', {'class':'h5'}).text))
                    elif soup.find('h2', {'class':'margin-bottom-big'}) is not None:
                        _subtitle.append(formatStr(soup.find('h1', {'class':'margin-bottom-big'}).text))
                    else:
                        _subtitle.append('')

                    if soup.find('h4', {'class':'uppercase'}) is not None:
                        _pretitle.append(formatStr(soup.find('h4', {'class':'uppercase'}).text))
                    elif soup.find('h4', {'class':'shoulder'}) is not None:
                        _pretitle.append(formatStr(soup.find('h4', {'class':'shoulder'}).text))
                    else:
                        _pretitle.append('')
                        
                    if soup.find('div', {'class':'author-name margin-bottom-big'}) is not None:
                        _author.append(formatStr(soup.find('div', {'class':'author-name margin-bottom-big'}).find('span' , {'itemprop':'name'}).text))
                    else:
                        _author.append('')

                    content = ''
                    if soup.find('div', {'class':'node-content'}) is not None:
                        contents = soup.find('div', {'class':'node-content'}).findAll('p')
                        for p in range(len(contents)):
                            content = content + formatStr(contents[p].text) + ' '
                    elif soup.find('div', {'class':'field-body'}) is not None:
                        contents = soup.find('div', {'class':'field-body'}).findAll('p')
                        for p in range(len(contents)):
                            content = content + formatStr(contents[p].text) + ' '
                    elif soup.find('div', {'class':'description'}) is not None:
                        contents = soup.findAll('div', {'class':'description'})
                        for p in range(len(contents)):
                            if contents[p].find('p') is not None:
                                content = content + formatStr(contents[p].find('p').text) + ' '
                            else:
                                continue
                    _content.append(formatStr(content))    


                    if soup.findAll('li', {'class':'bg-sky italic'}) is not None:
                        tags = soup.findAll('li', {'class':'bg-sky italic'})
                        tag = ''
                        for t in range(len(tags)):
                            if (t == 0):
                                tag = tags[t].text
                            else:
                                tag = tag + '|' + tags[t].text
                        _tag.append(formatStr(tag))
                    else:
                        _tag.append('')
                    print(date + datetime.now().strftime(' %H:%M:%S ') + str(len(_date)) + 'S' + str(len(_title)) + '/' + str(len(title)) + ' ' + formatStr(title[i].text)[:40])

                else:
                    continue
                                
            try:
                df['id'] = _id
            except ValueError as e:
                e_file.write(date + url + ',ValueError [ID]:' + str(e) + '\n')
                print(date + ' ID ValueError: Length of values does not match length of index')
                continue
            try:
                df['date'] = _date
            except ValueError as e:
                e_file.write(date + url + ',ValueError [DATE]:' + str(e) + '\n')
                print(date + ' DATE ValueError: Length of values does not match length of index')
                continue
            try:
                df['title'] = _title
            except ValueError as e:
                e_file.write(date + url + ',ValueError [TITLE]:' + str(e) + '\n')
                print(date + ' TITLE ValueError: Length of values does not match length of index')
                continue
            try:
                df['subtitle'] = _subtitle
            except ValueError as e:
                e_file.write(date + url + ',ValueError [SUBTITLE]:' + str(e) + '\n')
                print(date + ' SUBTITLE ValueError: Length of values does not match length of index')
                continue
            try:
                df['pretitle'] = _pretitle
            except ValueError as e:
                e_file.write(date + url + ',ValueError [PRETITLE]:' + str(e) + '\n')
                print(date + ' PRETITLE ValueError: Length of values does not match length of index')
                continue
            try:
                df['author'] = _author
            except ValueError as e:
                e_file.write(date + url + ',ValueError [AUTHOR]:' + str(e) + '\n')
                print(date + ' AUTHOR ValueError: Length of values does not match length of index')
                continue
            try:
                df['section'] = _section
            except ValueError as e:
                e_file.write(date + url + ',ValueError [SECTION]:' + str(e) + '\n')
                print(date + ' SECTION ValueError: Length of values does not match length of index')
                continue
            try:
                df['tag'] = _tag
            except ValueError as e:
                e_file.write(date + url + ',ValueError [TAG]:' + str(e) + '\n')
                print(date + ' TAG ValueError: Length of values does not match length of index')
                continue
            try:
                df['ref'] = _ref
            except ValueError as e:
                e_file.write(date + url + ',ValueError [REF]:' + str(e) + '\n')
                print(date + ' REF ValueError: Length of values does not match length of index')
                continue
            try:
                df['content'] = _content
            except ValueError as e:
                e_file.write(date + url + ',ValueError [CONTENT]:' + str(e) + '\n')
                print(date + ' CONTENT ValueError: Length of values does not match length of index')
                continue
            try:
                df['publish_time'] = _o_time
            except ValueError as e:
                e_file.write(date + url + ',ValueError [PUBLISH_TIME]:' + str(e) + '\n')
                print(date + ' PUBLISH_TIME ValueError: Length of values does not match length of index')
                continue
            try:
                df['update_time'] = _u_time
            except ValueError as e:
                e_file.write(date + url + ',ValueError [UPDATE_TIME]:' + str(e) + '\n')
                print(date + ' UPDATE_TIME ValueError: Length of values does not match length of index')
                continue
            
            _id.clear()
            _date.clear()
            _title.clear()
            _subtitle.clear()
            _pretitle.clear()
            _author.clear()
            _section.clear()
            _tag.clear()
            _ref.clear()
            _content.clear()
            _o_time.clear()
            _u_time.clear()

        else:
            continue
        
        df.to_csv('./' + str(year) + '/dailyStar-' + date +'.csv', index=False)
        end = time.time()
        dur = end - start
        dur = str(round(dur/60, 2))
        l_file.write(date + ',' + dur + '\n')
        print('=================================================================================\n' + date + '  |  DONE  |  Time Duration: ' + dur + 'mins \n=================================================================================')
        playsound('../click.wav')

l_file.close()
e_file.close()
