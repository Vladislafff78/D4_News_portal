from django.contrib import admin
from .models import Post, Comment


class PostAdmin(admin.ModelAdmin):
    list_display = (id, 'post_title', 'post_date', 'post_photo')
    list_display_links = (id, 'post_title')
    search_fields = ('post_title', 'post_text')


admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
