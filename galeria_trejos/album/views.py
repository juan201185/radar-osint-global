from django.shortcuts import render
from .models import Foto

def galeria(request):
    fotos = Foto.objects.all().order_by('-fecha')
    return render(request, 'album/index.html', {'fotos': fotos})