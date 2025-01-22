from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Topic, Comment, Rating, Category
from .forms import LoginForm, RegisterForm, CommentForm
from django.core.paginator import Paginator

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('homepage')
            else:
                return render(request, 'login.html', {'form': form, 'error': 'Invalid credentials'})
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

@login_required
def homepage(request):
    categories = Category.objects.all()
    topics = Topic.objects.all()
    paginator = Paginator(topics, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'homepage.html', {'categories': categories, 'page_obj': page_obj})

@login_required
def topic_detail(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    comments = Comment.objects.filter(topic=topic)
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.topic = topic
            comment.user = request.user
            comment.save()
            return redirect('topic_detail', topic_id=topic_id)
    else:
        comment_form = CommentForm()
    return render(request, 'topic_detail.html', {'topic': topic, 'comments': comments, 'comment_form': comment_form})

def logout_view(request):
    logout(request)
    return redirect('login')
