# Create your models here.
from django.contrib.auth.models import User, AbstractUser 
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
 
class Profile(models.Model):
    class Meta:
        verbose_name = 'ユーザー情報データ'
        verbose_name_plural = 'ユーザー情報データ'
    
    user = models.OneToOneField(User, verbose_name='ユーザー',null=True, blank=True, on_delete=models.CASCADE)

    id = models.CharField('ユーザーID',max_length=20,primary_key=True) # 'user_name'
    email = models.EmailField('メールアドレス', max_length=255, null=True)
    full_name = models.CharField('氏名',max_length=50)      # '藤川希'
    company = models.CharField('所属',max_length=50)      # 'エブセレ株式会社'
    position = models.CharField('役職',max_length=50)    # '代表取締役'
    image = models.ImageField(upload_to='media/images/user_image',null=True, blank=True,) # 'プロフィール画像'
    introduce = models.TextField('自己紹介',blank=True,null=True,max_length=1000) # '自己紹介文'
    URL = models.URLField() # 'TwitterURL'
    #followees = models.ManyToManyField(
        #'User', verbose_name='フォロー中のユーザー', through='Relationship',
        #related_name='followees', through_fields=('follower', 'following'))
    #followers = models.ManyToManyField(
        #'User', verbose_name='フォローされているユーザー', through='Relationship', 
        #related_name='followers', through_fields=('following', 'follower'))
    following_num = models.IntegerField('フォロー', default=0)
    follower_num = models.IntegerField('フォロワー', default=0)
   
    #管理画面で表示される文字列を定義する
    def __str__(self):
        #ログインログアウト機能の時に追加
        user_str = ''
        if self.user is not None:
            user_str = '(' + self.user.username + ')'

        return self.id 



class Relationship(models.Model):
    class Meta:
        verbose_name = 'フォロー情報データ'
        verbose_name_plural = 'フォロー情報データ'
        #unique_together = ('follower', 'following')

    follower = models.ForeignKey(User, related_name='follower', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.follower} follows {self.following}"



class Tag(models.Model):
    class Meta:
        verbose_name = 'タグ情報データ'
        verbose_name_plural = 'タグ情報データ'

    name = models.CharField(max_length=50)
    slug = models.SlugField(null=True, blank=True)

    def __str__(self):
        return self.name



class Post(models.Model):
    class Meta:
        verbose_name = 'アイデア情報データ'
        verbose_name_plural = 'アイデア情報データ'
    tags = models.ManyToManyField(Tag, blank=True)
    title = models.TextField(blank=True)
    content = models.TextField(blank=True)
    description = models.TextField(blank=True)
    price = models.PositiveSmallIntegerField('アイデア価格',blank=True, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey(get_user_model(),verbose_name='アイデア投稿者',null=True, blank=True,on_delete=models.CASCADE)
    like_num = models.IntegerField('いいね', default=0)
    comment_num = models.IntegerField('コメント', default=0)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title



class Like(models.Model):
    class Meta:
        verbose_name = 'いいね情報データ'
        verbose_name_plural = 'いいね情報データ'

    post = models.ForeignKey(Post, null=True, blank=True, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), null=True, blank=True, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)


class Comment(models.Model):
    class Meta:
        verbose_name = 'コメント情報データ'
        verbose_name_plural = 'コメント情報データ'
    #アイデアに紐づくコメント
    post = models.ForeignKey(Post, null=True, blank=True, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(get_user_model(),verbose_name='コメント投稿者',null=True, blank=True,on_delete=models.CASCADE)
    text = models.TextField('本文')
    created_at = models.DateTimeField('作成日', auto_now_add=True)
 
    def __str__(self):
        return self.text[:2]



class Purchase(models.Model):
    class Meta:
        verbose_name = 'アイデア購入情報データ'
        verbose_name_plural = 'アイデア購入情報データ'
    
    #購入した時のデータ
    purchased_user = models.ForeignKey(User,verbose_name='購入者',null=True, blank=True,on_delete=models.CASCADE)
    purchased_post = models.ForeignKey(Post, null=True, blank=True, on_delete=models.CASCADE)
    timestamp = models.DateTimeField('購入日時', auto_now_add=True) #購入時の現在時刻'13:15'


