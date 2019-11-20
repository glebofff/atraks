# -*- coding: utf-8 -*-
#
# Author: Stanislav Glebov <glebofff@gmail.com> 
# Created: 20/11/19
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:number>', views.CheckView.as_view(), name='check')
]