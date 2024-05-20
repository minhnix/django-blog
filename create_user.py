import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'personal_blog.settings')
django.setup()

from blog.models import User

def create_user(username, password, email=None):
    user = User.objects.create_user(username=username, password=password, email=email)
    print(f'User {username} created successfully!')

# Tạo user
create_user('admin', 'admin', 'admin@example.com')
