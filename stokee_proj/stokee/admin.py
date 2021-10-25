from django.contrib import admin 

# モデルをインポート 
from .models import Profile, Post, Comment, Tag, Like, Purchase, Relationship

# 管理サイトへのモデルの登録 
admin.site.register(Profile) 
admin.site.register(Post) 
admin.site.register(Comment) 
admin.site.register(Tag)
admin.site.register(Like)
admin.site.register(Purchase)
admin.site.register(Relationship)