import os
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm

ARTICLES_DIR = 'articles/'

# Utility function to read articles
def read_article(slug):
    try:
        with open(os.path.join(ARTICLES_DIR, f'{slug}.json'), 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        raise Http404("Article not found")

# Utility function to write articles
def write_article(slug, data):
    with open(os.path.join(ARTICLES_DIR, f'{slug}.json'), 'w') as file:
        json.dump(data, file)

# Utility function to get all article slugs
def list_articles():
    return [f.replace('.json', '') for f in os.listdir(ARTICLES_DIR) if f.endswith('.json')]

def home(request):
    articles = list_articles()
    return render(request, 'blog/home.html', {'articles': articles})

def article_detail(request, slug):
    article = read_article(slug)
    return render(request, 'blog/article_detail.html', {'article': article})

def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    articles = list_articles()
    return render(request, 'blog/dashboard.html', {'articles': articles})

@login_required
def add_article(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        date = request.POST.get('date')
        slug = slugify(title)

        write_article(slug, {'title': title, 'content': content, 'date': date})
        return redirect('dashboard')

    return render(request, 'blog/add_article.html')

@login_required
def edit_article(request, slug):
    article = read_article(slug)
    
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        date = request.POST.get('date')
        new_slug = slugify(title)  # Use new slug if the title changes

        write_article(new_slug, {'title': title, 'content': content, 'date': date})
        if new_slug != slug:
            os.remove(os.path.join(ARTICLES_DIR, f'{slug}.json'))  # Remove old file if slug changes
        return redirect('dashboard')

    return render(request, 'blog/edit_article.html', {'article': article})

def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'blog/login.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()  # This saves the user with the hashed password
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'blog/register.html', {'form': form})
