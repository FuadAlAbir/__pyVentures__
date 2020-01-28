import requests
import socket
import pandas as pd
from bs4 import BeautifulSoup
import os
import sys
import re
import json
from playsound import playsound
from datetime import datetime
import time

def is_connected():
    try:
        socket.create_connection(('www.google.com', 80))
        return True
    except OSError as e:
        e_file.write(year + ',' + datetime.now().strftime('%H:%M:%S') + ',www.google.com,OSError: ' + str(e) + '\n')
        return False
    except socket.gaierror as e:
        e_file.write(year + ',' + datetime.now().strftime('%H:%M:%S') + ',' + url + ',socket.gaierror: ' + str(e) + '\n')
        return False
    return False

def formatStr(string):
    return " ".join(string.replace(',', '.').strip().split())


connection_message_positive = 'Connention Established...'
connection_message_negative = 'Connention Checking...'
pause_time = 3

def get_resource(url = 'www.google.com'):
    while True:
        if(is_connected()):
            try:
                return requests.get(url)
            except OSError as e:
                e_file.write(year + ',' + datetime.now().strftime('%H:%M:%S') + ',' + url + ',OSError: ' + str(e) + '\n')
                pass
            except socket.gaierror as e:
                e_file.write(year + ',' + datetime.now().strftime('%H:%M:%S') + ',' + url + ',socket.gaierror: ' + str(e) + '\n')
                pass
        else:
            time.sleep(pause_time)

def fileMode(filename):
    if os.path.exists(filename):
        return 'a'
    else:
        return 'w'
    
def checkPathExists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

exceptionFilename = './exceptions/exceptions.csv'
e_file = open(exceptionFilename, fileMode(exceptionFilename))
header = 'year,time,url,message\n'
if(fileMode(exceptionFilename) == 'w'):
    e_file.write(header)



# terminal input
year = sys.argv[1]
l = int(sys.argv[2])

# count # of files in a folder
DIR = './splitted/' + year + '-splitted/'

#h = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))]) + 1
h = int(sys.argv[3]) + 1

checkPathExists('./comments/' + year)
checkPathExists('./contents/' + year)

for i in range(l, h):
    start = time.time()

    df = pd.read_csv('./splitted/' + year + '-splitted/prothomAlo-' + year + '-' + str(i) + '.csv')
    
    _tag = []
    _content = []
    _articleId = []
    
    _contentID = []
    _commentID = []
    _parent = []
    _label_depth = []
    _commenter_name = []
    _comment = []
    _create_time = []
    _comment_status = []
    _like_count = []
    _dislike_count = []
    _device = []

    for u in range(len(df['ref'])):
        url = df['ref'][u]
        
        while True:
            if(is_connected()):
                resource = get_resource(url)
                break
            else:
                time.sleep(pause_time)
                continue
            
        soup = BeautifulSoup(resource.text, 'lxml')

        tags = soup.find('div', {'class':'topic_list'})
        tag = ''
        if tags is not None:
            tags = tags.findAll('a', {'':''})
            for t in range(len(tags)):
                if tag == '':
                    tag = tags[t].text
                else:
                    tag = tag + '|' + tags[t].text
        
        _tag.append(tag)
        

        content_tag = soup.find('div', {'itemprop':'articleBody'})
        content = ''
        if content_tag is not None:
            content_head = content_tag.find('div', {'class':'palo_web_news_div'})
            if content_head is not None:
                content = content + content_head.text + ' '
            content_all = content_tag.findAll('p', {'':''})
            for c in range(len(content_all)):
                content = content + content_all[c].text + ' '
        _content.append(formatStr(content))

        
        comment_url = 'https://www.prothomalo.com/api/comments/get_comments_json/?content_id={}'
        article_id = re.findall(r'article/(\d+)', url)[0]
        _articleId.append(article_id)
    
        
        comment_data = requests.get(comment_url.format(article_id)).json()

        if(len(comment_data)):
            
            keys = list(comment_data.keys())
            
            for c in range(len(keys)):
                _contentID.append(formatStr(comment_data[keys[c]]['content_id']))
                _commentID.append(formatStr(comment_data[keys[c]]['comment_id']))
                _parent.append(formatStr(comment_data[keys[c]]['parent']))
                _label_depth.append(formatStr(comment_data[keys[c]]['label_depth']))
                if comment_data[keys[c]]['commenter_name'] is not None:
                    _commenter_name.append(formatStr(comment_data[keys[c]]['commenter_name']))
                else:
                    _commenter_name.append('')
                _comment.append(formatStr(comment_data[keys[c]]['comment']))
                _create_time.append(formatStr(comment_data[keys[c]]['create_time']))
                _comment_status.append(formatStr(comment_data[keys[c]]['comment_status']))
                _like_count.append(formatStr(comment_data[keys[c]]['like_count']))
                _dislike_count.append(formatStr(comment_data[keys[c]]['dislike_count']))
                _device.append(formatStr(comment_data[keys[c]]['device']))
        
        print(str(i) + '/' + str(h - 1) + ' ' + df['date'][u] + datetime.now().strftime(' %H:%M:%S : ') + df['title'][u])       
        
    _commentDF = pd.DataFrame()
    _commentDF['content_id'] = _contentID
    _commentDF['comment_id'] = _commentID
    _commentDF['parent'] = _parent
    _commentDF['label_depth'] = _label_depth
    _commentDF['commenter_name'] = _commenter_name
    _commentDF['comment'] = _comment
    _commentDF['create_time'] = _create_time
    _commentDF['comment_status'] = _comment_status
    _commentDF['like_count'] = _like_count
    _commentDF['dislike_count'] = _dislike_count
    _commentDF['device'] = _device
    _commentDF.to_csv('./comments/' + year + '/prothomAlo-' + year + '-' + str(i) + '-comments.csv', index=False)
                
    df['tags'] = _tag
    df['content'] = _content
    df['article_id'] = _articleId
    df.to_csv('./contents/' + year + '/prothomAlo-' + year + '-' + str(i) + '-woComment.csv', index=False)
    end = time.time()
    dur = end - start
    dur = str(round(dur/60, 2))
    print('=================================================================================\n\t' + str(i) + '/' + str(h - 1) + ' : ' + year + '\t|  DONE  |\tTime Duration: ' + dur + 'mins \n=================================================================================')
    
    playsound('click.wav')


# print(json.dumps(comment_data, indent=4))
e_file.close()
playsound('click.wav')
playsound('click.wav')
playsound('click.wav')

# 2013 : 2019
# split - combine - reorder : per year
# combine : all years
# মন্তব্য has a extra space
