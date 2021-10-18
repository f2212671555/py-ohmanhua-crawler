# -*- coding: utf-8 -*-
from django.shortcuts import render
from .forms import ComicSearchForm
import crawler.crawl.crawl_comic as cc
import crawler.beans.chapter as c
from crawler.encoder import jsonEncoder as encoder
from django.views.decorators.csrf import csrf_exempt
import json
import urllib.request as req

comic_image_api_url = "https://comic-api-server.herokuapp.com/comic/image/"

def home(request):
    return render(request, 'home/home.html')


@csrf_exempt
def search_comic(request):
    if request.method == 'POST':
        form = ComicSearchForm(request.POST)
        if form.is_valid():
            comic_name = form.cleaned_data['comic_name']
            version = form.cleaned_data['version']
            page = form.cleaned_data['page']

            search = cc.crawl_search_comic(comic_name, page,version)
            if search.page_num > 0:
                return render(request, 'comics/search.html', {
                    'comic_name': comic_name,
                    'version': version,
                    'current_page': page,
                    'search':  search
                })
            else:
                return render(request, 'home/home.html', {
                    'version': version,
                    "statement": "找不到符合的漫畫喔!!"
                })

    return render(request, 'home/home.html', {
        'version': "0",
        "statement": "請再次輸入!!"
    })
# , name, version
def show_comic(request):
    name = request.POST.get("name","")
    href = request.POST.get("href","")
    version = request.POST.get("version","")
    comic = cc.crawl_one_comic(href, version)
    comic.chapters.reverse()
    return render(request, 'comics/chapters.html', {
        'name': name,
        'version': version,
        'comic_chapters_num': len(comic.chapters),
        'comic':  comic
    })


def read_comic(request):
    name = request.POST.get("name","")
    href = request.POST.get("href","")
    title = request.POST.get("title","")
    version = request.POST.get("version","")
    comic = cc.crawl_one_comic(href, version)
    if version == "1":
        base_img_url = comic.chapters[0].base_img_url
        return render(request, 'comics/read.html', {
            'name': name,
            'title': title,
            'href': href,
            'version': version,
            'base_img_url': base_img_url,
            'pre_chapter':  "",
            'next_chapter':  "",
        })
    else:
        current_index = 0
        for i in range(len(comic.chapters)):
            if comic.chapters[i].title == title:
                current_index = i
                break

        pre_chapter_index = current_index
        next_chapter_index = current_index
        if current_index - 1 >= 0:
            pre_chapter_index = current_index - 1
        if current_index + 1 < len(comic.chapters):
            next_chapter_index = current_index + 1

        print(pre_chapter_index)
        print(next_chapter_index)
        print(comic.chapters[current_index].href)
        data = {"url":comic.chapters[current_index].href} 
        data = json.dumps(data).encode('utf8')
        imgRequest = req.Request(comic_image_api_url, data=data,
                            headers={'content-type': 'application/json'})
        with req.urlopen(imgRequest) as response:
            data = response.read().decode("utf-8")
        base_img_url = json.loads(data)[0]['url'].split('/0001')[0]
        print(base_img_url)

        return render(request, 'comics/read.html', {
            'name': name,
            'title': title,
            'href': href,
            'version': version,
            'base_img_url': base_img_url,
            'pre_chapter':  comic.chapters[pre_chapter_index].title,
            'next_chapter':  comic.chapters[next_chapter_index].title,
        })
