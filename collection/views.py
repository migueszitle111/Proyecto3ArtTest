from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.template.loader import render_to_string
import random
from random import choice  
from .models import Artwork


def search(request):
    query = request.GET.get('q', '')

    if query:
        artworks = Artwork.objects.annotate(
            search=SearchVector('title', 'author__name', 'style__name', 'genre__name')
        ).filter(search=SearchQuery(query))

        artworks = artworks.annotate(
            rank=SearchRank(SearchVector('title', 'author__name', 'style__name', 'genre__name'), SearchQuery(query))
        ).order_by('-rank')

    else:
        artworks = Artwork.objects.all()

    return render(request, 'collection/index.html', {'artworks': artworks, 'query': query})


def register(request):
    if request.method == 'POST':
        f = UserCreationForm(request.POST)
        if f.is_valid():
            f.save()
            username = f.cleaned_data.get('username')
            raw_password = f.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)

            return HttpResponseRedirect('/')

    else:
        f = UserCreationForm()

    return render(request, 'registration/registration_form.html', {'form': f})

def artwork(request, artwork_id):

    artwork = Artwork.objects.get(pk=artwork_id)

    return render(request, 'collection/artwork.html', {'artwork': artwork})

def index(request):
    artworks = list(Artwork.objects.all())
    random_works = []
    if artworks:
        random_works = random.sample(artworks, 12)
    return render(request, 'collection/index.html', {'artworks': random_works})

def random_artworks(request):
    artworks = list(Artwork.objects.all())
    random_works = []
    if artworks:
        random_works = random.sample(artworks, 24)
    return render(request, 'collection/artworks_random.html', {'artworks': random_works})