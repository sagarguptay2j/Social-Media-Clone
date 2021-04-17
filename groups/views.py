from django.shortcuts import render
from django.urls import reverse
from  groups.models import Group,GroupMember
from django.contrib import messages
from django.shortcuts import get_object_or_404
# Create your views here.
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin



class GroupList(generic.ListView):
    model = Group

class GroupDetail(generic.DetailView):
    model = Group

    def check(self):
        for oneuser in self.object.user.all():
            if oneuser.username == self.request.user.username:
                return True
        return False

class CreateGroup(LoginRequiredMixin,generic.CreateView):
    fields = ('name','description')
    model = Group


class JoinGroup(LoginRequiredMixin,generic.RedirectView):
    def get_redirect_url(self,*args,**kwargs):
        return reverse('groups:single',kwargs={'slug':self.kwargs.get('slug')})

    def get(self,request,*args,**kwargs):
        group = get_object_or_404(Group,slug=self.kwargs.get('slug'))
        try:
            GroupMember.objects.create(user=self.request.user,group=group)
        except:
            messages.warning(self.request,'Already a user')
        else:
            messages.success(self.request,'Successfully joined')

        return super().get(request,*args,**kwargs)

class LeaveGroup(LoginRequiredMixin,generic.RedirectView):
    def get_redirect_url(self,*args,**kwargs):
        return reverse('groups:single',kwargs={'slug':self.kwargs.get('slug')})

    def get(self,request,*args,**kwargs):

        try:
            membership = GroupMember.objects.filter(user=self.request.user,group__slug=self.kwargs.get('slug'))
        except:
            messages.warning(self.request,'You are not a member of this group')
        else:
            membership.delete()
            messages.success(self.request,'Successfully left the group')

        return super().get(request,*args,**kwargs)
