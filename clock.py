import django
from django.conf import settings
from planthood import settings as planthood_defaults

settings.configure(default_settings=planthood_defaults, DEBUG=True)
django.setup()

from apscheduler.schedulers.blocking import BlockingScheduler

from django.core.mail import send_mail

sched = BlockingScheduler()


@sched.scheduled_job('interval', minutes=3)
def scheduled_job():
    send_mail(
        'test tematu',
        'test treści',
        'planthood-mokotow@gmail.com',
        ['planthood-mokotow@gmail.com'],
        fail_silently=False
    )
    print('Reminders sent at 8am.')


sched.start()
