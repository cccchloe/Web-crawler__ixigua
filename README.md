# Web-crawler__ixigua
This project aims to crawl videos from www.ixigua.com, a short video publishing website. 
This website uses AJAX web pages and they are dynamic in structure. After trying several methods(urllib, request, beatifulsoup, selenium,etc), I suggest using selenium framework and python for web crawling. The selenium package is used to automate web browser interaction from Python. 
Required knowledge: HTML, CSS, Javascript(need to learn), Python, Selenium package
Web to learn selenium: https://www.bilibili.com/video/av19430527/?p=1
Selenium Offical documentation:https://www.seleniumhq.org/docs/

2018-08-16  version 1
In this version, I have built a foundamental framework which can automatically loading main pages and get video urls shown on main page.
Main Function:
1. Open main page www.ixigua.com and load videos as much as possible(by scroll down to the end of page).
2. Collect all video page url(only those loaded will show address)
3. For each video, open video page, use find_element_by_xpath to get title, publisher, publishing time, video url, comments and user_id.
4. Filter ads.
5. Download videos.(urllib.request.urlretrieve)

Problems to be solved:
1. Each time scroll down to the end of page, the web may not load. Sometimes it has to wait for a few seconds(2-10 seconds). When too many videos are loading, the pages loads even slower. So through this method I can't control the number of videos I want to download. The only thing I can control is the number of scrolls. Each time I run, the page show different number of videos.
2. The pages don't show publishing time and I can't find it in the source code.
3. Some video pages loads too slow, then will return noelementexception and timeoutexception. 
4. Some comments are reply to other comments, which is not displayed in the page. Try to use actionchian to click to show the comments.
