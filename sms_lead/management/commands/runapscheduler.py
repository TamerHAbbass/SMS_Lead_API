import logging

from django.conf import settings
from sms_lead.sms_run import run
from apscheduler import events
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from sms_lead.management.commands.jobstores import DjangoJobStore
from sms_lead.models import DjangoJobExecution
from sms_lead.management.commands import util
from reporting.generate_report import main as send_report
import datetime

logger = logging.getLogger(__name__)

TIME_MINUTES = 60

# def get_dir(event):
#   print(dir(event.alias))
#   print(event.job_id)

# The `close_old_connections` decorator ensures that database connections, that have become
# unusable or are obsolete, are closed before and after our job has run.
@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
  """
  This job deletes APScheduler job execution entries older than `max_age` from the database.
  It helps to prevent the database from filling up with old historical records that are no
  longer useful.
  
  :param max_age: The maximum length of time to retain historical job execution records.
                  Defaults to 7 days.
  """
  DjangoJobExecution.objects.delete_old_job_executions(max_age)



class Command(BaseCommand):
  help = "Runs APScheduler."

  def handle(self, *args, **options):
      scheduler = BlockingScheduler({'apscheduler.executors.default': {'class': 'apscheduler.executors.pool:ThreadPoolExecutor','max_workers': '10'}},  timezone=settings.TIME_ZONE)
      scheduler.add_jobstore(DjangoJobStore(), "default")

      try:
          logger.info("Starting scheduler...")
          scheduler.add_listener(run, events.EVENT_JOB_SUBMITTED | events.EVENT_JOB_EXECUTED)
          scheduler.start()
      except KeyboardInterrupt:
          logger.info("Stopping scheduler...")
          scheduler.shutdown()
          logger.info("Scheduler shut down successfully!")

