from django.contrib import admin

from .models import Category, Group


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    date_hierarchy = 'last_modified'
    readonly_fields = ('last_modified',)
    fields = ('id', 'name', 'parent', 'last_modified')
    list_display = ('id', 'name', 'parent', 'last_modified')


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    date_hierarchy = 'last_modified'
    readonly_fields = ('last_modified',)
    fields = ('name', 'number', 'category', 'last_modified', 'bot_enabled', 'vacancy')
    list_display = ('name', 'number', 'category', 'last_modified', 'bot_enabled', 'vacancy')
    list_filter = ('category',)
