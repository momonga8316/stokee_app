from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404, JsonResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required #ログインしてないと見れない設定
from stokee.models import Post, Comment, Tag, Like, Profile, Purchase
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from stokee.forms import CommentForm, CreateForm
from django.contrib import messages
from django.db.models import Q
from django.urls import reverse_lazy
import json
from django.conf import settings
import stripe
from django.urls import reverse


@login_required
def list_view(request):
    post_list = Post.objects.all().order_by('-id')
    paginator = Paginator(post_list, 10) # ページ当たり10個表示
    keyword = request.GET.get('keyword')

    try:
        page = int(request.GET.get('page'))
    except:
        page = 1

    posts = paginator.get_page(page)

    if keyword:
        posts = Post.objects.filter(
                 Q(title__icontains=keyword) | Q(content__icontains=keyword)
               )
        messages.success(request, '「{}」の検索結果'.format(keyword))

    return render(request, 'stokee/post_list.html',  {'posts': posts, 'page': page, 'last_page': paginator.num_pages})

@login_required
def detail_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    key_data = {
        "publishable_key":settings.STRIPE_PUBLISHABLE_KEY,
    }
    try:
        page = int(request.GET.get('from_page'))
    except:
        page = 1
        
    return render(request, 'stokee/post_detail.html', {'post': post, 'page': page, 'data_json':json.dumps(key_data)})
    


@login_required
def new(request):
    if request.method == 'POST':
        form = CreateForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('stokee:post_list')
    else:
       form = CreateForm()
    return render(request, 'stokee/create.html', {'form': form})


@login_required
def like(request, **kwargs):
    user = request.user    
    post = Post.objects.get(id=kwargs['post_id'])
    is_like = Like.objects.filter(user=user.id).filter(post=post).count()
    
    # unlike
    if is_like > 0:
        liking = Like.objects.get(post__id=kwargs['post_id'], user=user.id)
        liking.delete()
        post.like_num -= 1
        post.save()
        messages.warning(request, 'いいねを取り消しました')
        return redirect(reverse_lazy('stokee:post_detail', kwargs={'post_id': kwargs['post_id']}))
    # like
    post.like_num += 1
    post.save()
    like = Like()
    like.user = user
    like.post = post
    like.save()
    messages.success(request, 'いいね！しました')
    return HttpResponseRedirect(reverse_lazy('stokee:post_detail', kwargs={'post_id': kwargs['post_id']}))



@login_required
# 「この商品を購入」ボタンが押された時の関数
def create_checkout_session(request, post_id):
    
    # settings.pyから秘密鍵を読み込む
    stripe.api_key = settings.STRIPE_SECRET_KEY

    try:
       post = get_object_or_404(Post, id=post_id) 
       checkout_session = stripe.checkout.Session.create(
           # カード決済
           payment_method_types=['card'],
           # 決済内容を記述

           line_items=[
               {
                   'price_data': {
                       # 通貨（円）
                       'currency': 'jpy',
                       # 金額
                       'unit_amount': post.price,
                       # 商品説明・画像
                       'product_data': {
                           'name': post.title,
    
                       },
                   },
                   # 個数
                   'quantity': 1,
               },
           ],
           mode='payment',
           # 成功すれば投稿詳細ページへ。本番環境では下のIPアドレスをこっち（13.113.139.112）変える必要があるよ
           success_url="http://127.0.0.1:8000/stokee/post/buy/"+ str(post.id),
           # 中止すれば"購入前投稿ページ"へ。本番環境では下のIPアドレスを変える必要があるよ
           cancel_url="http://127.0.0.1:8000/stokee/post/"+ str(post.id),
       )

       print("session id :", checkout_session.id)
       return JsonResponse({'id': checkout_session.id})
    except Exception as e:
       print("Error", str(e))
       return JsonResponse({'error':str(e)})




@login_required
def bought_post_detail_view(request, post_id):

    post = get_object_or_404(Post, id=post_id)
    user_id = request.user.id #そもそもuserが存在しているかどうかを確認
    comments = Comment.objects.filter(post=post)
    
    
    if request.method == "POST": #入力フォームはPOSTなので
        form = CommentForm(request.POST)
        if form.is_valid(): #もし、formの内容が正しい時は
            comment = form.save(commit=False) #formの内容はまだセーブしません！
            comment.post = post
            comment.user = request.user
            post.comment_num += 1
            post.save()
            comment.save() #ユーザーを追加したのちにセーブ
            
    
            
            
    else:
        form = CommentForm()

    try:
        page = int(request.GET.get('from_page'))
    except:
        page = 1
    
    purchase_post = Purchase(purchased_user_id=user_id, purchased_post_id=post_id) #テーブルの中に情報を追加
    purchase_post.save() #Purchaseテーブルを保存

    return render(request, 'stokee/buy_post_detail.html', {'post': post, 'page': page,'form': form,
        'comments': comments})


