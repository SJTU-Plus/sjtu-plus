import logging
from datetime import timedelta
from time import ctime

import requests
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger
from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils.timezone import localtime
from django_apscheduler.jobstores import DjangoJobStore
from requests.auth import HTTPBasicAuth
from requests.exceptions import SSLError

from groups.models import Category, Group

# logger = logging.getLogger(__name__)
logger = logging.getLogger('django.request')


def github_action():
    try:
        logger.debug('running github_action')
        resp = requests.post(
            settings.GITHUB_TRIGGER_URL,
            json={'ref': 'master'},
            headers={'Accept': 'application/vnd.github.v3+json'},
            auth=HTTPBasicAuth(settings.GITHUB_USERNAME, settings.GITHUB_PERSONAL_ACCESS_TOKEN)
        )
        logger.info('Returned {} from {}'.format(resp.status_code, resp.url))
    except (ConnectionError, SSLError) as e:
        logger.error(e)


def check_entity(entity_class, delta: timedelta):
    try:
        entity = entity_class.objects.latest('last_modified')
        logger.info("{} {} {}".format(ctime(), str(entity_class), entity.last_modified))
        if localtime() - entity.last_modified < delta + timedelta(seconds=1):
            github_action()
            return
    except entity_class.DoesNotExist:
        logger.info('empty {}'.format(entity_class))


def check_database(delta: timedelta):
    logger.info("invoked")
    check_entity(Group, delta)
    check_entity(Category, delta)


class Command(BaseCommand):
    help = 'Watch the Category and Group. Invoke github deployment.'

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            check_database,
            args=(timedelta(seconds=settings.DEPLOYMENT_INTERVAL),),
            trigger=IntervalTrigger(seconds=settings.DEPLOYMENT_INTERVAL),
            id="github_action",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'github_action'.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
