from django.shortcuts import render

# Create your views here.


def index(request):
    return render(request, 'index.j2')

def verify(request):
    return render(request, 'verify.j2')
