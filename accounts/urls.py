from django.urls import path

from .views import RegisterView, SignInView, SignOutView

app_name = "accounts"

urlpatterns = [
    path("dang-nhap/", SignInView.as_view(), name="login"),
    path("dang-xuat/", SignOutView.as_view(), name="logout"),
    path("dang-ky/", RegisterView.as_view(), name="register"),
]
