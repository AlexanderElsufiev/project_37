
import os
from django.db import models
from datetime import datetime
from django.db.models import Sum

from django.contrib.auth.models import User


# class Author(models.Model):
#    # user = models.ForeignKey(User, on_delete=models.CASCADE)
#    # сделаем максимум 1 автора на 1 пользователя
#    user = models.OneToOneField(User, on_delete=models.CASCADE)
#    raiting = models.IntegerField(default=0)
#    # kolzap = models.IntegerField(default=0)
#    # timezap = models.DateTimeField(auto_now_add=True)
#
#    def __str__(self):
#        return self.user.username
#
#    def update_rating(self):
#        # 1. Суммарный рейтинг всех постов автора, умноженный на 3
#        raiting_post = self.author_post.aggregate(total=models.Sum('raiting'))['total'] or 0
#        raiting_comm = self.user.user_comm.aggregate(total=models.Sum('raiting'))['total'] or 0
#        raiting_post_comm = Comment.objects.filter(post__author=self).aggregate(total=models.Sum('raiting'))[
#                                       'total'] or 0
#        # raiting_post_comm = self.author_post.all().post_comm.(total=models.Sum('raiting'))['total'] or 0
#        self.raiting = raiting_post*3+raiting_comm+raiting_post_comm
#        self.save()
#

class Category(models.Model):
    category = models.CharField(max_length=50, default='', unique=True)

    def __str__(self):
        return self.category.title() # добавка .title() чтобы выводить каждое новое слово с заглавной буквы




class Post(models.Model):
    # txt = 't'
    # news = 'n'
    # TIPS = [(txt, 'Статья'),(news, 'Новость'),]
    # Дополнительное поле указатель на номера категорий - многие ко многим
    # categorys = models.ManyToManyField(Category, through = 'PostCategory')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category_post') # только 1 категория на пост

    # авторы
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name='user_post')

    # ТИП стаитья или новость
    # tip = models.CharField(max_length=1,choices=TIPS,default=txt)
    time_in = models.DateTimeField(auto_now_add=True)
    time_ism = models.DateTimeField(auto_now=True)
    zagolov = models.CharField(max_length=100, default='')
    text = models.TextField()
    # raiting = models.IntegerField(default=0)
    # likes = models.IntegerField(default=0)
    # dislikes = models.IntegerField(default=0)
    # Дополнительное поле указатель на комментарии
    comments = models.ManyToManyField(User, through = 'Comment')

    # def like(self):
    #     self.likes += 1;self.raiting += 1
    #     self.save()
    # def dislike(self):
    #     self.dislikes += 1;self.raiting -= 1
    #     self.save()

    def preview(self):
        stext = self.text[:123] + '...' if len(self.text) > 123 else self.text
        return stext

    # Обратите внимание, что мы дополнительно указали методы __str__ у моделей. Django будет их использовать, когда потребуется где-то напечатать наш объект целиком
    def __str__(self):
        # return f'{self.zagolov.title()}: {self.text[:20]} </br>'
        return f'{self.zagolov.title()}: {self.preview()} </br>'

# МЕДИАФАЙЛЫ ДЛЯ ПОСТОВ
class MediaFile(models.Model):
    MEDIA_TYPES = [
        ('image', 'Изображение'),
        ('video', 'Видео'),
        ('audio', 'Аудио'),
        ('document', 'Документ!'),
        ('other', 'Другое!!!'),
    ]

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='media_files')
    file = models.FileField(upload_to='media/posts/%Y/%m/%d/')
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPES)
    title = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.post.zagolov} - {self.get_media_type_display()}"

    def save(self, *args, **kwargs):
        # Автоматическое определение типа файла по расширению
        if not self.media_type:
            ext = os.path.splitext(self.file.name)[1].lower()
            if ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp']:
                self.media_type = 'image'
            elif ext in ['.mp4', '.avi', '.mov', '.wmv', '.flv']:
                self.media_type = 'video'
            elif ext in ['.mp3', '.wav', '.flac', '.aac']:
                self.media_type = 'audio'
            elif ext in ['.pdf', '.doc', '.docx', '.txt']:
                self.media_type = 'document'
            else:
                self.media_type = 'other'
        super().save(*args, **kwargs)


from django.core.mail import send_mail
from django.conf import settings

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE, related_name='post_comm')
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name='user_comm')
    comment = models.CharField(max_length=255, default='')
    time_in = models.DateTimeField(auto_now_add=True)
    # raiting = models.IntegerField(default=0)
    # likes = models.IntegerField(default=0)
    # dislikes = models.IntegerField(default=0)
    # txt = 't';    news = 'n'
    rassm='1';prin='2';otkl='0'
    STAT = [(rassm, 'Не рассмотрен'),(prin, 'Принят'),(otkl,'Отклонён')]
    # ТИП стаитья или новость
    stat = models.CharField(max_length=1,choices=STAT,default=rassm)


    def send_new_comment_email(self):
        """Отправка email автору поста о новом комментарии"""
        post_user = self.post.user
        # Не отправляем письмо, если автор комментария = автор поста
        # if self.user == post_user or not post_user.email:return

        subject = f'Новый комментарий к вашему посту'
        message = f'''
    Здравствуйте, {post_user.username}!
    К вашему посту "{self.post.zagolov}" добавлен новый комментарий.
    Автор комментария: {self.user.username}
    Комментарий: "{self.comment}"
    Дата: {self.time_in.strftime('%d.%m.%Y %H:%M')}

    Для модерации перейдите по ссылке:
    http://127.0.0.1:8000/news/privat/{self.post.id}
            '''

        try:
            send_mail(
                subject=subject,message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[post_user.email],
                fail_silently=False,
            )
        except Exception as e:print(f"Ошибка отправки email: {e}")

    def save(self, *args, **kwargs):
        """Переопределяем save для отправки email при создании нового комментария"""
        is_new = self.pk is None  # Проверяем, новый ли это комментарий
        if self.user==self.post.user and self.stat=='1': self.stat='2' # свой коммент автоматом принимается
        super().save(*args, **kwargs)
        # Отправляем email только для новых комментариев
        if is_new:self.send_new_comment_email()

    def send_status_email(self):
        """Отправка email о изменении статуса"""
        if not self.user.email: return  # Если у пользователя нет email
        subject = f'Ваш комментарий {self.get_stat_display()}'
        message = f'''
    Здравствуйте, {self.user.username}!
    Ваш комментарий к посту "{str(self.post)}" поменял статус.
    Ваш комментарий: "{self.comment}"
    Статус: {self.get_stat_display()} '''
        # было {self.post.zagolov} поставил {str(self.post)}
        try:
            send_mail(
                subject=subject,message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[self.user.email],
                fail_silently=False,
            )
        except Exception as e:print(f"Ошибка отправки email: {e}")





    def like(self):
        old_status = self.stat
        self.stat= self.prin;self.save()
        # Отправляем email только если статус изменился
        if old_status != self.prin:self.send_status_email()

    def dislike(self):
        old_status = self.stat
        self.stat = self.otkl;self.save()
        # Отправляем email только если статус изменился
        if old_status != self.otkl:self.send_status_email()






# class PostCategory(models.Model):
#     post = models.ForeignKey(Post, on_delete = models.CASCADE)
#     category = models.ForeignKey(Category, on_delete = models.CASCADE)
#     class Meta:
#         unique_together = ('post', 'category')


# # класс подписок пользователей на категории
# class Subscribers(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subscribers')
#     class Meta:
#         unique_together = ('user', 'category')

# # СПИСОК ЗАПРЕЩЁННЫХ СЛОВ
# class Zapret(models.Model):
#     zapret = models.CharField(max_length=50, default='', unique=True)
#     # Для читаемости
#     def __str__(self):
#         return self.zapret.title()

# процедура удаления из текста запрещённых слов - перенесена в templatetags/custom_filters.py

