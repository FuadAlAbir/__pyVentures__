#!/usr/bin/python

import os
import sys
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq

channel = sys.argv[1]
query = sys.argv[2]
output_dir = '/media/fuad/D U S T   B I N/_downloads/' + query + '-' + channel + '/%(title)s.%(ext)s'

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

url = 'https://www.youtube.com/channel/' + channel + '/search?query=' + query
u = uReq(url)
html = u.read()
u.close()

soup = soup(html, 'html.parser')
links = []
for link in soup.findAll('a'):
    link = link.get('href')
    if link.find("watch") == 1:
        link = 'https://www.youtube.com/' + link
        links.append(link)
links = list(set(links))

for link in links:
    os.system('youtube-dl ' + link + ' --no-warnings -o ' + '"' + output_dir + '"')
