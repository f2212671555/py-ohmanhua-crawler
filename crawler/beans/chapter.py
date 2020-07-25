class Chapter():
    def __init__(self, title = "", href = "", base_img_url = ""):
        self._title = title
        self._href = href
        self._base_img_url = base_img_url

    def __str__(self):
        return 'title: %s  href: %s base_img_url: %s' %(self._title,self._href,self._base_img_url)

    def __repr__(self):
        return self.__str__()
        
    @property
    def title(self):
        return self._title
    
    @title.setter
    def set_title(self, title):
        self._title = title

    @property
    def href(self):
        return self._href
    
    @href.setter
    def set_href(self, href):
        self._href = href
    
    @property
    def base_img_url(self):
        return self._base_img_url
    
    @base_img_url.setter
    def set_base_img_url(self, base_img_url):
        self._base_img_url = base_img_url