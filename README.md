# StoKee


**フォロー機能・コードのありか**

#### models.py
`stokee_proj --> stokee --> models.py`

#### vews.py
`stokee_proj --> stokee --> templates --> stokee --> mypage.html または profile_details.html`

#### html
`stokee_proj --> stokee --> views --> profile.py`

　＜起きたこと＞

Modelsの`Profile`に`follower,followeeのManytoManyフィールド`を設定してないが故に、フォロー機能自体はできても、
実際にフォローした人の人数を増やしたり、フォロワー一覧を表示したりなど、追加の機能をつけようとした時につまづいた。
（つまり、ManytoManyテーブルを作る前に中間テーブルとなるRelationテーブルだけ作ってしまった。）


＜次にしたこと＞

Profileテーブルにfriends/manytomanyフィールドを追加
中間テーブルと紐付ける

models内
#followees = models.ManyToManyField(
        #'User', verbose_name='フォロー中のユーザー', through='Relationship',
        #related_name='followees', through_fields=('follower', 'following'))
    #followers = models.ManyToManyField(
        #'User', verbose_name='フォローされているユーザー', through='Relationship', 
        #related_name='followers', through_fields=('following', 'follower'))


を追加しようとしたらエラーが出たから、諦めました。。。。


＜本当はこんなことがやりたい＞

フォロー機能がつけたいというよりは、*YOUTRUST　みたいな　友達申請　が作りたい*
かつ、友達の友達の投稿をフィードに表示させたい

```
AさんがBさんにつながり申請
↓
Bさんにユーザー申請がきたことを通知
↓
申請を受け取ったAさんは、申請を許可するか選択できる
↓
Aさんが許可した場合にBさんはAさんと友達になれる
```

