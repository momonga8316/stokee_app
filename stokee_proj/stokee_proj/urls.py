"""stokee_proj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# path()関数、include()関数のインポート 
from django.urls import include, path #デフォルトのurls.pyにincludeを追加
# 管理サイトの機能をインポート 
from django.contrib import admin 
from django.shortcuts import render
from . import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth.decorators import login_required
from stokee.views.register import register_view, done_view, validation_view
from stokee.models import Post, Comment, Tag, Like, Profile
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Q


def index(request):
    post_list = Post.objects.all().order_by('-id')
    paginator = Paginator(post_list, 5) # 最新のアイデアを5個表示
    
    try:
        page = int(request.GET.get('page'))
    except:
        page = 1

    posts = paginator.get_page(page)

    return render(request, 'index.html',  {'posts': posts, 'page': page, 'last_page': paginator.num_pages})

urlpatterns = [
    # stokee アプリケーションの URL 設定を追加 
    path('', index, name='index'),
    path('stokee/', include('stokee.urls')),
    path('stokee/', include('social_django.urls', namespace='social')),
    
    # 管理サイト 
    path('admin/', admin.site.urls), 
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register/', register_view, name='register'),
    path('accounts/register/validation/<token>/', validation_view, name='create_complete'),
    path('accounts/register/done', done_view, name='register_done'),
    
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)