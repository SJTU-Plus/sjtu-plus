import requests
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from requests.auth import HTTPBasicAuth
import logging

logger = logging.getLogger(__name__)


@receiver(post_save)
def trigger_github_action(sender, instance, **kwargs):
    url = 'https://api.github.com/repos/{owner}/{repo}/actions/workflows/{workflow_id}/dispatches'
    username = settings.GITHUB_USERNAME
    token = settings.GITHUB_PERSONAL_ACCESS_TOKEN

    resp = requests.post(
        url.format(owner='sjtu-plus', repo='sjtu-plus.github.io', workflow_id='2177133'),
        json={'ref': 'master'},
        headers={'Accept': 'application/vnd.github.v3+json'},
        auth=HTTPBasicAuth(username, token)
    )

    logger.info(resp.url)
