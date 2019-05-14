# -*- coding: utf-8 -*-


"""
Created on Thu May  9 11:25:06 2019

@author: Yu Ho Kwan
"""



from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
import time
import csv
import pandas as pd


def main(data_path,name,password,topic):
    """chrome setting"""
    chrome_options = webdriver.ChromeOptions() # path = 'chromedriver.exe'
    chrome_options.add_argument('headless')    # this will crawl without a gui web app
    #chrome_options.add_experimental_option( "prefs",{'profile.managed_default_content_settings.javascript': 2})
    #prefs = {"profile.managed_default_content_settings.images": 2}
    #chrome_options.add_experimental_option("prefs", prefs)
    browser = webdriver.Chrome(chrome_options=chrome_options)
    
    
    browser.get(r'https://www.zhihu.com/signin?next=%2F')
    account = browser.find_element_by_xpath(r'//*[@id="root"]/div/main/div/div/div/div[2]/div[1]/form/div[1]/div[2]/div[1]/input')
    account.send_keys(name)   # your account name
    password = browser.find_element_by_xpath(r'//*[@id="root"]/div/main/div/div/div/div[2]/div[1]/form/div[2]/div/div[1]/input')
    password.send_keys(password)     # your password
    login = browser.find_element_by_xpath('//*[@id="root"]/div/main/div/div/div/div[2]/div[1]/form/button').click()
    
    serach = topic
    browser.get(r'https://www.zhihu.com/search?type=content&q=%s' %serach)
    
    while True:
        print('scrolling question')
        last_height = browser.execute_script("return document.body.scrollHeight")
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        browser.execute_script("window.scrollBy(0,500)")
        browser.execute_script("window.scrollBy(0,-500)")
        browser.execute_script("window.scrollBy(0,500)")
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
        time.sleep(3)#4
        last_height2 = browser.execute_script("return document.body.scrollHeight")
        if last_height == last_height2:
            break
    
    questions_list = []
    empty_text = 0
    index = 0
    while True:
       try:
           index +=1
           print('getting question',str(index))
           question_text = browser.find_element_by_xpath('//*[@id="SearchMain"]/div/div/div/div/div[%s]/div/div/h2/div/a/span'%str(index))
           questions_list.append(question_text.text)
       except NoSuchElementException:
           empty_text += 1
           index +=1
       if empty_text>50:
           break
    print('length of questions_list',len(questions_list))
    """check ans for each question"""
    question_answer_list = []
    missed_url = []
    empty_text = 0
    for i in enumerate(questions_list):
        index = 0
        browser.get(r'https://www.zhihu.com/search?type=content&q=%s' %i[1])
        try:
           question_href = browser.find_element_by_xpath('//*[@id="SearchMain"]/div/div/div/div/div[1]/div/div/h2/div/a').get_attribute('href')
           print(question_href)
           browser.get(question_href.split('answer')[0])   # https://www.zhihu.com/question/20946770
           time.sleep(3)
        except NoSuchElementException:
            missed_url.append(r'https://www.zhihu.com/search?type=content&q=%s' %i[1])
            pass
        
    
           
        while True:
            print('scrolling answer at question_answer_list',i[0])
            start_time = time.time()
            last_height = browser.execute_script("return document.body.scrollHeight")
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            #time.sleep(0.2)#4
            last_height2 = browser.execute_script("return document.body.scrollHeight")
            #browser.execute_script("window.scrollTo(0, %s);" %str(int(last_height2)+10))
            print('last_height : last_height2',last_height,last_height2)
            browser.execute_script("window.scrollBy(0,100)")
            browser.execute_script("window.scrollBy(0,-100)")
            time.sleep(3)#4
            last_height2 = browser.execute_script("return document.body.scrollHeight")
            end_time = time.time()
            if last_height == last_height2:
                break
            #if end_time-start_time>10:
                #break
                
        
        empty_text = 0
        while True:
            try:
                index +=1
                print('getting answer for question_answer_list', i[0])  # ,str(index)
                question_answer_list.append((i,
                                             browser.find_element_by_xpath('//*[@id="QuestionAnswers-answers"]/div/div/div/div[2]/div/div[%s]/div/div[2]'%str(index)).text,
                                             browser.find_element_by_xpath('//*[@id="QuestionAnswers-answers"]/div/div/div/div[2]/div/div[%s]/div/div[2]/div[3]/span/button[1]'%str(index)).text,
                                             browser.find_element_by_xpath('//*[@id="QuestionAnswers-answers"]/div/div/div/div[2]/div/div[%s]/div/div[2]/div[3]/button[1]'%str(index)).text))
                # question,text ,like no, commitment no

                print('length question_answer_list',len(question_answer_list))
            except NoSuchElementException:
                empty_text += 1
            if empty_text>100:
               empty_text = 0
               break
        print('length question_answer_list',len(question_answer_list))
        
        csv_file = open(data_path+'\%s.csv'%str(i[1].replace('?','').replace('!','').replace('?','').replace("\\",'').replace("//",'').replace('|','').replace('？','')),'w',encoding='gb18030',errors = 'ignore',newline='')
        csv_write = csv.writer(csv_file,dialect='excel')

        csv_write.writerow(['question','answer','like number','commitment number'])
        for j in question_answer_list:
            small_list = [j[0][1],j[1],j[2],j[3]]
            csv_write.writerow(small_list)

        question_answer_list=[]
# =============================================================================
# 
if __name__ == '__main__':
    data_path = 'data_path'   # e:  r'C://data
    name = 'account name'     # you should register one of it
    password = 'password'
    topic = 'interested topic话题'  # eg 香港
    main(data_path,name,password,topic)   








