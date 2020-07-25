class Comic():
    def __init__(self, name='', href="", img_url="",detail="", chapters = []):
        self._name = name
        self._href = href
        self._img_url = img_url
        self._detail = detail
        self._chapters = chapters

    def __str__(self):
        return 'name: %s  href: %s img_url: %s detail: %s chapters: %s' %(self._name,self._href,self._img_url,self._detail,self._chapters)

    def __repr__(self):
        return self.__str__()

    @property
    def name(self):
        return self._name
    
    @name.setter
    def set_name(self, name):
        self._name = name
    
    @property
    def href(self):
        return self._href
    
    @href.setter
    def set_href(self, href):
        self._href = href
    
    @property
    def img_url(self):
        return self._img_url
    
    @img_url.setter
    def set_img_url(self, img_url):
        self._img_url = img_url

    @property
    def detail(self):
        return self._detail
    
    @detail.setter
    def set_detail(self, detail):
        self._detail = detail
    
    @property
    def chapters(self):
        return self._chapters
    
    @chapters.setter
    def set_chapters(self, chapters):
        self._chapters = chapters