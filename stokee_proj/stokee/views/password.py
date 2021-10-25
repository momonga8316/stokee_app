from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import reverse_lazy
from stokee.password_form import MyPasswordChangeForm, MyPasswordResetForm, MySetPasswordForm
from django.contrib.sites.shortcuts import get_current_site
from django.http import Http404, HttpResponseBadRequest, HttpResponse

class PasswordChange(PasswordChangeView):
    """パスワード変更ビュー"""
    form_class = MyPasswordChangeForm
    success_url = reverse_lazy('stokee:password_change_done')
    template_name = 'password/password_change.html'

pass_change_view = PasswordChange.as_view()

class PasswordChangeDone(PasswordChangeDoneView):
    """パスワード変更しました"""
    template_name = 'password/password_change_done.html'


pass_change_done_view = PasswordChangeDone.as_view()



class PasswordReset(PasswordResetView):
    """パスワード変更用URLの送付ページ"""
    subject_template_name = 'password/subject.txt'
    email_template_name = 'password/message.txt'
    template_name = 'password/password_reset_form.html'
    form_class = MyPasswordResetForm
    success_url = reverse_lazy('stokee:password_reset_done')

reset_view = PasswordReset.as_view()

class PasswordResetDone(PasswordResetDoneView):
    """パスワード変更用URLを送りましたページ"""
    template_name = 'password/password_reset_done.html'


reset_done_view = PasswordResetDone.as_view()

class PasswordResetConfirm(PasswordResetConfirmView):
    """新パスワード入力ページ"""
    form_class = MySetPasswordForm
    success_url = reverse_lazy('stokee:password_reset_complete')
    template_name = 'password/password_reset_confirm.html'


reset_confirm_view = PasswordResetConfirm.as_view()


class PasswordResetComplete(PasswordResetCompleteView):
    """新パスワード設定しましたページ"""
    template_name = 'password/password_reset_complete.html'


reset_complete_view = PasswordResetComplete.as_view()