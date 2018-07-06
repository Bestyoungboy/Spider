"""
-* coding: utf-8 *- 
@Author : ice cream 
@Time : 2018/7/6 15:50
@File : qzone.py
@Software: PyCharm
"""
from selenium import webdriver
from time import sleep

# 使用chrome headless 代替phantomJS


options = webdriver.ChromeOptions()
options.add_argument('headless')

# driver = webdriver.Chrome(chrome_options=options)
driver = webdriver.Chrome(r'E:\package\chromedriver.exe')

driver.get('https://i.qq.com/?rd=1')
# driver.implicitly_wait(10)
# print(driver.page_source)

while True:
    try:
        # loginLable = driver.find_element_by_xpath('//*[@id="switcher_plogin"]')
        iframe = driver.find_element_by_id('login_frame')

        print(iframe.get_attribute('src'))
        print('-----------')

        driver.get(iframe.get_attribute('src'))
        loginLable = driver.find_element_by_xpath('//*[@id="switcher_plogin"]')
        break
    except:
        print('retry ....')
        sleep(0.1)

loginLable.click()
driver.find_element_by_id('u').send_keys('406069993')

driver.find_element_by_id('p').send_keys('clannad8.')

driver.find_element_by_xpath('//input[@class="btn"]').click()

driver.save_screenshot('qzone.png')

driver.quit()
