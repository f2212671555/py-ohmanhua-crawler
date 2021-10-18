# -*- coding: utf-8 -*-
import json
import urllib.request as req
import urllib.parse as parse
import bs4
import crawler.beans.search as s
import crawler.beans.comic as c
import crawler.beans.chapter as ch

comic_api_url = "https://comic-api-server.herokuapp.com/searchString/"
comic_chapter_api_url = "https://comic-api-server.herokuapp.com/comic/chapter/"
base_search_url_dark = "https://nhentai.net/search/?q="
base_g_url_dark = "https://nhentai.net/g/"
comic_img_base_url_dark = "https://t.nhentai.net/galleries"


def crawl_search_comic(searchString, page, version):
    encodeStr = parse.quote(searchString)

    # --version----
    if version == "1":
        url = base_search_url_dark + encodeStr + "&page=" + page
    else:
        # url = base_search_url + encodeStr + "&page=" + page
        url = comic_api_url + encodeStr + "&page=" + page
    # --version----

    request = req.Request(url, headers={
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36"
    })

    with req.urlopen(request) as response:
        data = response.read().decode("utf-8")

    page_num = 1
    comics = []
    # --version----
    if version == "1":

        soup = bs4.BeautifulSoup(data, "html.parser")

        end_page = 1
        a_s = soup.findAll(
            "a", {"class": "last"})
        for a in a_s:
            end_page = int(a["href"].split("page=",1)[1])
            # print(end_page)
        page_num = end_page

        divs = soup.findAll("div", {"class": "gallery"})
        for div in divs:
            div_a = div.select_one("div a")
            div_a_img = div_a.select_one("img")
            comic_img_url = div_a_img["data-src"]
            # print(comic_img_url)
            comic_url = div_a["href"].split("g", 1)[1]
            # print(comic_url)
            div_a_img = div_a.select_one("div.caption")
            comic_name = div_a.text
            # print(comic_name)
            comics.append(c.Comic(comic_name, comic_url, comic_img_url))
            # break                         # ---ttttteeeessstttt----
    else:
        # api version
        data = json.loads(data)
        for d in data:
            comic_name = d['name']
            comic_url = d['link']
            comic_img_url = d['imgUrl']
            comics.append(c.Comic(comic_name, comic_url, comic_img_url))
        # crawler version is gg
    # --version----

    if len(comics) == 0:
        page_num = 0
    return s.Search(searchString, page_num, comics)

def crawl_one_comic(href, version):

    # --version----
    if version == "1":
        url = base_g_url_dark + href
    else:
        url = comic_chapter_api_url
    # --version----

    chapters = []
    # --version----
    if version == "1":
        request = req.Request(url, headers={
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"
        })

        with req.urlopen(request) as response:
            data = response.read().decode("utf-8")
        soup = bs4.BeautifulSoup(data, "html.parser")
        h2s = soup.findAll("h2", {"class": "title"})
        for h2 in h2s:
            title_1 = h2.select_one("span.before").text
            title_2 = h2.select_one("span.pretty").text
            title_3 = h2.select_one("span.after").text
            title = title_1 + title_2 + title_3
            # print(title)
        div = soup.find(id="cover")
        div_img = div.select("img")[0]["data-src"]
        div_img_href = div_img.split(comic_img_base_url_dark, 1)[
            1].split("cover.jpg", 1)[0]
        base_img_url = comic_img_base_url_dark + div_img_href
        chapters.append(ch.Chapter(title, href, base_img_url))
    else:
        data = {"url":href} 
        data = json.dumps(data).encode('utf8')
        request = req.Request(url, data=data,
                             headers={'content-type': 'application/json'})
        with req.urlopen(request) as response:
            data = response.read().decode("utf-8")
        data = json.loads(data)
        for d in data:
            title = d['title']
            c_href = d['href']
            chapters.append(ch.Chapter(title, c_href))
    # --version----
    return c.Comic("", href, "", "", chapters)
