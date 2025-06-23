import datetime

from django.conf import settings
from django.core.mail import EmailMultiAlternatives

from django.db.models.signals import m2m_changed
# from django.db.models.signals import post_save # МОЖНО ПОСТАВИТЬ: post_(delete,init,migrate,save)
from django.db.models.signals import post_save, post_delete, pre_save # МОЖНО ПОСТАВИТЬ: post_(delete,init,migrate,save)
from django.dispatch import receiver
from .models import  Post
from .models import  Comment #PostCategory
from django.template.loader import render_to_string




def send_notifications(preview,pk,title,subscribers): #программа собственно отсылки писем
    html_content= render_to_string (
        'post_created_email.html', #ФАЙЛ собственно текста письма - он создаётся в templates/
        {'text':preview,'link':f"{settings.SITE_URL}/news/{pk}"} #красивая ссылка в почте на открытие собственно статьи
    )
    msg = EmailMultiAlternatives(
        subject = title,
        body = '',
        from_email = settings.DEFAULT_FROM_EMAIL, #от кого отправляютсявсе письма по умолчанию
        to = subscribers,
    )
    msg.attach_alternative(html_content,'text/html') # сформированный выше шаблон с указанием формата
    msg.send() # собственно отсылка



# @receiver(post_save, sender=PostCategory)
# def notify_about_new_post(sender, instance, created, **kwargs):

# # СИГНАЛ НА ПРИВЕДЕНИЕ ПОСТА К НУЖНОЙ КАТЕГОРИИ - УБИРАЮ
# @receiver(m2m_changed, sender=PostCategory) #от кого приходит сигнал о событии
# def notify_about_new_post(sender,instance,**kwargs):
#     print('СИГНАЛ СВЯЗИ= kwargs[action]='+kwargs['action']+' kwargs='+str(kwargs)+'  instance='+str(instance)+ ' sender='+str(sender))
#     # СИГНАЛ = pre_add
#     # СИГНАЛ = post_add
#     if kwargs['action'] == 'post_delete':  # если было событие добавления add поста post в категриии PostCategory
#         print('РАСПЕЧАТКА ПО СИГНАЛУ удаления, МОЖНО УКАЗАТЬ ПЕРЕМЕННУЮ')
#     if kwargs['action']== 'post_add': #если было событие добавления add поста post в категриии PostCategory
#         # print('РАСПЕЧАТКА ПО СИГНАЛУ, МОЖНО УКАЗАТЬ ПЕРЕМЕННУЮ')
#         categories=instance.categorys.all() #всё что послужило сигналом - список категорий данного поста, здесь не instance.=PostCategory.category а =Post.categorys!!!
#         subscribers_emails = [] # исходно список почт подписчиков для рассылки пуст
#         # subscribers_emails = ['proba@mail.ru',]
#         for cat in categories: # перебор всех категорий поста
#             # subscribers = cat.subscribers_set.all()
#             subscribers = cat.subscribers.all()
#             # for s in subscribers:
#             #     print(f"Subscriber ID: {s.id}, User: {s.user}, Email: {s.user.email}") #вывод на печать!
#             subscribers_emails += [s.user.email for s in subscribers  if s.user.email]
#
#         subscribers_emails = list(set(subscribers_emails)) # ДЕЛАЮ СПИСОК УНИКАЛЬНЫХ ПОЧТ - НА ВСЯКИЙ СЛУЧАЙ
#         print('РАСПЕЧАТКА ПО СИГНАЛУ, МОЖНО УКАЗАТЬ ПЕРЕМЕННУЮ')
#         send_notifications(instance.preview(), instance.pk, instance.zagolov, subscribers_emails)
#     # здесь instance.preview() = post.previev(), instance.pk - тот ID с которым создан пост , instance.zagolov = post.zagolov








# # УДАЛЯЮ ДО ЗАМЕНЫ АВТОРА НА ЮЗЕРА
# # ТАК ЖЕ ВМЕСТО ДЕКОРАТОРА post_save МОЖНО ИСПОЛЬЗОВАТЬ pre_save ЕСЛИ СПЕРВАИМПОРТИРОВАТЬ
# # в декоратор передаётся первым аргументом сигнал, на который будет реагировать эта функция, и в отправители надо передать также модель
# @receiver(post_save, sender=Post)
# # создаём функцию-обработчик с параметрами под регистрацию сигнала
# def notify_managers_post(sender, instance, created, **kwargs):
#     # print('СИГНАЛ ПОСТА=  kwargs='+str(kwargs)+"  CREATED=" + str(created) +'  instance='+str(instance) +' sender='+str(sender) )
#     author=instance.author
#
#     time_post = str(instance.time_in)[0:15]
#     time_auth=str(author.timezap)[0:15]
#     print('ВРЕМЯ= time_post=' + time_post+ '  time_auth='+time_auth)
#     author.kolzap +=1
#     if time_post != time_auth:
#         author.kolzap=1
#
#     if author.kolzap>3:
#         raise RuntimeError('ВЫ ПРЕВЫСИЛИ ЛИМИТ 3 ПОСТА В ТЕЧЕНИЕ 10 МИНУТ! Подождите немного.')
#         # author.kolzap = author.kolzap/0  # ВЫЗОВ ОШИБКИ ZeroDivisionError at /news/create/
#     author.timezap = instance.time_in
#     author.save()


# # ВАРИАНТ ПРЕРЫВАНИЯ ОТ ПРЕПОДА - удалил потому что нет пока ограничения
# @receiver(pre_save, sender=Post)
# # создаём функцию-обработчик с параметрами под регистрацию сигнала
# def post_limit(sender, instance, **kwargs):
#     today=datetime.date.today()
#     author=instance.author
#     kolpost=Post.objects.filter(author=author, time_in__date=today).count()
#     if kolpost>=6:
#         raise RuntimeError('ВЫ ПРЕВЫСИЛИ ЛИМИТ 6 ПОСТОВОВ В СУТКИ! Подождите немного.')
#     author=instance.author
#
#     time_post = str(instance.time_in)[0:15]
#     time_auth=str(author.timezap)[0:15]
#     print('ВРЕМЯ= time_post=' + time_post+ '  time_auth='+time_auth)
#     author.kolzap +=1
#     if time_post != time_auth:
#         author.kolzap=1






# ОБРАБОТЧИК УДАЛЕНИЯ СОБЫТИЯ - У МЕНЯ ПОСТА!
@receiver(post_delete, sender=Post)
def notify_managers_appointment_canceled(sender, instance, **kwargs):
    print('СИГНАЛ УДАЛЕНИЯ ПОСТА=  kwargs=' + str(kwargs)  + '  instance=' + str(instance) + ' sender=' + str(sender) +' time_in='+str(sender.time_in))
    message = f'Canceled appointment for {instance.time_in.strftime("%d %m %Y")}'
    print('message='+message +' raiting='+str(instance.raiting))








# ИСПОЛЬЗОВАТЬ КАК АНАЛОГ
# from django.shortcuts import render
# from django.views.generic import TemplateView
# from django.contrib.auth.mixins import LoginRequiredMixin
#
# class IndexView(LoginRequiredMixin, TemplateView):
#     template_name = 'protect/index.html'
#
# # ДОБАВЛЕНИЕ РАБОТЫ С ГРУППАМИ - распознавание есть ли в группе авторов
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
#         return context







