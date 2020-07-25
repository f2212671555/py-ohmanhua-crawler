# -*- coding: utf-8 -*-
import urllib.request as req
import urllib.parse as parse
import bs4
import crawler.beans.comic as c
import crawler.beans.chapter as ch

base_url = "https://www.ohmanhua.com/"
comic_img_base_url = "https://img.ohmanhua.com/comic"

def crawl_search_comic(searchString):
    encodeStr = parse.quote(searchString)
    url = base_url + "search?searchString=" + encodeStr
    request = req.Request(url,headers={
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"
    })

    with req.urlopen(request) as response:
        data = response.read().decode("utf-8")
    
    soup = bs4.BeautifulSoup(data,"html.parser")

    dls = soup.findAll("dl",{"class":"fed-deta-info fed-deta-padding fed-line-top fed-margin fed-part-rows fed-part-over"})
    comics = []
    for dl in dls:
        dt_a = dl.select_one("dt a")
        comic_img_url = dt_a["data-original"]
        # print(comic_img_url)
        dd_a = dl.select_one("dd a")
        comic_url = dd_a["href"]
        # print(comic_url)
        comic_name = dd_a.text
        # print(comic_name)
        comics.append(c.Comic(comic_name,comic_url,comic_img_url))
        # break                         # ---ttttteeeessstttt----
    return comics

def crawl_one_comic(href):
    url = base_url + href
    request = req.Request(url,headers={
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"
    })

    with req.urlopen(request) as response:
        data = response.read().decode("utf-8")

    soup = bs4.BeautifulSoup(data,"html.parser")

    lis = soup.findAll("li",{"class":"fed-padding fed-col-xs6 fed-col-md3 fed-col-lg3"})
    
    chapters = []
    for li in lis:
        a = li.select_one("a")
        title = a["title"]
        # print(title)
        base_img_url = comic_img_base_url + href + title
        chapters.append(ch.Chapter(title,href,base_img_url))
        # break                         # ---ttttteeeessstttt----
    return c.Comic("",href,"","",chapters)