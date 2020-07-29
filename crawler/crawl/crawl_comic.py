# -*- coding: utf-8 -*-
import urllib.request as req
import urllib.parse as parse
import bs4
import crawler.beans.search as s
import crawler.beans.comic as c
import crawler.beans.chapter as ch

base_url = "https://www.ohmanhua.com/"
base_search_url = "https://www.ohmanhua.com/search?searchString="
base_search_url_dark = "https://nhentai.net/search/?q="
base_g_url_dark = "https://nhentai.net/g/"
comic_img_base_url = "https://img.ohmanhua.com/comic"
comic_img_base_url_dark = "https://t.nhentai.net/galleries"


def crawl_search_comic(searchString, page, version):
    encodeStr = parse.quote(searchString)

    # --version----
    if version == "1":
        url = base_search_url_dark + encodeStr
    else:
        url = base_search_url + encodeStr + "&page=" + page
    # --version----

    request = req.Request(url, headers={
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"
    })

    with req.urlopen(request) as response:
        data = response.read().decode("utf-8")

    soup = bs4.BeautifulSoup(data, "html.parser")

    page_num = 1
    comics = []
    # --version----
    if version == "1":
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
        end_page = 1
        a_s = soup.findAll(
            "a", {"class": "fed-btns-info fed-rims-info show-page-jump"})
        for a in a_s:
            end_page = int(a["data-total"])
            # print(end_page)
        page_num = end_page

        dls = soup.findAll("dl", {
            "class": "fed-deta-info fed-deta-padding fed-line-top fed-margin fed-part-rows fed-part-over"})
        for dl in dls:
            dt_a = dl.select_one("dt a")
            comic_img_url = dt_a["data-original"]
            # print(comic_img_url)
            dd_a = dl.select_one("dd a")
            comic_url = dd_a["href"]
            # print(comic_url)
            comic_name = dd_a.text
            # print(comic_name)
            comics.append(c.Comic(comic_name, comic_url, comic_img_url))
            # break                         # ---ttttteeeessstttt----
    # --version----

    if len(comics) == 0:
        page_num = 0
    return s.Search(searchString, page_num, comics)

def crawl_one_comic(href, version):

    # --version----
    if version == "1":
        url = base_g_url_dark + href
    else:
        url = base_url + href
    # --version----
    request = req.Request(url, headers={
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"
    })

    with req.urlopen(request) as response:
        data = response.read().decode("utf-8")

    soup = bs4.BeautifulSoup(data, "html.parser")

    chapters = []
    # --version----
    if version == "1":
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
        lis = soup.findAll(
            "li", {"class": "fed-padding fed-col-xs6 fed-col-md3 fed-col-lg3"})
        for li in lis:
            a = li.select_one("a")
            title = a["title"]
            # print(title)
            base_img_url = comic_img_base_url + href + title
            chapters.append(ch.Chapter(title, href, base_img_url))
            # break                         # ---ttttteeeessstttt----
    # --version----
    return c.Comic("", href, "", "", chapters)
