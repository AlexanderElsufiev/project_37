import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from django.core.mail import send_mail

logger = logging.getLogger(__name__)


# наша задача по выводу текста на экран
# def my_job():
#     print('hello from job =Appointment')

from news.models import PostCategory, Post
import datetime
from datetime import datetime, timedelta
from django.conf import settings
from django.core.mail import EmailMultiAlternatives

# def my_job(instance,**kwargs):
def my_job():
    kol_day=7 #ЗА СКОЛЬКО ДНЕЙ БЕРЁМ СПИСОК НОВОСТЕЙ
    print(f"hello from job =NEWS= {datetime.now()}")
    print('Post='+str(Post))
    # today = datetime.date.today()
    today = datetime.now().date()
    to_day= today - timedelta(days=kol_day)
    posts = Post.objects.filter(time_in__date__gte=to_day)
    spisok = {} # БУДУЩИЙ СПИСОК ОТСЫЛОК

    for pst in posts:
        emails = []
        cats=pst.categorys.all()
        for cat in cats:
            subscribers = cat.subscribers.all()
            emails += [s.user.email for s in subscribers if s.user.email]
        emails = list(set(emails))  # ДЕЛАЮ СПИСОК УНИКАЛЬНЫХ ПОЧТ
        content=f"<h2>Появилась новая <a href= {settings.SITE_URL}/news/{pst.pk}> статья </a>"
        content += f" в разделе куда вы подписаны. </h2> <p>Заголовок='{pst.zagolov}'</p> <p>Превью='{pst.preview()}'</p> "
        # print(f"КРАСИВАЯ ОТСЫЛКА = {content}")
        for email in emails:
            if not email in spisok:spisok[email]=[]
            spisok[email].append(content)
    # print(f"spisok={spisok}")
    # ТЕПЕРЬ СОБСТВЕННО ОТСЫЛКА ПИСЕМ
    for email in spisok:
        posti=spisok[email]
        lettre='<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>УВЕДОМЛЕНИЕ!</title></head><body>'
        lettre+=f"<p>За последние {kol_day} дней в чате появились следующие новости:</p>"
        for pst in posti:
            lettre+=pst
        lettre += f"</body></html>"
        msg = EmailMultiAlternatives(
            subject='Уведомление по почте',
            body=f"В приложении список статей за последние {kol_day} дней, которые вы могли случайн оне увидеть на сайте",
            from_email=settings.DEFAULT_FROM_EMAIL,  # от кого отправляютсявсе письма по умолчанию
            to=[email],
        )
        msg.attach_alternative(lettre, 'text/html')  # сформированный выше шаблон с указанием формата
        msg.send()  # собственно отсылка







































# функция, которая будет удалять неактуальные задачи
def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # добавляем работу нашему задачнику
        scheduler.add_job(
            my_job,
            trigger=CronTrigger(second="*/30"),
            # trigger=CronTrigger(second="*/(3600*24*7)"), # ВАРИАНТ РАССЫЛКИ ИМЕННО РАЗ В НЕДЕЛЮ
            # То же, что и интервал, но задача тригера таким образом более понятна django
            id="my_job",  # уникальный айди
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить, либо уже выполнять не надо.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")



