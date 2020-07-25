from django import forms
from crawler.models import Post

class ComicSearchForm(forms.ModelForm):
	comic_name = forms.CharField(max_length=100)

	class Meta:    
		model = Post    
		fields = ('comic_name',)