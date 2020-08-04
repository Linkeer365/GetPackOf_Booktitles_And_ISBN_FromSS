import requests
from lxml import etree

headers={
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"
}

url_feed_isbn="http://book.ucdrs.superlib.net/search?sw={}"
def is_isbn(some_str):
    return len(some_str)==13

def get_iid_from_link(some_iid_link):
    iid=some_iid_link.rsplit("?iid=",maxsplit=1)[1]
    print("IID is:\t{}".format(iid))
    return iid


def get_iids_from_isbn(some_isbn):
    assert is_isbn(some_isbn)
    url_with_isbn=url_feed_isbn.format(some_isbn)
    url_text=requests.get(url_with_isbn,headers=headers).text
    html=etree.HTML(url_text)

    pattern_NotFound="//div[@style='font-size:13px; line-height:24px;']"
    pattern_iidLink="//img[@height=110]//@src"
    fields_NotFound=html.xpath(pattern_NotFound)
    if bool(fields_NotFound)!=0:
        print("Not Found!")
        return "NIL"

    fields_iidLinks=html.xpath(pattern_iidLink)

    iids=[get_iid_from_link(iidLink) for iidLink in fields_iidLinks]

    return iids

def main():
    broken_isbn="9787301167045"
    multi_isbn="9787509749296"
    onlyone_isbn="9787208060753"

    print("Only One",get_iids_from_isbn(onlyone_isbn))
    print("Broken",get_iids_from_isbn(broken_isbn))
    print("Multi",get_iids_from_isbn(multi_isbn))

if __name__ == '__main__':
    main()

