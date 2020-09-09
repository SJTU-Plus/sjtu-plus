from django.shortcuts import render

from .models import Category


def index(request, root: int):
    root = Category.objects.get(id=root)

    return render(request, 'groups/index.j2', {
        'root': root
    })
