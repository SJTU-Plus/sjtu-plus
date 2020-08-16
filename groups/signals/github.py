import logging

import requests
from django.conf import settings
from requests.auth import HTTPBasicAuth
from requests.exceptions import SSLError

logger = logging.getLogger(__name__)


def trigger_github_action(sender, **kwargs):
    url = 'https://api.github.com/repos/{owner}/{repo}/actions/workflows/{workflow_id}/dispatches'
    username = settings.GITHUB_USERNAME
    token = settings.GITHUB_PERSONAL_ACCESS_TOKEN

    try:
        resp = requests.post(
            url.format(owner='sjtu-plus', repo='sjtu-plus.github.io', workflow_id='2177133'),
            json={'ref': 'master'},
            headers={'Accept': 'application/vnd.github.v3+json'},
            auth=HTTPBasicAuth(username, token)
        )

        logger.info(resp.url)
    except (ConnectionError, SSLError) as e:
        logger.error(e)
