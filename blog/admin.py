from django.contrib import admin

# Register your models here.
# blog/admin.py
from blog.models import User, Tag, Post

class UserAdmin(admin.ModelAdmin):
    pass
class TagAdmin(admin.ModelAdmin):
    pass
class PostAdmin(admin.ModelAdmin):
    pass

admin.site.register(User, UserAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Post, PostAdmin)