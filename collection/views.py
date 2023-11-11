from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.template.loader import render_to_string
from django.contrib.postgres import search 
from django.core.paginator import Paginator
import random
from .models import Artwork, Collection
from .forms import CollectionForm


def search_artworks(request):
    query_param = request.GET.get('q', '')
    artworks = []

    if query_param:
        vector = (
            search.SearchVector("title", weight="A")
            + search.SearchVector("author__name", weight="B")
            + search.SearchVector("style__name", weight="C")
            + search.SearchVector("genre__name", weight="C")
        )
        query = search.SearchQuery(query_param, search_type="websearch")
        artworks = (
            Artwork.objects.annotate(
                search=vector,
                rank=search.SearchRank(vector, query),
            )
            .filter(search=query)
            .order_by("-rank")
        )

        paginator = Paginator(artworks, 3)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        return render(request, 'collection/artwork_search.html', {'artworks': artworks, 'search_value': query_param, "page_obj": page_obj})
    else:
        return render(request, 'collection/index.html', {'artworks': [], 'search_value': None})

    
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


def collections(request):
    collections = Collection.objects.filter(owner=request.user)
    return render(request, 'collection/collections.html',
                  {'collections': collections})
    
def collection_list(request):
    collections = Collection.objects.filter(owner=request.user)
    return render(request, 'collection/collection_list.html',
                  {'collections': collections})
    
def collection_add(request):
    form = None
    if request.method == 'POST':
        form = CollectionForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            collection = Collection(
                    name=name,
                    description=description,
                    owner=request.user)
            collection.save()
            return HttpResponse(status=204,
                                headers={'HX-Trigger': 'listChanged'})

    return render(request,
                  'collection/collection_form.html',
                  {'form': form})