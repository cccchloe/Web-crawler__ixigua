#!/usr/bin/python
# coding: utf-8

# In[384]:


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

import pandas as pd
import time
import urllib.request

# In[322]:


url='https://www.ixigua.com/'


# # Make direct calls to browser
# eg.Chrome


chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
driver = webdriver.Chrome(chrome_options=chrome_options)


# eg.Linux Centos7


chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
driver = webdriver.Chrome(executable_path='/opt/chromedriver',chrome_options=chrome_options)



driver.get(url)
driver.implicitly_wait(10)
html_source=driver.page_source
print(driver.title)

page_url=[]
video_title=[]
publisher=[]
video=[]
content=[]
comment=[]
com_user=[]
com_date=[]


# # Scroll up and down the pages and dynamically loading new videos
# js="var q=document.documentElement.scrollTop=1000000"
# driver.execute_script(js)
# js="var q=document.documentElement.scrollTop=0"
# driver.execute_script(js)


# 方法一：使用快速不断上下滚动页面来更新页面
# 问题：不是每一次拉到页面底部就加载，需要等一会儿，加载时间不确定

def scrolldown(num_of_runs):
    for i in range(num_of_runs): 
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            driver.execute_script("window.scrollTo(0, 0);")
            break


def count_video():
    page_url_pre=driver.find_elements_by_xpath('//div[@class="title-box"]/a[@href]')
    i=0
    for each in video_url_pre:
        page_url.append(each.get_attribute('href'))
        i+=1
    print ( 'number of videos %d'%i)



i=[1000]              # try this for 5 times, about to finish in 20 mins, loading 700 videos.
start_time=time.localtime(time.time()).tm_min
for num in i:
    scrolldown(num)
    count_video()
end_time=time.localtime(time.time()).tm_min
print(str(start_time-end_time))

page_info={'page_url':page_url}
page_list=pd.DataFrame(page_info)
page_list.to_csv('video_list.csv',encoding='utf_8_sig') 



# 方法二：通过模拟滚轮缓慢小步向下滚动来加载页面,移动速度可控，加载匀速
# 问题： 不能确定加载的数据的数量,有时候会卡住

# i=0
# while i<1000:
#     driver.execute_script("window.scrollBy(0, 1);")
#     time.sleep(0.5)
#     i+=1


start_time=time.localtime(time.time()).tm_min

i=0

while i < len(page_url):
    url=page_url[i]
    a=re.search('ixigua',url)
	if a==None:
    	print('This page is invalid.URL:%s'%url)
    	i=i+1
    	continue
    
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.implicitly_wait(100)
    driver.get(url)
    
    page_title=driver.title            #check if the page is available
    if page_title=='西瓜视频 - 原头条视频, 唯一官方网站':
        print('This video does not exist any more.')
    else:
    
        # find the title element of video
        v_t=driver.find_element_by_xpath('//h2[@class="title"]').text
        video_title.append(v_t)
        print('video %d:%s'%(i,v_t))
        
        #find the publisher element
        p=driver.find_element_by_xpath('//a[@class="media-user"]').text
        publisher.append(p)
    
        #get the url of each video for downloading
        v_url=driver.find_element_by_xpath('//video[@src]').get_attribute('src')
        video.append(v_url)
        urllib.request.urlretrieve(v_url,'d:\ixigua\%s.mp4'%i)     #download video
    
        #get the content of each video
        #content.append(driver.find_element_by_xpath('//div[@class="abstract-wrap"]/div[@class="text"]').text)

        num_of_com=driver.find_element_by_css_selector('#comment > div.c-header > em').text.replace(',','')
    
        # check if comment exists
        if int(num_of_com)==0:
            print('This video has %s comments:'%num_of_com)

        else:  
            print('This video has %s comments:'%num_of_com) 

            # check if all comments are visible, if not, click to load more comments
            elem=WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH,'//*[@id="comment"]/a')))
            while elem.text=='查看更多评论':
                try:
                    elem.click()
                    elem=WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH,'//*[@id="comment"]/a')))
                except:
                    break  

            comment_pre=driver.find_elements_by_xpath('//div[@class="c-content"]/p')         #get text of comments of each video
            com_user_pre=driver.find_elements_by_xpath('//div[@class="c-content"]/div[@class="c-user-info"]/a')    #get user info
            com_date_pre=driver.find_elements_by_xpath('//div[@class="c-content"]/div[@class="c-user-info"]/span')  #get date info
            for each in comment_pre:
                comment.append(each.text)
            for each in com_user_pre:
                com_user.append(each.text)
            for each in com_date_pre:
                com_date.append(each.text)

         

    driver.quit()
    i=i+1
    each_end_time=time.localtime(time.time()).tm_min
    print(str(each_end_time-start_time))


end_time=time.localtime(time.time()).tm_min
print(str(end_time-start_time))

video_info={'Title':video_title,
            'Publisher':publisher,
            'URL':video
     }
video_list=pd.DataFrame(video_info)

comment_info={'Comment':comment,
             'User':com_user,
             'Date':com_date
             }
comment_list=pd.DataFrame(comment_info)

video_list.to_csv('video_list.csv',encoding='utf_8_sig') 

comment_list.to_csv('comment_list.csv',encoding='utf_8_sig')
