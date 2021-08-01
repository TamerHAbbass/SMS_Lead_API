
from .sms_run import start_sms
from apscheduler.schedulers.background import BackgroundScheduler


HOUR = (60*60) * .1

scheduler = BackgroundScheduler()

def main():
    print('hi')
    start_sms()

scheduler.add_job(main, 'interval', seconds=HOUR)
scheduler.start()