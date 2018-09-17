from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^about$', views.about),
    url(r'^how_it_works$', views.how),
    url(r'^login$', views.login),
    url(r'^register$', views.register),
    url(r'^shelter$', views.shelter),
    url(r'^registeruser$', views.registerUser),
    url(r'^loginuser$', views.loginUser),
    url(r'^loginshelter$', views.loginShelter),
    url(r'^play$', views.play),
    url(r'^logout$', views.logout),
    url(r'^shelter/home$', views.shelterHome),
    url(r'^registeranimal$', views.registerAnimal),
    url(r'^like$', views.like),
    url(r'^dislike$', views.dislike),
]