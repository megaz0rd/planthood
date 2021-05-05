import os
import django
from django.core import mail
from apscheduler.schedulers.blocking import BlockingScheduler

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'planthood.settings')
django.setup()

from plantswap_api.utils import today
from plantswap.models import Reminder

sched = BlockingScheduler()


@sched.scheduled_job('cron', day_of_week='Mon-Sat', hour=8)
def scheduled_job():
    recipients = []

    for reminder in Reminder.objects.all():
        if reminder.next_care_day == today:
            recipient = reminder.creator.email
            if recipient not in recipients:
                recipients.append(reminder.creator.email)

    if recipients:
        with mail.get_connection() as connection:
            mail.EmailMessage(
                'Twoje rośliny wymagają uwagi!',
                'Zaloguj się do aplikacji, by sprawdzić przypomnienia!',
                'planthood.mokotow@gmail.com',
                bcc=recipients,
                connection=connection,
            ).send()
        print('Reminders sent at 6am.')
    else:
        print('No reminders were sent today.')


sched.start()
