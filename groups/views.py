from django.http import JsonResponse
from django.shortcuts import render

from .models import Category, Group


def index(request):
    roots = Category.objects.filter(parent__id=5)

    return render(request, 'groups/index.html', {
        'roots': list(roots)
    })


def json(request, root: int):
    root = Category.objects.get(id=root)

    def resolve_category(category: Category):
        return {
            "category_id": category.id,
            "category_name": category.name,
            "groups": [{
                "group_id": g.id,
                "group_name": g.name,
                "group_number": str(g.number) if g.number else None,
                "bot_enabled": g.bot_enabled,
                "vacancy": g.vacancy,
            } for g in Group.objects.filter(category=category)],
            "subcategories": [
                resolve_category(c) for c in Category.objects.filter(parent=category)
            ]
        }

    return JsonResponse(resolve_category(root))
