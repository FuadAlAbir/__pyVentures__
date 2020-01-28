import pandas as pd
import glob
import os

def checkPathExists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

source = '/media/fuad/D U S T   B I N/P R O J E C T S/dataScienceProjects/project_news_dataset/finalCSV-ProthomAlo/content/'

csvfiles = sorted(glob.glob(source + '*.csv'))

df = pd.DataFrame()
for files in csvfiles:
    df = df.append(pd.read_csv(files))

df.to_csv(source + 'prothomAlo-all_contents_2013-2019.csv', index = False, encoding='utf-8-sig')
