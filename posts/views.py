from django.shortcuts import render, redirect, get_object_or_404
from .forms import PostForm, CommentForm
from .models import HashTag, Post, Comment
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

# Create your views here.


def index(request):
    posts = Post.objects.all()
    # 한페이지에 몇개를 보여줄지
    paginator = Paginator(posts, 5) 

    page = request.GET.get('page')
    posts = paginator.get_page(page)

    comment_form = CommentForm()
    context = {
        'posts': posts,
        'comment_form': comment_form,
    }
    return render(request, 'posts/index.html', context)

@login_required
def create(request):
    if request.method == 'POST':
        # 이미지파일은 request.FILES안에 들어있다.
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            # post object (None) 상태
            post.save()
            # post object 생성된 상태 -> 해시태그 추가
            for word in post.content.split():
                if word.startswith('#'): # word[0] == '#'과 동일
                    # get_or_create() 해당객체가 있으면 가져오고 없으면 생성한다.
                    # hashtag, created = HashTag.objects.get_or_create(content=word) # (obj, True or False) 튜플 반환
                    hashtag = HashTag.objects.get_or_create(content=word)[0] # obj만 가져오겠다.
                    post.hashtags.add(hashtag)
            return redirect(request.GET.get('next') or 'posts:index')
    else:
        form = PostForm()
    context = {
        'form': form
    }
    return render(request, 'posts/form.html', context)

def hashtags(request, id):
    hashtag = get_object_or_404(HashTag, id=id)
    posts = hashtag.taged_post.all
    context = {
        'posts': posts
    }
    return render(request, 'posts/index.html', context)

@login_required
def like(request, id):
    post = get_object_or_404(Post, id=id)
    user = request.user
    if user in post.like_users.all():
        post.like_users.remove(user)
    else:
        post.like_users.add(user)
    return redirect(request.GET.get('next') or 'posts:index')

@login_required
def update(request, id):
    post = get_object_or_404(Post, id=id)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save()
            post.hashtags.clear()
            for word in post.content.split():
                if word.startswith('#'):
                    hashtag = HashTag.objects.get_or_create(content=word)[0]
                    post.hashtags.add(hashtag)
            return redirect('posts:index')
    else:
        form = PostForm(instance=post)
    context = {
        'form': form
    }
    return render(request, 'posts/form.html', context)

@login_required
def delete(request, id):
    post = get_object_or_404(Post, id=id)
    post.delete()
    return redirect('posts:index')

@login_required
def comment_create(request, id):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            form.save()
    return redirect('posts:index')