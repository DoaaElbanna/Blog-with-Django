from django.contrib import admin
from .models import Post


class PostModelAdmin(admin.ModelAdmin):
    list_display = ["__str__", "timestamp", "updated"]
    list_display_links = ["timestamp"]  # field be linked
    list_filter = ["timestamp", "updated"]  # field can filter by it
    search_fields = ["title", "content"]  # searchable fields

    class Meta:
        model = Post


admin.site.register(Post, PostModelAdmin)






















