# path()関数のインボート 
import django.contrib.auth.views
from django.urls import path
from stokee.views import mypage, post, tag, profile

from stokee.views.emailchange import change_view, change_validation_view, change_done_view
from stokee.views.password import pass_change_view, pass_change_done_view, reset_view, reset_done_view, reset_confirm_view, reset_complete_view


# ルーティングの設定 

app_name = 'stokee'

urlpatterns = [
    path('mypage', mypage.mypage_top, name='mypage_top'),
    #マイページ編集ページ
    path('mypage/update/', mypage.UserChangeView.as_view(), name='mypage_update'),

    #ユーザープロフィール詳細ページ
    path('profile/<slug:user_id>/', profile.detail_view, name='profile_detail'), 
    #フォローする・フォローを外す
    path('profile/<slug:user_id>/follow', profile.follow_view, name='follow'),
    path('profile/<slug:user_id>/unfollow', profile.unfollow_view, name='unfollow'),
    
    #登録情報関係
    path('email/change/', change_view, name='email_change'),
    path('email/change/validation/<token>/', change_validation_view, name='email_change_complete'),
    path('email/change/done', change_done_view, name='email_change_done'),
    path('password_change/', pass_change_view, name='password_change'),
    path('password_change/done/', pass_change_done_view, name='password_change_done'),

    path('password_reset/', reset_view, name='password_reset'),
    path('password_reset/done/', reset_done_view, name='password_reset_done'),
    path('password_reset/confirm/<uidb64>/<token>/', reset_confirm_view, name='password_reset_confirm'),
    path('password_reset/complete/', reset_complete_view, name='password_reset_complete'),

    path('post/', post.list_view, name='post_list'),
    path('post/<slug:post_id>', post.detail_view, name='post_detail'),
    path('post/<int:post_id>/like/', post.like, name='like'),
    path("create/", post.new, name="create"),
    path('tags/', tag.TagListView.as_view(), name='tag_list'),
    path('tag/<str:tag_slug>/', tag.TagPostView.as_view(), name='tag_detail'),
    path('create_checkout_session/<slug:post_id>', post.create_checkout_session, name='checkout_session'),

    
     # アイデア購入後に表示されるページ
    path('post/buy/<slug:post_id>', post.bought_post_detail_view, name='buy_post_detail'), 




]