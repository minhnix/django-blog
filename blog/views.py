from django.shortcuts import render, get_object_or_404, redirect
from .models import Tag, Post, User, Comment
from .forms import PostForm, SimpleForm, CommentForm
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.http import JsonResponse

def index(request):
	return render(request, 'index.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Tài khoản hoặc mật khẩu không đúng")
            return redirect("/login")

    return render(request, 'login.html')

def logout_f(request):
    logout(request)
    return redirect('/')


def tag_index(request):
	tags = Tag.objects.raw('''
                        SELECT t.id, t.name, COUNT(bp.id) AS count
    FROM blog_tag t
    LEFT JOIN blog_post_tags bpt ON t.id = bpt.tag_id
    LEFT JOIN blog_post bp ON bpt.post_id = bp.id AND bp.published = 1
    GROUP BY t.id, t.name
''')
	return render(request, 'tag_index.html', {'tags': tags})

def tag_detail(request, tag_name):
	tag = Tag.objects.get(name=tag_name)
	posts_with_tag = tag.posts.filter(published=True).order_by('-created_on').select_related('author').prefetch_related('tags')

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
    posts = Post.objects.all().select_related('author').prefetch_related('tags').filter(published=True).order_by('-created_on')
    data = []

    for post in posts:
        tags = post.tags.all()  # Lấy tất cả các tags liên quan đến bài viết
        tag_names = [tag.name for tag in tags]  # Tạo danh sách tên các tag (use tag.name instead of tag)

        post_info = {
            'id': post.id,
            'title': post.title,
            'created_on': post.created_on,
            'author': post.author.username,
            'tags': tag_names,  # Sử dụng danh sách tên các tag
            'thumbnail': post.thumbnail.url if post.thumbnail else '',
        }
        
        print(post_info['tags'])  # Access the tags using the dictionary key
        data.append(post_info)

    context = {
        'posts': data,
    }

    return render(request, 'bootstrap/post_index.html', {'data': context})

def post_detail(request, post_id):
    
    posts_query = Post.objects.filter(published=True).order_by('-created_on').select_related('author').prefetch_related('tags')
    post = get_object_or_404(posts_query, id=post_id)

    # print(post.tags)
    comments = post.comments.filter(parent__isnull=True)
    new_comment = None

    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        print(request.POST)
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            parent_id = comment_form.cleaned_data.get('parent_id')
            if parent_id:
                new_comment.parent = Comment.objects.get(id=parent_id)
            new_comment.save()

            return JsonResponse({
                'id': new_comment.id,
                'content': new_comment.content,
                'created_on': new_comment.created_on.strftime('%Y-%m-%d %H:%M:%S'),
                'parent_id': new_comment.parent.id if new_comment.parent else None,
                'post_id': new_comment.post.id,
            })

    comment_form = CommentForm()

    context = {"post": post,
                "author": post.author,
                "tags": post.tags.all(),
                'new_comment': new_comment,
                'comment_form': comment_form,
                'comments': comments,
    }
    
    # print(context.post.tags)
    
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