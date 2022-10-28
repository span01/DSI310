#!/usr/bin/env python
# coding: utf-8

# In[18]:


get_ipython().system('pip install selenium')
get_ipython().system('pip install bs4')


# In[19]:


import pandas as pd
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
import bs4
import time
import re


# In[17]:


options = Options()
options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
driver = webdriver.Firefox(executable_path=r'C:\Users\Acer\scrapy_shopee_test\geckodriver.exe', options=options)
driver.get('https://shopee.co.th/')
time.sleep(5)
thai_button = driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div/div[3]/div[1]/button')
thai_button.click()
time.sleep(3)
close_adver = driver.execute_script('return document.querySelector("shopee-banner-popup-stateful").shadowRoot.querySelector("div.shopee-popup__close-btn")')
close_adver.click()
time.sleep(3)
search = driver.find_element_by_xpath('/html/body/div[1]/div/header/div[2]/div/div[1]/div[1]/div/form/input')
search.send_keys('กาแฟผลไม้') #ใส่เนื้อหาที่ต้องการที่จะ Scrape จากเว็บ Shopee
search.send_keys(Keys.ENTER)

driver.execute_script("document.body.style.MozTransform='scale(0.1)';")
driver.execute_script('document.body.style.MozTransformOrigin = "0 0";')

records=[]
for i in range(3):
    data = driver.page_source
    soup = bs4.BeautifulSoup(data)
    All_product=soup.select(".row>div")
    for Product in All_product:
        name = Product.select_one("div.col-xs-2-4 > a:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1)").text.strip()
        try:
            p = Product.select_one("div.col-xs-2-4 > a:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > span:nth-child(2)").text.strip()
            if p == '':
                print(1/0)
        except:
            p = Product.select_one("div.col-xs-2-4 > a:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1)").text.strip()
        p = p.replace(",", "").replace("฿", "").replace(" ", "")
        try:
            start_price = float(p)
        except:
            price = p.rpartition('-')[0]
            start_price = float(price)

        sales = Product.select_one("div.col-xs-2-4 > a:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(3) > div:nth-child(2)").text.strip().replace("พัน","000").replace("ล้าน","000000")
        try:
            sales = float(re.sub('\D','',sales))
        except:
            sales = 0
        province = Product.select_one("div.col-xs-2-4 > a:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(2) > div:nth-child(4)").text.strip()
        #print(name, p)
        records.append([name, start_price,sales,province])
        
    time.sleep(5)
    next_button = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/div/div[2]/div[2]/div[3]/div/button[8]')
    next_button.click()
    time.sleep(5)
    
df = pd.DataFrame(records, columns=['Product','price','sales','province']) # ใส้ชื่อ Columns ทั้งหมด
df


# In[ ]:




