from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View

from .forms import RegisterForm, StyledAuthForm


class SignInView(LoginView):
    template_name = "accounts/login.html"
    authentication_form = StyledAuthForm
    redirect_authenticated_user = True


class SignOutView(LogoutView):
    next_page = reverse_lazy("accounts:login")


class RegisterView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect("dashboard:home")
        return render(request, "accounts/register.html", {"form": RegisterForm()})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("dashboard:home")
        return render(request, "accounts/register.html", {"form": form})
