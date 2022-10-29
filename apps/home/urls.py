# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.home import views

urlpatterns = [

    # The home page
    path('', views.index, name='home'),
    path('', views.index, name='index'),
    path("folder/<int:folderid>/",views.folder, name="folder"),
    path("addFolder/", views.addfolder, name="addfolder"),
    path("delete/<int:deleteid>/",views.delete, name="delete"),
    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]
