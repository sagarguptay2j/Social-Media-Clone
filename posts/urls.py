from django.urls import path
from . import views


app_name = 'posts'

urlpatterns = [
    path('',views.PostList.as_view(),name='all'),
    path('<str:username>/',views.UserPostList.as_view(),name='for_user'),
    path('new/',views.CreatePost.as_view(),name='new'),
    path('<str:username>/<int:pk>/',views.PostDetail.as_view(),name='single'),
    path('delete/<int:pk>/',views.DeletePost.as_view(),name='all'),
]
