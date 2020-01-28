import os
from playsound import playsound

def fileMode(filename):
    if os.path.exists(filename):
        return 'a'
    else:
        return 'w'
    
def checkFile(filename):
    if os.path.exists(filename):
        return
    else:
        l_file.write(date + '\n')
    
days = ['31', '28', '31', '30', '31', '30', '31', '31', '30', '31', '30', '31']

for y in range(2016, 2020):
    year = str(y)
    logFilename = 'log-missingFiles.csv'
    l_file = open(logFilename, fileMode(logFilename))
    if (fileMode(logFilename) == 'w'):
        l_file.write('date\n')
    
    for m in range(1, 13):
        if m < 10:
            months = '0' + str(m)
        else:
            months = str(m)
        for day in range(1, int(days[m - 1]) + 1):
            if day < 10:
                day = '0' + str(day)
            date = str(year) + '-' + str(months) + '-' + str(day)
            fileName = './' + str(year) + '/dailyStar-' + date +'.csv'
            checkFile(fileName)        

    playsound('../click.wav')
        
