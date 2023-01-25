from selenium import webdriver
import time
from openpyxl import Workbook
import pandas as pd
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from list import chamions

import warnings
warnings.filterwarnings('ignore')

wb = Workbook(write_only=True)
ws = wb.create_sheet()

driver = webdriver.Chrome("chromedriver.exe")
driver.get("https://www.youtube.com/watch?v=n-nCotAcjms")
driver.implicitly_wait(3)

time.sleep(1.5)

driver.execute_script("window.scrollTo(0, 800)")
time.sleep(3)

last_height = driver.execute_script("return document.documentElement.scrollHeight")

while True:
    driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
    time.sleep(1.5)

    new_height = driver.execute_script("return document.documentElement.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

time.sleep(1.5)

buttons = driver.find_elements_by_css_selector("#more-replies > a")

time.sleep(1.5)

for button in buttons:
    button.send_keys(Keys.ENTER)
    time.sleep(1.5)
    button.click()

html_source = driver.page_source
soup = BeautifulSoup(html_source, 'html.parser')

# id_list = soup.select("div#header-author > h3 > #author-text > span")
comment_list = soup.select("yt-formatted-string#content-text")

# id_final = []
comment_final = []
append_list = chamions

for i in range(len(comment_list)):
    temp_comment = comment_list[i].text
    temp_comment = temp_comment.replace('\n', '')
    temp_comment = temp_comment.replace('\t', '')
    temp_comment = temp_comment.replace('    ', '')
    for i in append_list:
        if i in temp_comment:
            comment_final.append(temp_comment) # 댓글 내용

pd_data = {"댓글 내용" : comment_final}
youtube_pd = pd.DataFrame(pd_data)

youtube_pd.to_csv('result.csv')