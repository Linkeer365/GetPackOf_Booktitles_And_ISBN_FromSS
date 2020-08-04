from getIIDFromISBN import get_iids_from_isbn
from getSSfromIID import get_ss_list_from_iid_list

import sqlite3
import os
from bs4 import BeautifulSoup
import re

import requests
from lxml import etree

from time import sleep

headers={
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"
}

history_dir=r"C:\Users\linsi\AppData\Local\CentBrowser\User Data\Default"
history_path=os.path.join(history_dir,"History")


def get_douban_urls(max_cnt):
# 数据库操作，得到历史数据中所有的网址
    c=sqlite3.connect(history_path)
    cursor=c.cursor()
    pattern_str="https://book.douban.com/subject/%/"
    select_statement="SELECT DISTINCT urls.url FROM urls,visits WHERE urls.id=visits.url AND urls.url LIKE '{}' AND urls.url NOT LIKE '%comments/' ORDER BY last_visit_time DESC".format(pattern_str)
    # select_statement="SELECT urls.url FROM urls,visits WHERE urls.id=visits.url AND urls.url LIKE '{}' AND datetime('now','-1 day','last_visit_time')>1".format(pattern_str)
    print(select_statement)
    cursor.execute(select_statement)
    results=cursor.fetchall()
    print("Re",results)
    urls=[]
    for each in results:
        url=each[0]
        if not url in urls:
            urls.append(url)

    # for url in urls:
    #     print(url)
    if max_cnt==-1:
        return urls
    return urls[0:max_cnt]
    # print(url)

def get_fields_from_pattern_xpath(some_url,some_pattern):
    url_text=requests.get(some_url,headers=headers).text
    html=etree.HTML(url_text)
    fields=html.xpath(some_pattern)
    if bool(fields)==0:
        print("Fields not found!")
    return fields[0]

def get_fields_from_str(some_str,some_re_pattern):
    fields=re.findall(some_re_pattern,some_str,re.S)
    if bool(fields)==0:
        print("Fields not found!")
    return fields[0]

def getPack_title_isbn_ssSet(douban_url):
    pattern_introPack="//script[@type='application/ld+json']//text()"
    introPack = get_fields_from_pattern_xpath(douban_url, pattern_introPack)
    re_pattern_title = "\"name\" : \"(.*?)\","
    re_pattern_isbn = "\"isbn\" : \"(.*?)\","

    # introPack=str(introPack)

    title = get_fields_from_str(introPack, re_pattern_title)
    isbn = get_fields_from_str(introPack, re_pattern_isbn)

    iids = get_iids_from_isbn(isbn)
    ss_list = get_ss_list_from_iid_list(iids)

    print("\n& Start &\n")
    print("Title:",title)
    print("Isbn:",isbn)
    print("IIDs:",iids)
    print("ssList:",ss_list)
    print("\n& End &\n")

    pack_title_isbn_ssSet = (title, isbn, set(ss_list))
    return pack_title_isbn_ssSet

def main():
    douban_urls=get_douban_urls(max_cnt=10)
    pattern_introPack="//script[@type='application/ld+json']//text()"

    packs=[]

    for each_idx in range(len(douban_urls)):
        douban_url=douban_urls[each_idx]
        pack=getPack_title_isbn_ssSet(douban_url)
        packs.append(pack)

        # print("\n& Start &\n")
        # print("Title:",title)
        # print("Isbn:",isbn)
        # print("IIDs:",iids)
        # print("ssList:",ss_list)
        # print("\n& End &\n")
        # sleep(3)


if __name__ == '__main__':
    main()

# def tt():
#     get_douban_urls()
# tt()

