import django
from django.conf import settings
from apscheduler.schedulers.blocking import BlockingScheduler

from django.core.mail import EmailMessage

settings.configure()
django.setup()

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
