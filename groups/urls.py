from django.contrib import admin
from django.urls import path
from . import views

app_name = 'groups'

urlpatterns = [
    path('',views.GroupList.as_view(),name='all'),
    path('new/',views.CreateGroup.as_view(),name='new'),
    path('posts/in/<slug:slug>/',views.GroupDetail.as_view(),name='single'),
    path('join/<slug:slug>/',views.JoinGroup.as_view(),name='join'),
    path('leave/<slug:slug>/',views.LeaveGroup.as_view(),name='leave'),
]
