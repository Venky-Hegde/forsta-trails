from django.conf.urls import url,include
from .views import  OverwriteStorage
from django.conf import settings


urlpatterns=[

     url(r'^extract-file/', view = OverwriteStorage.as_view(), name="extract-file"),
]

