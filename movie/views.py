from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home(request):
    #return HttpResponse("<h1>Movie Reviews Home Page</h1>")
    #return render(request, 'home.html')
    return render(request, 'home.html', {'name': 'Juanes'})
def about(request):
    return HttpResponse("<h1>About Movie Reviews</h1>")