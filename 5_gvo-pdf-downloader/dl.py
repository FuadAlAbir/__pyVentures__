from selenium import webdriver
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import pyautogui

from util import check, read_log, make_pdf

class GVO:
    def __init__(self, username, password, book_id, lst):
        chromedriver = '/usr/bin/chromedriver'

        self.driver = webdriver.Chrome(chromedriver)
        
        self.driver.get('https://stackoverflow.com/users/signup?ssrc=head&returnurl=%2fusers%2fstory%2fcurrent')
        sleep(3)
        
        self.driver.find_element_by_xpath('//*[@id="openid-buttons"]/button[1]').click()
        self.driver.find_element_by_xpath('//input[@type="email"]').send_keys(username)
        self.driver.find_element_by_xpath('//*[@id="identifierNext"]').click()
        sleep(3)
        
        self.driver.find_element_by_xpath('//input[@type="password"]').send_keys(password)
        self.driver.find_element_by_xpath('//*[@id="passwordNext"]').click()
        sleep(3)
        
        for i in lst:
            tab_url = 'https://drive.google.com/viewerng/img?id=' + book_id + '&authuser=0&page=' + str(i-1) + '&skiphighlight=true&w=800&webp=false'
            self.driver.get(tab_url)
            img = self.driver.find_element_by_xpath('/html/body/img')

            action = ActionChains(self.driver)
            action.move_to_element_with_offset(img, 5, 5)
            action.context_click()
            action.perform()
            
            pyautogui.press('v')
            sleep(2)
            for c in str(i):
                pyautogui.press(c)
            pyautogui.press('enter')
        
        sleep(10)
        self.driver.close()

txt = read_log()

mail = txt[0]
password = txt[1]
book_name = txt[2]
book_id = txt[3]
start = int(txt[4])
end = int(txt[5])
dl_flag= int(txt[6])
check_flag = int(txt[7])
pdf_flag = int(txt[8])

lst = [i for i in range(start, end+1)]

# download: take 1
if(dl_flag == 1):
    print('Downloading ' + book_name + ':' , str(lst[0]), 'to',         str(lst[-1]))
    GVO(mail, password, book_id, lst)   

# checking for error, redownloading
if(check_flag == 1):
    while(True):
        lst = check(end)
        if(len(lst) > 0):
            print('Redownloading:', lst)
            GVO(mail, password, book_id, lst)
        else:
            print(book_name + ': All Images Downloaded Successfully.')
            break

# convering all png to pdf
if(pdf_flag == 1):
    make_pdf(end, book_name)
