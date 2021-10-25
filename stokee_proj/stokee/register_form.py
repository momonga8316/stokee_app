from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from stokee.models import Profile
from django.contrib.auth import get_user_model
User = get_user_model()

class RegisterForm(UserCreationForm):    
    full_name = forms.CharField(label='氏名',required=True) #'藤川希'
    company = forms.CharField(label='所属先（会社名/学校名）',required=False)  #'エブセレ株式会社'
    position = forms.CharField(label='役職・部署',required=True)  #'代表取締役'
    image = forms.ImageField(label='プロフィール画像',required=False) #'プロフィール画像'
    introduce = forms.CharField(label='自己紹介文',widget=forms.Textarea,required=False) #'自己紹介文'
    URL = forms.URLField(label='Twitterのリンク',required=True) #'TwitterURL'
    

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2','full_name','image','company','position','introduce','URL' ]
        labels = {
            'username': 'ユーザー名',
            'email': 'メールアドレス',
            'password1': 'パスワード',
            'password2': 'パスワード確認',
            'full_name': '氏名',
            'image': 'プロフィール画像',
            'company': '所属先／会社名',
            'position': '役職',
            'introduce': '自己紹介',
            'URL': 'URL',
        }

    def save(self, commit=True):
        if not commit:
            raise NotImplementedError('Cannot create User and Profile without database save')
        
        user = super().save()


        user_id = self.cleaned_data['username']
        full_name = self.cleaned_data['full_name']
        company = self.cleaned_data['company']
        position = self.cleaned_data['position']
        image = self.cleaned_data['image']
        introduce = self.cleaned_data['introduce']
        URL = self.cleaned_data['URL']

        profile = Profile(id=user_id,full_name=full_name,company=company,position=position,image=image,user_id=user.id,introduce=introduce,URL=URL)
        profile.save()

        return user

    def clean_email(self):
        email = self.cleaned_data['email']
        User.objects.filter(email=email, is_active=False).delete()
        return email