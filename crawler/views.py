# -*- coding: utf-8 -*-
from django.shortcuts import render
from .forms import ComicSearchForm
import crawler.crawl.crawl_comic as cc
import crawler.beans.chapter as c
from crawler.encoder import jsonEncoder as encoder
from django.views.decorators.csrf import csrf_exempt
import json

def home(request):
    return render(request, 'home/home.html')

@csrf_exempt
def search_comic(request):
    if request.method == 'POST':
        form = ComicSearchForm(request.POST)
        if form.is_valid():
            comic_name = form.cleaned_data['comic_name']
            version = form.cleaned_data['version']

            comics = cc.crawl_search_comic(comic_name,version)
            if len(comics) > 0 :
                return render(request,'comics/search.html',{
                    'comic_name': comic_name,
                    'version': version,
                    'comics':  comics
                })
            else:
                return render(request, 'home/home.html',{
                    'version': version,
                    "statement": "找不到符合的漫畫喔!!"
                })
            
    return render(request, 'home/home.html',{
        'version': "0",
        "statement": "請再次輸入!!"
    })

def show_comic(request,name,href,version):
    comic = cc.crawl_one_comic(href,version)
    comic.chapters.reverse()
    return render(request, 'comics/chapters.html',{
                    'name': name,
                    'version': version,
                    'comic_chapters_num': len(comic.chapters),
                    'comic':  comic
                })

def read_comic(request,name,href,title,version):
    comic = cc.crawl_one_comic(href,version)
    if version == "1":
        base_img_url = comic.chapters[0].base_img_url
        return render(request, 'comics/read.html',{
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
        if current_index + 1 <= len(comic.chapters):
            next_chapter_index = current_index + 1
        
        base_img_url = cc.comic_img_base_url + "/" + href + "/" +title
        return render(request, 'comics/read.html',{
            'name': name,
            'title': title,
            'href': href,
            'version': version,
            'base_img_url': base_img_url,
            'pre_chapter':  comic.chapters[pre_chapter_index].title,
            'next_chapter':  comic.chapters[next_chapter_index].title,
        })
