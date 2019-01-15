# coding=utf-8
import requests
from bs4 import Tag
from bs4 import BeautifulSoup


def getHtml(url):
    page = requests.get(url)
    html = page.text
    return html


def getText(html):
    get_text = Tag.get_text
    soup = BeautifulSoup(html, 'html.parser')

    author_info = soup.find_all('div', class_='atl-info')
    listauthor = [x.get_text() for x in author_info]

    list_info = soup.find_all('div', class_='bbs-content')
    listtext = [x.get_text() for x in list_info]

    global i
    if i > 1:
        listtext = [""] + listtext
    file=open('./china.txt','a')
    for x in range(len(listauthor)):
        if "楼主" in listauthor[x]:
            print(listtext[x].strip())
            file.write(listtext[x].strip())
            file.write(listtext[x].strip())
    file.close()



if __name__ == '__main__':
    for i in range(1, 3):
        url = ("http://bbs.tianya.cn/post-worldlook-980641-%s.shtml" % str(i))
        html = getHtml(url)
        getText(html)