from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
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
<<<<<<< HEAD
    artworks = list(Artwork.objects.all())
    random_works = []
    if artworks:
        random_works = random.sample(artworks, 12)

    return render(request, 'collection/index.html', {'artworks': random_works})
=======
    # Obtiene todas las obras de arte
    artworks = list(Artwork.objects.all())
    random_artwork = []
    # Selecciona una obra de arte al azar
    if artworks:
        random_artwork = random.sample(artworks, 12)
    return render(request, 'collection/index.html', {'random_artwork': random_artwork})
>>>>>>> 7319c5da81f72dc190835af6321b03b6d1a6cee3
