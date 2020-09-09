from django.http import JsonResponse
from django.shortcuts import render

from .models import Category, Group


def index(request, root: int):
    root = Category.objects.get(id=root)

    return render(request, 'groups/index.html', {
        'roots': root
    })
