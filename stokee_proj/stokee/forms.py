from django import forms
from django.contrib.auth.models import User
from stokee.models import Comment, Post, Profile
from django.views.generic import UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required




class UserChangeForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['full_name','image','company','position','introduce','URL' ]

    def __init__(self, full_name=None, image=None, company=None, position=None, introduce=None, URL=None, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super().__init__(*args, **kwargs)
        # ユーザーの更新前情報をフォームに挿入
        
        if full_name:
            self.fields['full_name'].widget.attrs['value'] = full_name
        if image:
            self.fields['image'].widget.attrs['value'] = image
        if company:
            self.fields['company'].widget.attrs['value'] = company
        if position:
            self.fields['position'].widget.attrs['value'] = position
        if introduce:
            self.fields['introduce'].widget.attrs['value'] = introduce
        if URL:
            self.fields['URL'].widget.attrs['value'] = URL

    def update(self, user):
        
        user.full_name = self.cleaned_data['full_name']
        user.image = self.cleaned_data['image']
        user.company = self.cleaned_data['company']
        user.position = self.cleaned_data['position']
        user.introduce = self.cleaned_data['introduce']
        user.URL = self.cleaned_data['URL']
    
        user.save()


class CreateForm(forms.ModelForm):
    """アイデア投稿フォーム"""

    title = forms.CharField(
          label='どんな事業アイデア？',
          required=True,
          disabled=False,
          max_length=140,
          min_length=1,
          widget=forms.TextInput(attrs={
        'placeholder':'ビジネスアイデアのタイトルを書いてみよう'
    })) 

    content = forms.CharField(
          label='アイデアを思いついたきっかけは？',
          required=True,
          disabled=False,
          max_length=500,
          min_length=1,
          widget=forms.Textarea(attrs={
        'placeholder':'アイデアを思いついたきっかけを10文字以上で書いてください'
    }))

    description = forms.CharField(
          label='アイデアをもう少し詳しく話すと？',
          required=True,
          disabled=False,
          max_length=500,
          min_length=1,
          widget=forms.Textarea(attrs={
        'placeholder':'アイデアをもう少し詳しく書いてください'
    }))  
    

    class Meta():
        model = Post
        fields = ['title', 'content', 'description', 'price']
        labels = {
            'title': 'どんな事業アイデア？',
            'content': 'アイデアを思いついたきっかけは？',
            'description': 'アイデアをもう少し詳しく話すと？',
            'price': 'アイデアの販売価格を決めよう',
        }
    

class CommentForm(forms.ModelForm):
    """コメント投稿フォーム"""
    class Meta:
        model = Comment
        fields = ['text']
        labels = {
            'text': 'コメント',
        }
    
    