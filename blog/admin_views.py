from django.shortcuts import render, get_object_or_404, redirect
from .models import Tag, Post, User
from .forms import PostForm, TagForm
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import random
import string

def index(request):
    return redirect("/dashboard/posts")

def randomID(num = 8):
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choices(characters, k = num))
    return random_string

def post_index(request):
    posts = Post.objects.all()
    return render(request, 'admin/post/index.html', {'posts': posts})

def create_post(request):
    if request.method == "POST":
            form = PostForm(request.POST, request.FILES)
        # if form.is_valid():
            post = form.save(commit=False)
            # post.author = request.user
            post.author = User.objects.get(id=1)
            post.url = post.title.replace(" ", "-").lower() + "-" + randomID()
            post.save()
            tag_names = form.cleaned_data['tag_names'].split(',')  # Tách các tag thành danh sách
            for tag_name in tag_names:
                tag, created = Tag.objects.get_or_create(name=tag_name.strip().upper())
                post.tags.add(tag)

            messages.success(request, "%s successfully saved." % post.title)
            return redirect("/dashboard/posts")
    else:
        form = PostForm()
        context = {"form": form, "title": "Post Form"}
    return render(request, "admin/post/form.html", context)

def update_post(request, post_id):
    post = Post.objects.get(id=post_id)
    form = PostForm(initial={"title": post.title, "description": post.description, "thumbnail": post.thumbnail, "id": post.id, "tag_names": ", ".join([tag.name for tag in post.tags.all()])})
    thumbnail = post.thumbnail.url
    if request.method == "POST":
                    form = PostForm(request.POST, request.FILES, instance=post)
                    post = form.save(commit=False) 
                    tag_names = form.cleaned_data['tag_names'].split(',')
                    post.tags.clear()
                    for tag_name in tag_names:
                        tag, created = Tag.objects.get_or_create(name=tag_name.strip().upper())
                        post.tags.add(tag)

                    post.save()
                    messages.success(request, "Post with id %s successfully updated." % post.id)
                    return redirect('/dashboard/posts')  
    
    return render(request, "admin/post/form.html", {"form": form, "thumbnail": thumbnail})


def published_post(request, post_id, is_published):
    post = get_object_or_404(Post, id=post_id)
    if is_published == 'True':
        post.published = True
        post.save()
    else:
        post.published = False
        post.save()
        
    return redirect("/dashboard/posts")

def delete_post(request, post_id):
    post = Post.objects.get(id=post_id)
    try:
        post.delete()
    except:
        pass
    messages.success(request, "Post with id %s successfully deleted." % post_id)
    return redirect('/dashboard/posts')

def tag_index(request):
    tags = Tag.objects.all().order_by('id')
    return render(request, 'admin/tag/index.html', {'tags': tags})


def create_tag(request):
    if request.method == "POST":
            form = TagForm(request.POST)
            if form.is_valid():
                    tag = form.save(commit=False)
                    tag.name = tag.name.upper()
                    tag.save()
                    messages.success(request, "%s successfully saved." % tag.name)
            else:
                    messages.error(request, "Tag name '%s' already exists." % request.POST.get("name"), extra_tags="danger")
            
            return redirect("/dashboard/tags")
    else:
        form = TagForm()
        context = {"form": form, "title": "Tag Form"}

    return render(request, "admin/tag/form.html", context)

def update_tag(request, id):
    tag = Tag.objects.get(id=id)
    form = TagForm(initial={"name": tag.name, "id": tag.id})
    if request.method == "POST":
            form = TagForm(request.POST, instance=tag)
            if form.is_valid():  
                    form.save() 
                    model = form.instance
                    messages.success(request, "Tag with id %s successfully updated." % model.id)
                    return redirect('/dashboard/tags')  
            else:
                    messages.error(request, "Tag name '%s' already exists." % request.POST.get("name"), extra_tags="danger")
                    return redirect("/dashboard/tags")

    return render(request, "admin/tag/form.html", {"form": form})

def delete_tag(request, id):
    tag = Tag.objects.get(id=id)
    try:
        tag.delete()
    except:
        pass
    messages.success(request, "Tag with id %s successfully deleted." % id)
    return redirect('/dashboard/tags')