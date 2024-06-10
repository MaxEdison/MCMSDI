import requests
import random
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.conf import settings
from .models import Image, Article, Person

def homepage(request):
    return render(request, 'homepage.html')

def image_list(request):
    category = request.GET.get('category')
    images = Image.objects.select_related('photographer')
    
    if category:
        images = images.filter(category=category)
        categories = Image.objects.values_list('category', flat=True).distinct()
    else:
        categories = Image.objects.values_list('category', flat=True).distinct()
    
    return render(request, 'image_list.html', {'images': images, 'categories': categories, 'selected_category': category})

def article_list(request):
    category = request.GET.get('category')
    articles = Article.objects.select_related('writer')

    if category:
        articles = articles.filter(category=category)
        categories = Article.objects.values_list('category', flat=True).distinct()
    else:
        categories = Article.objects.values_list('category', flat=True).distinct()
    
    return render(request, 'article_list.html', {'articles': articles, 'categories': categories, 'selected_category': category})

def photographer_list(request):
    photographers = Person.objects.all()
    return render(request, 'photographer_list.html', {'photographers': photographers})

def writer_list(request):
    writers = Person.objects.all()
    return render(request, 'writer_list.html', {'writers': writers})

def photographer_images(request, photographer_code):
    photographer = Person.objects.get(id=photographer_code) #<<<<<<related name used here>>>>>>
    images = Image.objects.filter(photographer=photographer)
    return render(request, 'photographer_images.html', {'photographer': photographer, 'images': images})

def writer_articles(request, writer_code):
    writer = Person.objects.get(id=writer_code) #<<<<<<related name used here>>>>>>
    articles = Article.objects.filter(writer=writer)
    return render(request, 'writer_articles.html', {'writer': writer, 'articles': articles})


def update_data(image):
    headers = {'Authorization': f'Bearer {settings.PHOTOTAG_API_KEY}',}

    payload = {
    "language": "en",
    "singleWordKeywordsOnly": True
    }

    img = requests.get(image.image_path)

    files = [
        ('file', img.content)
    ]

    response = requests.request("POST",
                                settings.PHOTOTAG_API_URL,
                                headers=headers,
                                data=payload,
                                files=files)
    
    if response.status_code == 200:
        metadata = response.json()
        print(metadata)
        print(metadata['data']['title'])
        image.title = metadata['data']['title']
        image.tags = random.choice(metadata['data']['keywords']) #Not tested yet! Beta version!!!
        image.descr = metadata['data']['description']
        image.save()
        return True
    return False

def api_req(request, image_id):
    if request.method == 'POST':
        image = get_object_or_404(Image, pk=image_id)
        if update_data(image):
            messages.success(request, 'Metadata updated successfully.')
        else:
            messages.error(request, 'Failed to update metadata.')
    return redirect('image_list')