from django.shortcuts import render
from . import forms
from . import models
from django.http import Http404
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from braces.views import SelectRelatedMixin
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from groups.models import Group,GroupMember
from .models import Post
# Create your views .
class PostList(SelectRelatedMixin,generic.ListView):
    model = models.Post
    template_name = 'posts/post_list.html'
    context_object_name = 'post_all'
    select_related = ('user','group')

    def user_groups(self):
        return Group.objects.filter(user = self.request.user)

class UserPostList(LoginRequiredMixin,generic.ListView):
    model = models.Post
    template_name = 'posts/user_post_list.html'
    referenced_user = None

    def get_queryset(self):
            try:
                self.referenced_user = self.kwargs.get('username')
                #self.post_user = User.objects.prefetch_related('posts').get(username__iexact = self.kwargs.get('username'))
            except :
                raise Http404
            else:
                return Post.objects.filter(user__username__iexact = self.referenced_user)


    def post_user(self):
        return Post.objects.filter(user__username__iexact = self.referenced_user.username)




class PostDetail(SelectRelatedMixin,generic.DetailView):
    model = models.Post
    select_related = ('user','group')

    def get_queryset(self):
        queryset = super().queryset()
        return queryset.filter(user__username__iexact = self.kwargs.get('username'))

class CreatePost(LoginRequiredMixin,SelectRelatedMixin,generic.CreateView):
    model = models.Post
    fields = ('message','group')
    template_name = 'posts/post_form.html'
    def form_valid(self,form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        sel.object.save()
        return super().form_valid(form)

class DeletePost(LoginRequiredMixin,SelectRelatedMixin,generic.DeleteView):
    model = models.Post
    select_related = ('user','group')
    success_url = reverse_lazy('posts:all')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id = self.request.user.id)

    def delete(self,*args,**kwargs):
        messages.success(self.request,'Post Deleted')
        return super().delete(*args,**kwargs)
