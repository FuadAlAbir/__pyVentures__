from selenium import webdriver
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import pyautogui

class GVO:
    def __init__(self, username, password, book_id, start, end):
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
        
        for i in range(start, end+1):
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



# parameters

mail = 'YOUR GMAIL ADDRESS'
password = 'GMAIL PASSWORD'
book_id = 'BOOK_ID'
start = 1   # range: start to end, inclusive
end = 100

dl = GVO(mail, password, book_id, start, end)
 
