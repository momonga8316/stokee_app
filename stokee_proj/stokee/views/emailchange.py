from django.views import generic
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.signing import BadSignature, SignatureExpired, loads, dumps
from django.http import Http404, HttpResponseBadRequest, HttpResponse
from stokee.emailchange_form import EmailChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin


class EmailChange(LoginRequiredMixin, generic.FormView):
    """メールアドレスの変更"""
    template_name = 'emailchange/email_change_form.html'
    form_class = EmailChangeForm

    def form_valid(self, form):
        user = self.request.user
        new_email = form.cleaned_data['email']

        # URLの送付
        current_site = get_current_site(self.request)
        domain = current_site.domain

        subject = "StoKee - メールアドレスの変更"
        message = f"{ new_email }様、下記URLよりサイトにアクセスすると、メールアドレスの変更が完了します:\n\n http://{domain}/stokee/email/change/validation/{dumps(new_email)}\n"
        
        print(subject, message)
        user.email_user(subject, message)


        return HttpResponse("<h1>あと1ステップでメールアドレス変更完了です。</h1><br><h2>入力いただいたメールアドレスにメールアドレス変更用URLをお送りしました。</h2><h2>送信したメールのリンクからメールアドレスの変更を行って下さい。</h2>")

change_view = EmailChange.as_view()



class EmailChangeValidationView(LoginRequiredMixin, generic.TemplateView):
    """リンクを踏んだ後に呼ばれるメアド変更ビュー"""
    template_name = 'emailchange/email_change_validation.html'
    timeout_seconds = getattr(settings, 'ACTIVATION_TIMEOUT_SECONDS', 60*60*24)  # デフォルトでは1日以内

    def get(self, request, **kwargs):
        """tokenが正しければメールアドレス変更."""
        token = kwargs.get('token')
        try:
            new_email = loads(token, max_age=self.timeout_seconds)

        # 期限切れ
        except SignatureExpired:
            return HttpResponseBadRequest()

        # tokenが間違っている
        except BadSignature:
            return HttpResponseBadRequest()

        # tokenは問題なし
        # tokenは問題なし
        else:
            User.objects.filter(email=new_email, is_active=False).delete()
            request.user.email = new_email
            request.user.save()
            return super().get(request, **kwargs)

change_validation_view = EmailChangeValidationView.as_view()

class EmailChangeDoneView(LoginRequiredMixin, generic.TemplateView):
    """メールアドレスの変更メールを送ったよ"""
    template_name = 'emailchange/email_change_done.html'

change_done_view = EmailChangeDoneView.as_view()