from django.shortcuts import render

from .models import Category, Group, Website


def build_category(category):
    groups = Group.objects.filter(category=category, number__isnull=False)
    websites = Website.objects.filter(category=category)
    categories = Category.objects.filter(parent=category)
    return {
        'id': category.id,
        'name': category.name,
        'groups': list(groups) if groups.count() > 0 else None,
        'websites': list(websites) if websites.count() > 0 else None,
        'subcategories': [build_category(category) for category in categories] if categories.count() > 0 else None
    }


def index(request, root: int):
    root = build_category(Category.objects.get(id=root))
    return render(request, 'groups/group.j2', {
        'root': root
    })


def website(request, root: int):
    root = build_category(Category.objects.get(id=root))
    return render(request, 'groups/website.j2', {
        'root': root
    })
