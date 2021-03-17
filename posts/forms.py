from django import forms
from .models import *


class PostForm(forms.ModelForm):
    content=forms.CharField(widget=forms.Textarea(attrs={
        'rows':3,
    }))
    class Meta:
        model = Post
        fields = ['content','image']


class commentForm(forms.ModelForm):
    body=forms.CharField(label='',widget=forms.TextInput(attrs={
        'placeholder':'add a comment...',
    }))
    class Meta:
        model=Comments
        fields=['body']