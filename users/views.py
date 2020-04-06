import os
import requests
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.shortcuts import redirect, reverse
from django.contrib.auth import authenticate, login, logout
from . import forms, models

# Create your views here.


class LoginView(FormView):

    template_name = "users/login.html"
    form_class = forms.LoginForm
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):

        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")

        user = authenticate(self.request, username=email, password=password)

        if user is not None:
            login(self.request, user)

        return super().form_valid(form)


def log_out(request):
    logout(request)
    return redirect(reverse("core:home"))


class SignUpView(FormView):

    template_name = "users/signup.html"
    form_class = forms.SignUpForm
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):

        form.save()

        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")

        user = authenticate(self.request, username=email, password=password)

        if user is not None:
            login(self.request, user)

        user.verify_email()

        return super().form_valid(form)


def complete_verification(request, key):

    try:
        user = models.User.objects.get(email_secret=key)
        user.email_verified = True
        user.email_secret = ""
        user.save()
        # 성공 메세지 추가
    except models.User.DoesNotExist:
        # 에러 메세지 추가
        pass

    return redirect(reverse("core:home"))


# OAuth를 사용하는 플랫폼이면 이 형식을 사용하여 로그인을 할 수 있게 만들 수 있음


def github_login(request):

    client_id = os.environ.get("GH_ID")  # github id
    redirect_uri = "http://127.0.0.1:8000/users/login/github/callback"

    return redirect(
        f"https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&scope=read:user"
    )


def github_callback(request):

    client_id = os.environ.get("GH_ID")
    client_secret = os.environ.get("GH_SECRET")

    code = request.GET.get("code")

    if code is not None:
        result = requests.post(
            f"https://github.com/login/oauth/access_token?client_id={client_id}&client_secret={client_secret}&code={code}",
            headers={"Accept": "application/json"},
        )
        result_json = result.json()
        error = result_json.get("error", None)

        if error is not None:
            return redirect(reverse("users:login"))  # 에러가 생기면 이곳으로 감
        else:
            access_token = result_json.get("access_token")
            profile_request = requests.get(
                "https://api.github.com/user",
                headers={
                    "Authorization": f"token {access_token}",
                    "Accept": "application/json",
                },
            )
            profile_json = profile_request.json()
            username = profile_json.get("login", None)

            if username is not None:
                name = profile_json.get("name")
                email = profile_json.get("email")
                bio = profile_json.get("bio")

                user = models.User.objects.get(email=email)

                if user is not None:
                    return redirect(
                        reverse("users:login")
                    )  # 이미 그 email을 가진 user가 있으면 수행
                else:
                    user = models.User.objects.create(
                        username=email, first_name=name, bio=bio, email=email
                    )
                    login(request, user)

                    return redirect(reverse("core:home"))
            else:
                return redirect(reverse("users:login"))
    else:
        return redirect(reverse("core:home"))
