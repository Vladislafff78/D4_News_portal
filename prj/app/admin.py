from django.contrib import admin
from .models import *


class PostAdmin(admin.ModelAdmin):
    list_display = (id, 'type_category', 'post_title', 'post_date', 'post_photo')
    list_display_links = (id, 'post_title')
    search_fields = ('post_title', 'post_text')


admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
