from apscheduler.schedulers.blocking import BlockingScheduler

# from plantswap.models import Reminder
from django.core.mail import send_mail

sched = BlockingScheduler()


@sched.scheduled_job('cron', day_of_week='0-6', hour=11, minute=30)
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
