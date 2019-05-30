from django.contrib import admin
from .models import Post, Category

# Register your models here.


class CategoryOption(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug', ]
    prepopulated_fields = {'slug' : ('name', )}


admin.site.register(Category, CategoryOption)



admin.site.register(Post)

