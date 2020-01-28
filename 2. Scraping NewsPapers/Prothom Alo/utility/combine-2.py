import pandas as pd
import glob
import os

def checkPathExists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
        

        
for v in range(1, 4):
    

    for i in range(2013, 2020):
        path = '/media/fuad/D U S T   B I N/P R O J E C T S/dataScienceProjects/project_news_dataset/dataset_prothomAlo/code/comments/' + str(i) + '/' + str(v) + '/'
        
        desPath = '/media/fuad/D U S T   B I N/P R O J E C T S/dataScienceProjects/project_news_dataset/finalCSV-ProthomAlo/comment/'
        checkPathExists(desPath)
   
        
        if os.path.exists(path):
            csvfiles = sorted(glob.glob(path + '*.csv'))

            df = pd.DataFrame()
            for files in csvfiles:
                df = df.append(pd.read_csv(files))
            desPath = desPath + str(i)
            checkPathExists(desPath)
            df.to_csv(desPath + '/prothomAlo-' + str(i) + '-comment-' + str(v) + '.csv', index = False, encoding='utf-8-sig')
