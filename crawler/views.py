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
            comics = cc.crawl_search_comic(comic_name)
            return render(request,'comics/search.html',{
                    'comics':  comics
                })
    form = ComicSearchForm()
    return render(request, 'home/home.html')

def show_comic(request,name,href):
    comic = cc.crawl_one_comic(href)
    comic.chapters.reverse()
    return render(request, 'comics/chapters.html',{
                    'name': name,
                    'comic':  comic
                })

def read_comic(request,name,href,title):
    comic = cc.crawl_one_comic(href)

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
        'base_img_url': base_img_url,
        'pre_chapter':  comic.chapters[pre_chapter_index].title,
        'next_chapter':  comic.chapters[next_chapter_index].title,
    })
