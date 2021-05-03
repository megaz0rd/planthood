from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()


@sched.scheduled_job('cron', day_of_week='mon-sat', hour=8)
def scheduled_job():
    print('This job is run every weekday at 8am.')


sched.start()
