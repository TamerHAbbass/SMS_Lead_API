from reporting.generate_report import main
from django.core.management.base import BaseCommand


class Command(BaseCommand):
  help = "Runs Reporting."

  def handle(self, *args, **options):
      main()