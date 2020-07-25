# -*- coding: utf-8 -*-
from django.shortcuts import render
from .forms import ComicSearchForm
import crawler.crawl.crawl_comic as cc

def home(request):
    return render(request, 'home/home.html')

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
    return render(request, 'comics/chapters.html',{
                    'name': name,
                    'comic':  comic
                })

def read_comic(request,name,href,title):
    # comic = cc.crawl_one_comic(href)
    base_img_url = cc.comic_img_base_url + "/" + href + "/" +title
    return render(request, 'comics/read.html',{
        'name': name,
        'title': title,
        'href': href,
        'base_img_url': base_img_url,
    })
    