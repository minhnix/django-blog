from django.contrib import admin

# Register your models here.
# blog/admin.py
from blog.models import User

class UserAdmin(admin.ModelAdmin):
    pass
admin.site.register(User, UserAdmin)