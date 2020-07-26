# -*- coding: utf-8 -*-
from django.db import models

class Post(models.Model):  
  comic_name = models.CharField(max_length=500)
  version = models.CharField(max_length=100)