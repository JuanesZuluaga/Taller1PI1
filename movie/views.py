from django.shortcuts import render
from django.http import HttpResponse
import matplotlib.pyplot as plt
import matplotlib
import io
import urllib, base64

from .models import Movie
# Create your views here.

def home(request):
    #return HttpResponse("<h1>Movie Reviews Home Page</h1>")
    #return render(request, 'home.html')
    #return render(request, 'home.html', {'name': 'Juanes Zuluaga'})
    searchTerm = request.GET.get('searchMovie')
    if searchTerm:
        movies = Movie.objects.filter(title__icontains=searchTerm)
    else:
        movies = Movie.objects.all()
    return render(request, 'home.html', {'searchTerm': searchTerm, 'movies': movies})

def about(request):
    return render(request, 'about.html')

def statistics_view(request):
    matplotlib.use('Agg')  # Usar backend no interactivo

    # Obtener todos los géneros de las películas
    genres = Movie.objects.values_list('genre', flat=True)

    # Contar la cantidad de películas por género
    genre_counts = {}

    for genre in genres:
        if genre:  
            first_word = genre.split()[0]  # Tomar solo la primera palabra del género
            genre_counts[first_word] = genre_counts.get(first_word, 0) + 1

    # Definir parámetros para la gráfica
    bar_width = 0.5
    bar_positions = range(len(genre_counts)) 

    # Crear la gráfica de barras
    plt.bar(bar_positions, genre_counts.values(), width=bar_width, align='center')

    # Personalizar la gráfica
    plt.xticks(bar_positions, genre_counts.keys(), rotation=90)
    plt.xlabel("Genre")
    plt.ylabel("Number of movies")
    plt.title("Movies by Genre")
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # Ajustar la separación entre las barras
    plt.subplots_adjust(bottom=0.3)

    # Guardar la imagen en un objeto BytesIO
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    # Convertir la gráfica a base64
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png).decode('utf-8')

    # Renderizar la plantilla con la gráfica
    return render(request, 'statistics.html', {'graphic': graphic})

    """matplotlib.use('Agg')
    years = Movie.objects.values_list('year', flat=True).distinct().order_by('year') 
    movie_counts_by_year = {} 
    for year in years: 
        if year:
            movies_in_year = Movie.objects.filter(year=year)
        else:
            movies_in_year = Movie.objects.filter(year__isnull=True)
            year = "None"
        count = movies_in_year.count()
        movie_counts_by_year[year] = count
    bar_width = 0.5 
    bar_spacing = 0.5 
    bar_positions = range(len(movie_counts_by_year)) 
    plt.bar(bar_positions, movie_counts_by_year.values(), width=bar_width, align='center')
    plt.title('Movies per year')
    plt.xlabel('Year')
    plt.ylabel('Number of movies')
    plt.xticks(bar_positions, movie_counts_by_year.keys(), rotation=90)
    plt.subplots_adjust(bottom=0.3)
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')
    return render(request, 'statistics.html', {'graphic': graphic})
"""
def signup(request):
    email = request.GET.get('email')
    return render(request, 'signup.html', {'email': email})