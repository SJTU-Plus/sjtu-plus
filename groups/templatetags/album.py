from typing import List

from django import template

from groups.models import Group, Category

register = template.Library()


@register.inclusion_tag('groups/group_album.html')
def group_album(groups: List[Group]):
    return {
        'groups': [
            {
                'id': group.id,
                'name': group.name,
                'number': group.number
            }
            for group in groups
        ]
    }


@register.inclusion_tag('groups/category_panel.html')
def category_panel(category: Category):
    groups = Group.objects.filter(category=category, number__isnull=False)
    categories = Category.objects.filter(parent=category)

    return {
        'id': category.id,
        'groups': list(groups) if groups.count() > 0 else None,
        'children': list(categories) if categories.count() > 0 else None
    }
