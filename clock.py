import os
import django
from django.core import mail
from apscheduler.schedulers.blocking import BlockingScheduler

from plantswap.models import Reminder
from plantswap_api.utils import today

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'planthood.settings')
django.setup()

sched = BlockingScheduler()


@sched.scheduled_job('corn', day_of_week='Mon-Sat', hour=8)
def scheduled_job():
    with mail.get_connection() as connection:
        mail.EmailMessage(
            'Your plants need your attention!', 'test treści',
            'planthood.mokotow@gmail.com',
            ['planthood.mokotow@gmail.com'],
            connection=connection,
        ).send()
    print('Reminders sent at 8am.')


sched.start()
