from django.contrib import admin
from newspaper.models import Post, Category, Tag,NewsLetter,Contact,Comment
from django_summernote.admin import SummernoteModelAdmin

admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(NewsLetter)
admin.site.register(Contact)


# Apply summernote to content field in Post model.
class PostAdmin(SummernoteModelAdmin):  # instead of ModelAdmin
    summernote_fields = ("content",)
    list_display = ("title", "category", "author", "created_at")
    date_hierarchy = "published_at"


admin.site.register(Post, PostAdmin)