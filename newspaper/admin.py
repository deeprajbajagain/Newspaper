from django.contrib import admin
from newspaper.models import Post, Category, Tag,NewsLetter,Contact,Comment

admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(NewsLetter)
admin.site.register(Contact)
admin.site.register(Comment)
