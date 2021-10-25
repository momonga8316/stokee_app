from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404, JsonResponse, HttpResponseRedirect
from django.views.generic import TemplateView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from stokee.models import Profile, Post, Like, Purchase, Relationship
from django.shortcuts import redirect, resolve_url
from django.views import generic
from django.urls import reverse_lazy

import json



@login_required
def detail_view(request, user_id, **kwargs): #uls.pyの「path('mypage/<slug:user_id>'」が読み込まれている
    user = User.objects.get(username=user_id)

    print(user_id)
    #ユーザーが投稿したアイデアだけをリストで表示させる
    post_list = Post.objects.all().filter(user_id=user.id)
    #ユーザーがいいねしたアイデアだけをリストで表示させる
    like_id = Like.objects.all().filter(user_id=user.id).values_list('post_id', flat=True)
    post_like_list = Post.objects.filter(id__in=like_id)
    #ユーザーが購入したアイデアだけをリストで表示させる
    purchase_id = Purchase.objects.all().filter(purchased_user_id=user.id).values_list('purchased_post_id', flat=True)
    post_purchase_list = Post.objects.filter(id__in=purchase_id)
    #ユーザーのフォロー数を表示させる
    
    #ユーザーのフォロワー数を表示させる

    return render(request, 'stokee/profile_detail.html', {'user':user,'post_list': post_list,'post_like_list': post_like_list, 'post_purchase_list': post_purchase_list }) 



@login_required
def follow_view(request, user_id):
    follower = User.objects.get(username=request.user.username)
    following = User.objects.get(username=user_id)
    
    
    if follower == following:
        messages.warning(request, '自分自身はフォローできません')
        print("自分自身はフォローできません")
    else:
        
        _, created = Relationship.objects.get_or_create(follower=follower, following=following)
        
        if (created):    
            X = Profile.objects.get(id=user_id)  
            print("aaa")
            Y = Profile.objects.get(id=user_id)  
            print("bbb")
            X.following_num += 1 #フォロー数を一人増やす
            print("ccc")
            Y.follower_num += 1 #フォロワー数を一人増やす
            print("ddd")
            X.save() #モデルインスタンスで保存してみた
            print("eee")
            Y.save()
            print("fff")
        
            
            messages.success(request, '{}をフォローしました'.format(following.username))
            
            print("フォローをしました")
        else:
            messages.warning(request, 'あなたはすでに{}をフォローしています'.format(following.username))
            print("すでにフォローしています")

    return HttpResponseRedirect(reverse_lazy('stokee:profile_detail', kwargs={'user_id': following.username}))



@login_required
def unfollow_view(request, user_id):
    follower = User.objects.get(username=request.user.username)
    following = User.objects.get(username=user_id)

    if follower == following:
            messages.warning(request, '自分自身のフォローを外せません')
            print("自分自身のフォローを外せません")
    else:
            
        unfollow = Relationship.objects.get(follower=follower, following=following)
        unfollow.delete()
        x = Profile.objects.get(id=user_id)  
        print("あああ")
        y = Profile.objects.get(id=user_id)  
        print("いいい")
        x.following_num -= 1 #フォロー数を一人減らす
        print("ううう")
        y.follower_num -= 1 #フォロワー数を一人減らす
        print("えええ")
        x.save() #モデルインスタンスで保存してみた
        print("おおお")
        y.save()
        print("かかか")
        
            
        messages.success(request, 'あなたは{}のフォローを外しました'.format(following.username))
        print("フォローを解除しました")
    
    return HttpResponseRedirect(reverse_lazy('stokee:profile_detail', kwargs={'user_id': following.username}))

