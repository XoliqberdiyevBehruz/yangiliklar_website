from django.contrib import admin
from .models import News, Cotegory, Cantact, Comment
# Register your models here.

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'publish_time', 'status', 'cotegory']
    list_filter = ['status', 'create_time', 'publish_time']
    prepopulated_fields = {"slug":('title',)}
    date_hierarchy = 'publish_time'
    search_fields = ['title', 'body']
    ordering = ['publish_time', 'status']

   

@admin.register(Cotegory)
class CotegoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    
admin.site.register(Cantact)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'body', 'created_time', 'active']
    list_filter = ['created_time', 'active']
    search_fields = ['user', 'body']
