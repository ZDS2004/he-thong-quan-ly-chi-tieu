from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User


class StyledAuthForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update(
            {"placeholder": "Tên đăng nhập", "autocomplete": "username"}
        )
        self.fields["password"].widget.attrs.update(
            {"placeholder": "Mật khẩu", "autocomplete": "current-password"}
        )


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=False, label="Email")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({"placeholder": "Tên đăng nhập"})
        self.fields["email"].widget.attrs.update({"placeholder": "email@ví dụ.com"})
        self.fields["password1"].widget.attrs.update({"placeholder": "Mật khẩu"})
        self.fields["password2"].widget.attrs.update({"placeholder": "Nhập lại mật khẩu"})
