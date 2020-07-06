from django.shortcuts import render

from .models import *

# Create your views here.

def test(request):


    return render(request, 'ca_view.html')
