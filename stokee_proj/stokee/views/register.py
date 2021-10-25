from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy, reverse
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.signing import BadSignature, SignatureExpired, loads, dumps
from django.http import Http404, HttpResponseBadRequest, HttpResponse, HttpResponseRedirect
from stokee.register_form import RegisterForm

class RegisterView(CreateView):
    template_name = 'registration/register_form.html'
    form_class = RegisterForm
    def form_valid(self, form):
        """仮登録と本登録用メールの発行."""
        # 仮登録と本登録の切り替えは、is_active属性を使うと簡単です。
        # 退会処理も、is_activeをFalseにするだけにしておくと捗ります。
        user = form.save()
        user.is_active = False
        user.save()

        email = form.cleaned_data['email'] 
        print(email)

        # アクティベーションURLをメールで送付
        current_site = get_current_site(self.request)
        domain = current_site.domain

        subject = "StoKee - Register"
        message = f"{ email }様、StoKeeにご登録いただきありがとうございます。下記リンクをクリックして登録を完了して下さい:\n\n {self.request.scheme}://{domain}/accounts/register/validation/{dumps(user.pk)}\n"

        print(subject, message)
        user.email_user(subject, message)

        return HttpResponse("<h1>あと1ステップで登録完了です。</h1><br><h2>入力いただいたメールアドレスに会員登録確認用URLをお送りしました。</h2><h2>送信したメールのリンクから本登録を行って下さい。</h2>")


register_view = RegisterView.as_view()


class ValidationView(TemplateView):
    template_name = "registration/register_validation.html"
    timeout_seconds = getattr(settings, 'ACTIVATION_TIMEOUT_SECONDS', 60*60*24)  # デフォルトでは1日以内

    def get(self, request, **kwargs):
        """tokenが正しければ本登録."""
        token = kwargs.get('token')
        try:
            user_pk = loads(token, max_age=self.timeout_seconds)

        # 期限切れ
        except SignatureExpired:
            return HttpResponseBadRequest()

        # tokenが間違っている
        except BadSignature:
            return HttpResponseBadRequest()

        # tokenは問題なし
        else:
            try:
                user = User.objects.get(pk=user_pk)
            except User.DoesNotExist:
                return HttpResponseBadRequest()
            else:
                if not user.is_active:
                    # 問題なければ本登録とする
                    user.is_active = True
                    user.save()
                    return super().get(request, **kwargs)

        return HttpResponseBadRequest()

validation_view = ValidationView.as_view()


class DoneView(TemplateView):
    template_name = 'registration/register_done.html'

done_view = DoneView.as_view()

