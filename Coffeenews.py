#!/usr/bin/env python
# coding: utf-8

# In[37]:


get_ipython().system('pip install bs4')


# In[38]:


get_ipython().system('pip install requests')


# In[66]:


get_ipython().system('pip install pandas')


# In[113]:


get_ipython().system('pip install openpyxl')


# In[115]:


import pandas as pd
import bs4
import requests
import openpyxl


# In[116]:


page = 1
topics_list = []
news_list =[]
while page <= 29:
    data = requests.get('https://www.bbc.co.uk/search?q=coffee&page=' + str(page))
    soup = bs4.BeautifulSoup(data.text)
    for n in soup.find_all('div' ,{'class' : 'ssrcss-dirbxo-PromoSwitchLayoutAtBreakpoints e3z3r3u0'}):
        topics_list.append(n.find('div',{'class' : 'ssrcss-tq7xfh-PromoContent e1f5wbog7'}).find('span').text)
        news_list.append(n.find('p',{'class' : 'ssrcss-1q0x1qg-Paragraph eq5iqo00'}).text)
    print('Complete page number: ',page)
    page += 1
    
table = pd.DataFrame([topics_list, news_list]).transpose()
table.columns = ['topics', 'news']
table.set_index('topics')


# In[119]:


table = table.set_index('topics')


# In[121]:


table.to_excel('All News.xlsx',engine='openpyxl')


# In[ ]:





# In[ ]:




