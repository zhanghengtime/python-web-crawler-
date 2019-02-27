# CrowTaobaoPrice.py
import requests
from bs4 import BeautifulSoup


def getHTMLText(url):
    try:
        kv = {'user-agent':'Mozilla/5.0'}
        r = requests.get(url, timeout=30, headers=kv)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        demo = r.text
        return demo
    except:
        return ""


def parsePage(ilt, demo):
    try:
        price = []
        title = []
        soup = BeautifulSoup(demo, 'lxml')
        for line in soup.find_all('p', "price"):
            price.append(line.span.string)
        for line in soup.find_all('p', "name"):
            s = line.a.get('title')
            titles = s.split(' ')
            if len(titles[1]) <= 5:
                title.append(titles[1]+' '+titles[2])
                if len(titles[2]) <=2:
                    title.append(titles[1] + ' ' + titles[2]+ ' ' + titles[3])
            else:
                title.append(titles[1])
        for i in range(len(title)):
            ilt.append([price[i], title[i]])
    except:
        print("")


def printGoodsList(ilt):
    tplt = "{:4}\t{:8}\t{:16}"
    print(tplt.format("  序号", " 价格", "     商品名称    "))
    count = 0
    for g in ilt:
        count = count + 1
        print(tplt.format(count, g[0], g[1]))


def main():
    goods = input('Please in put a goods: ')
    depth = 3
    start_url = 'http://search.dangdang.com/?key=' + goods
    infoList = []
    for i in range(depth):
        try:
            url = start_url + '&page_index=' + str(i+1)
            html = getHTMLText(url)
            parsePage(infoList, html)
        except:
            continue
    printGoodsList(infoList)

if __name__ == '__main__':
    main()
