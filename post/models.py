from django.db import models
from django.contrib.auth import get_user_model

from ckeditor.fields import RichTextField
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=30)
    slug = models.SlugField(max_length=30, db_index=True, unique=True, allow_unicode=True, blank=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='posts')
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=50)
    text = RichTextField()
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title