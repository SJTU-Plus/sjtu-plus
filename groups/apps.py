from uuid import uuid1

from django.apps import AppConfig
from django.db.models.signals import post_save, post_delete


class GroupsConfig(AppConfig):
    name = 'groups'

    def ready(self):
        from groups.models import Category, Group
        from groups.signals.github import trigger_github_action

        post_save.connect(trigger_github_action, sender=Category, dispatch_uid=uuid1())
        post_save.connect(trigger_github_action, sender=Group, dispatch_uid=uuid1())
        post_delete.connect(trigger_github_action, sender=Category, dispatch_uid=uuid1())
        post_delete.connect(trigger_github_action, sender=Group, dispatch_uid=uuid1())
