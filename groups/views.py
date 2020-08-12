from django.shortcuts import render

from .models import Category


def index(request):
    roots = Category.objects.filter(parent__id=5)

    return render(request, 'groups/index.html', {
        'roots': list(roots)
    })
