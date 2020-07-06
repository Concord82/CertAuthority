from django.shortcuts import render, redirect
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, logout,  login as auth_login
# Create your views here.


def login(request):
    if request.user.is_authenticated:
        logout(request)
    else:
        username = request.POST['username']
        password = request.POST['password']
        print(username, password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
        else:
            raise PermissionDenied
            #return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def test(request):
    return render(request, "_base.html")
