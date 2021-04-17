from django.db import models
from django.utils.text import slugify
# Create your models here.
from django.contrib.auth.models import User

import misaka
from django.urls import reverse
from django import template
register = template.Library()




class Group(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(allow_unicode=True,unique = True)
    description = models.TextField(null=True,default = '')
    description_html = models.TextField(editable=False,null = True,default = '')
    user = models.ManyToManyField(User,through='GroupMember')


    def __str__(self):
        return self.name

    def save(self,*args,**kwargs):
        self.slug = slugify(self.name)
        self.description_html = misaka.html(self.description)
        super().save(*args,**kwargs)

    def get_absolute_url(self):
        return reverse('groups:single',kwargs={'slug':self.slug})



    class Meta:
        ordering = ['name']

class GroupMember(models.Model):
    group = models.ForeignKey(Group,related_name='members',on_delete=models.CASCADE)
    user = models.ForeignKey(User,related_name='user_groups',on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


    class Meta:
        unique_together = ['group','user']
