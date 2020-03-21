import os

with open('temp.txt') as f:
    links = f.read()
    links = list(links.split('\n'))
output_dir = links[0]
links = links[1:-1]

for link in links:
    os.system('youtube-dl ' + link + ' --no-warnings -o ' + '"' + output_dir + '"')
