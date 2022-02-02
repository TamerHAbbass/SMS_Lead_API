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

@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
  DjangoJobExecution.objects.delete_old_job_executions(max_age)



class Command(BaseCommand):
  help = "Runs APScheduler."

  def handle(self, *args, **options):
      scheduler = BlockingScheduler({'apscheduler.executors.default': {'class': 'apscheduler.executors.pool:ThreadPoolExecutor','max_workers': '10'}},  timezone=settings.TIME_ZONE)
      scheduler.add_jobstore(DjangoJobStore(), "default")      
      scheduler.add_job(run,trigger = 'interval', seconds = 30, max_instances = 1, coalesce = True )
      scheduler.start()
      # try:
      #     logger.info("Starting scheduler...")
      #     scheduler.add_listener(run, events.EVENT_JOB_SUBMITTED | events.EVENT_JOB_EXECUTED)
      
      # except KeyboardInterrupt:
      #     logger.info("Stopping scheduler...")
      #     scheduler.shutdown()
      #     logger.info("Scheduler shut down successfully!")

