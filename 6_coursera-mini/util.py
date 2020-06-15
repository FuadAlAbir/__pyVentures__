import os
import glob

def read_log():
    '''read from the log file'''
    with open('log') as f:
        txt = f.read()
    txt = txt.split('\n')
    return txt

def check(h):
    '''check if all files have been downloaded successfully'''
    lst = glob.glob('/home/fuad/Downloads/*.png')
    lt = [i for i in range(1, h+1)]
    for l in lst:
        a = l[21:-4]
        try:
            a = int(a)
        except ValueError:
            a = '/home/fuad/Downloads/' + a + '.png'
            print('Error Detected:', a, ' Deleting ... ')
            os.remove(a)
        if(a in lt):
            lt.remove(a)
    return lt

def make_pdf(end, book_name):
    '''converts all png to pdf'''
    if(len(check(end)) == 0):
        print(book_name + ': converting all png to pdf ... ')
        cdir = os.getcwd()
        os.system('mkdir tmp')
        os.chdir('tmp')
        os.system('cp /home/fuad/Downloads/*.png .')
        os.system('img2pdf -o ' + book_name + '.pdf $(ls *.png | sort -n)')
        os.system('rm -f *.png')
        os.chdir(cdir)
        #os.system('mkdir books')
        os.system('mv tmp/' + book_name + '.pdf books/')
        os.system('rm -rf tmp')
        print(book_name + '.pdf Created Successfully.')
        os.system('rm -f /home/fuad/Downloads/*.png')
