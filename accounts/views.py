from django.contrib.auth import (
     authenticate,
     get_user_model,
     login,
     logout
)
from django.shortcuts import render, redirect
from .forms import UserLoginForm, UserRegisterForm


def login_view(request):
    next = request.GET.get("next")
    title = "Login"
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username=username, password=password)  # check the user is exist
        login(request, user)
        if next:
            return redirect(next)  # after login go the next page
        redirect("/")
    context = {
        "form": form,
        "title":title
    }
    return render(request, "account_form.html", context)


def register_view(request):
    next = request.GET.get("next")
    title = "Register"
    form = UserRegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data.get("password")
        user.set_password(password)
        user.save()
        new_user = authenticate(username=user.username, password=password)
        login(request, new_user)
        if next:
            return redirect(next)  # after register go the next page
        redirect("/")
    context = {
        "title": title,
        "form": form
    }
    return render(request, "account_form.html", context)


def logout_view(request):
    logout(request)
    return redirect("/")
    # return render(request, "account_form.html", {})
