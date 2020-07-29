class Search():
    def __init__(self, search_str='', page_num=0, comics=[]):
        self._search_str = search_str
        self._page_num = page_num
        self._comics = comics

    def __str__(self):
        return 'search_str: %s page_num: %d comics: %s' % (self._search_str, self._page_num, self._comics)

    def __repr__(self):
        return self.__str__()

    def __jsonencode__(self):
        return {'search_str': self._search_str,
                'page_num': self._page_num,
                'comics': self._comics
                }

    @property
    def search_str(self):
        return self._search_str

    @search_str.setter
    def set_search_str(self, search_str):
        self._search_str = search_str

    @property
    def page_num(self):
        return self._page_num

    @page_num.setter
    def set_page_num(self, page_num):
        self._page_num = page_num

    @property
    def comics(self):
        return self._comics

    @comics.setter
    def set_comics(self, comics):
        self._comics = comics
