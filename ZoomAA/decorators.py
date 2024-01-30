from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse


def unauthenticated(viewFunc):
    def wrapperFunc(request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("index"))
        else:
            return viewFunc(request, *args, **kwargs)

    return wrapperFunc


def allowedUsers(allowedRoles=[]):
    def viewpage(viewFunc):
        def wrapperFunc(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            if group in allowedRoles:
                return viewFunc(request, *args, **kwargs)

            else:
                return HttpResponseRedirect(reverse("logout"))

        return wrapperFunc
    return viewpage
