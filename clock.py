import django
from django.conf import settings
from planthood import settings as planthood_defaults

settings.configure(default_settings=planthood_defaults, DEBUG=True)
django.setup()

from apscheduler.schedulers.blocking import BlockingScheduler

# from plantswap.models import Reminder
from django.core.mail import EmailMessage

sched = BlockingScheduler()


@sched.scheduled_job('interval', minutes=3)
def scheduled_job():
    email = EmailMessage(
        'test tematu',
        'test treści',
        to=['planthood-mokotow@gmail.com']
    )
    email.send()
    print('Reminders sent at 8am.')


sched.start()
