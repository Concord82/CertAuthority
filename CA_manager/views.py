from django.shortcuts import render
from django.utils.encoding import force_text, force_bytes
from .models import *
from .forms import UploadCertFileForm

# Create your views here.


def test(request):
    if request.method == 'POST':
        form = UploadCertFileForm(request.POST, request.FILES)
        if form.is_valid():
            print(request.POST['title'])

            handle_uploaded_file(request.FILES['file'], request.POST['title'])
            form = UploadCertFileForm()

    else:
        form = UploadCertFileForm()

    return render(request, 'ca_view.html', {'form':form})


def handle_uploaded_file(f, password):
    for chunk in f.chunks():
        loaded_file = loaded_file + chunk
        print(password)
        print(loaded_file)

