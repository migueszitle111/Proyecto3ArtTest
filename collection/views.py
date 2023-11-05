from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank

from random import choice  
from .models import Artwork

def search(request):
    query = request.GET.get('q', '')

    if query:
        artworks = Artwork.objects.annotate(
            search=SearchVector('title', 'author__name', 'style__name', 'genre__name')
        ).filter(search=SearchQuery(query))

        # Puedes ordenar los resultados por relevancia si lo deseas
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


def index(request):
    # Obtiene todas las obras de arte
    artworks = Artwork.objects.all()
    # Selecciona una obra de arte al azar
    random_artwork = choice(artworks)
    return render(request, 'collection/index.html', {'random_artwork': random_artwork})
