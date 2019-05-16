from django.shortcuts import HttpResponseRedirect


def user_permission(function):
    def wrap(request, *args, **kwargs):
        print(request.user,"$$$$$$$$$$$$$$$$$")
        if request.user.is_anonymous():
            return HttpResponseRedirect("/login/")
        if request.user.is_super_user:
                return function(request,*args,**kwargs)
        elif request.user.is_operator:
                return HttpResponseRedirect("/operatorpage/")
        elif request.user.is_company:
                return HttpResponseRedirect("/customerpage/")



    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap



def is_operator(function):
    def wrap(request, *args, **kwargs):
        print(request.user,"$$$$$$$$$$$$$$$$$")
        if request.user.is_anonymous():
            return HttpResponseRedirect("/login/")
        if request.user.is_operator:
                return function(request,*args,**kwargs)
        elif request.user.is_super_user:
                 return HttpResponseRedirect("/operatorlist/")
        elif request.user.is_company:
                return HttpResponseRedirect("/customerpage/")

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap


def is_company(function):
    def wrap(request, *args, **kwargs):
        print(request.user,"$$$$$$$$$$$$$$$$$")
        if request.user.is_anonymous():
            return HttpResponseRedirect("/login/")
        if request.user.is_company:
            return function(request, *args, **kwargs)
        elif request.user.is_operator:
                return HttpResponseRedirect("/operatorpage/")
        elif request.user.is_super_user:
                return HttpResponseRedirect("/operatorlist/")

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
