import os
import django
from django.core import mail
from apscheduler.schedulers.blocking import BlockingScheduler

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'planthood.settings')
django.setup()

sched = BlockingScheduler()


@sched.scheduled_job('interval', minutes=3)
def scheduled_job():
    with mail.get_connection() as connection:
        mail.EmailMessage(
            'test tematu', 'test treści', 'planthood.mokotow@gmail.com',
            ['planthood.mokotow@gmail.com'],
            connection=connection,
        ).send()
    print('Reminders sent at 8am.')


sched.start()
