from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404, JsonResponse
from django.views.generic import TemplateView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from stokee.models import Profile, Post, Like, Purchase
from django.shortcuts import redirect, resolve_url

from django.urls import reverse_lazy
import json
from stokee.forms import UserChangeForm
from django.views.generic import FormView


@login_required
def mypage_top(request):
    user = request.user
    #ログインしているユーザーが投稿したアイデアだけをリストで表示させる
    post_list = Post.objects.all().filter(user_id=user.id)
    #ログインしているユーザーがいいねしたアイデアだけをリストで表示させる
    like_id = Like.objects.all().filter(user_id=user.id).values_list('post_id', flat=True)
    post_like_list = Post.objects.filter(id__in=like_id)
    #ログインしているユーザーが購入したアイデアだけをリストで表示させる
    purchase_id = Purchase.objects.all().filter(purchased_user_id=user.id).values_list('purchased_post_id', flat=True)
    post_purchase_list = Post.objects.filter(id__in=purchase_id)


    return render(request, 'stokee/mypage.html', {'user':user,'post_list': post_list,'post_like_list': post_like_list, 'post_purchase_list': post_purchase_list }) 


class UserChangeView(FormView):
    template_name = 'stokee/mypage_update.html'
    form_class = UserChangeForm
    success_url = reverse_lazy('stokee:mypage_top')
    
    def form_valid(self, form):
        #formのupdateメソッドにログインユーザーを渡して更新
        form.update(user=self.request.user.profile)
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # 更新前のユーザー情報をkwargsとして渡す
        kwargs.update({
            
            'full_name' : self.request.user.profile.full_name,
            'image' : self.request.user.profile.image,
            'company' : self.request.user.profile.company,
            'position' : self.request.user.profile.position,
            'introduce' : self.request.user.profile.introduce,
            'URL' : self.request.user.profile.URL,
            
        })
        return kwargs

