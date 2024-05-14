from django.shortcuts import render, get_object_or_404, redirect
from .models import Tag, Post, User
from .forms import PostForm, SimpleForm
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def index(request):
	return render(request, 'index.html')

def tag_index(request):
	tags = Tag.objects.raw('''Select t.id, name, count(name) as count
						from blog_tag t left join blog_post_tags pt 
						on t.id = pt.tag_id group by t.id, name''')
	return render(request, 'tag_index.html', {'tags': tags})

def tag_detail(request, tag_name):
	tag = Tag.objects.get(name=tag_name)
	posts_with_tag = tag.posts.all()

	posts_data = []
	for post in posts_with_tag:
		post_info = {
            'id': post.id,
            'title': post.title,
			'created_on': post.created_on,
			'author': post.author.username,
            'thumbnail': post.thumbnail.url if post.thumbnail else '',
            'tags': post.tags.all(),
        }
		posts_data.append(post_info)

	data = {
        'tag_id': tag.id,
        'tag_name': tag.name,
        'posts': posts_data,
    }
    
	return render(request, 'tag_detail.html', {'data': data})

def post_index(request):
    posts = Post.objects.all().select_related('author').prefetch_related('tags')
    
    data = []
    for post in posts:
        author = post.author  
        tags = post.tags.all() 
        
        blog = {
            'post': post,
            'author': author,
            'tags': tags,
        }
        
        data.append(blog)
    print(data)
    theme = getattr(settings, "MARTOR_THEME", "bootstrap")
    return render(request, "%s/post_index.html" % theme, {'posts': data})
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    author = get_object_or_404(User, id=post.author_id)

    context = {"post": post,
               "author": author}
    
    theme = getattr(settings, "MARTOR_THEME", "bootstrap")
    return render(request, "%s/post_detail.html" % theme, context)

def create_post(request):
	return render(request, '../templates/boostrap/form.html')

def home_redirect_view(request):
    return redirect("simple_form")


def simple_form_view(request):
    form = SimpleForm()
    context = {"form": form, "title": "Simple Form"}
    theme = getattr(settings, "MARTOR_THEME", "bootstrap")
    return render(request, "%s/form.html" % theme, context)


@login_required
def post_form_view(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, "%s successfully saved." % post.title)
            return redirect("test_markdownify")
    else:
        form = PostForm()
        context = {"form": form, "title": "Post Form"}
    theme = getattr(settings, "MARTOR_THEME", "bootstrap")
    return render(request, "%s/form.html" % theme, context)


def test_markdownify(request):
    post = Post.objects.last()
    context = {"post": post}
    if post is None:
        context = {
            "post": {
                "title": "Fake Post",
                "description": """It **working**! :heart: [Python Learning](https://scontent.fsgn2-4.fna.fbcdn.net/v/t39.30808-6/277106760_1413085885787585_2033900011375700155_n.jpg?_nc_cat=101&ccb=1-7&_nc_sid=5f2048&_nc_ohc=0ECruOAvUKwQ7kNvgEouxZ7&_nc_ht=scontent.fsgn2-4.fna&oh=00_AfAE3plTT61n1BEPjgvYvFRs5TCKFxONSZhTw-VXBOMsQQ&oe=663AADAA)""",
            }
        }
    theme = getattr(settings, "MARTOR_THEME", "bootstrap")
    return render(request, "%s/test_markdownify.html" % theme, context)