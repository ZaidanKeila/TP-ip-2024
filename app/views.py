# capa de vista/presentación

from django.shortcuts import redirect, render
from .layers.services import services
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.core.paginator import Paginator 

def index_page(request):
    return render(request, 'index.html')

# esta función obtiene 2 listados que corresponden a las imágenes de la API y los favoritos del usuario, y los usa para dibujar el correspondiente template.
# si el opcional de favoritos no está desarrollado, devuelve un listado vacío.
def home(request, page=1):
    images = services.getAllImages()
    favourite_list = services.getAllFavourites(request)
    paginator = Paginator (images, per_page=20) #crea un objeto para manejar la paginación
    page_object = paginator.get_page(page) #recupera la pagina especifica solicitada por el usuario y page se utiliza para determinar que pagina buscar 
    context = {'page_object': page_object} #crea un diccionario de contecto, incluye page_object que contiene la info sobre la pagina actual, el total de paginas y las imagenes de esa pagina en especifico 

    #pasa las imagenes, favoritos y diccionario de contexto, pasando los datos necesarios para mostrar imagenes, favoritos y controles de paginacion
    return render(request, 'home.html', { 'images': images, 'favourite_list': favourite_list, 'context': context})

def search(request,page=1):
    search_msg = request.POST.get('query', '')

    # si el texto ingresado no es vacío, trae las imágenes y favoritos desde services.py,
    # y luego renderiza el template (similar a home).
    if (search_msg != ''):
        images = services.getAllImages(search_msg)
        favourite_list = services.getAllFavourites(request)
        paginator = Paginator (images, per_page=20)
        page_object = paginator.get_page(page)
        context = {'page_object': page_object}

        return render(request, 'home.html', { 'images': images, 'favourite_list': favourite_list, 'context': context})
    else:
        return redirect('home')


# Estas funciones se usan cuando el usuario está logueado en la aplicación.
@login_required
def getAllFavouritesByUser(request):
    favourite_list = services.getAllFavourites(request)
    return render(request, 'favourites.html', { 'favourite_list': favourite_list })

@login_required
def saveFavourite(request):
    services.saveFavourite(request)
    favourite_list = services.getAllFavourites(request)
    return redirect('home')

@login_required
def deleteFavourite(request):
    services.deleteFavourite(request)
    favourite_list = services.getAllFavourites(request)
    return render(request, 'favourites.html', { 'favourite_list': favourite_list })

@login_required
def exit(request):
    logout(request)
    return render(request, 'index.html')