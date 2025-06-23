from django.shortcuts import render
from django.http import HttpResponseRedirect

from django.urls import reverse_lazy
from django.views.generic import ListView,DetailView, CreateView, UpdateView, DeleteView

from .models import Post, Comment
from .filters import PostFilter
from .forms import PostForm

# ДЛЯ РАСПРЕДЕЛЕНИЯ ПРАВ ПОЛЬЗОВАТЕЛЕЙ
from django.contrib.auth.mixins import PermissionRequiredMixin

from datetime import datetime
from datetime import date


# ДЛЯ ПОДПИСКИ ПОЛЬЗОВАТЕЛЯ
from .models import  MediaFile
from .forms import PostForm, MediaFileFormSet
from django.db import transaction

from django.db import models



class PostsList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    # model = Product - меняем - показывать будем посты!
    model = Post
    # Поле, которое будет использоваться для сортировки объектов
    ordering = '-time_in'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'post_list.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    # context_object_name = 'products' - меняем на Посты - пока не знаю где их описать - ЭТО АДРЕС ССЫЛКИ
    context_object_name = 'posts'
    paginate_by = 8  # вот так мы можем указать количество записей на странице



# ВЫДАЧА НОВОСТЕЙ НА ПРИВАТНОЙ СТРАНИЦЕ
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q

class PostsListPrivat(LoginRequiredMixin, ListView):
    model = Post
    # ordering = '-time_in'
    template_name = 'post_privat.html'
    context_object_name = 'posts' # ЭТО АДРЕС ССЫЛКИ
    paginate_by = 8  # вот так мы можем указать количество записей на странице

    # def get_queryset(self):
    #     """Показываем только посты текущего пользователя с подсчетом комментариев"""
    #     return Post.objects.filter(user=self.request.user).annotate(
    #         app_count=Count('post_comm',filter=Q(post_comm__stat='2'))
    #     ).order_by('-time_in')

    def get_queryset(self):
        """Показываем только посты текущего пользователя с подсчетом комментариев"""
        queryset = Post.objects.filter(user=self.request.user).annotate(
        # queryset=Post.objects.annotate(
            app_count=Count('post_comm',filter=Q(post_comm__stat='1'))
            # ,app_count2=Count('post_comm',filter=Q(post_comm__stat='2'))
            , app_count3=Count('post_comm',filter=Q(post_comm__stat__in=['1','2']))
        ).order_by('-time_in')

        # Фильтрация по наличию новых комментариев
        show_new = self.request.GET.get('with_comments', False)
        if show_new:queryset = queryset.filter(app_count__gt=0)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['show_new'] = self.request.GET.get('with_comments', False)
        return context




class PostsListSearch(ListView):
    model = Post
    ordering = '-time_in'
    template_name = 'post_list_search.html'
    context_object_name = 'posts'
    paginate_by = 7  # вот так мы можем указать количество записей на странице

    # Переопределяем функцию получения списка товаров
    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset().order_by('-time_in')
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict, который мы рассматривали в этом юните ранее.
        self.filterset = PostFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список товаров
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset

        # Удаляем параметр page из строки запроса - чтобы при пагинации работали переходы
        query_params = self.request.GET.copy()
        if 'page' in query_params:
            query_params.pop('page')
        context['filter_query'] = query_params.urlencode()
        return context


# ДОБАВЛЯЕМ НОВЫЙ КЛАСС
#  Он отличается от ListView тем, что возвращает конкретный объект,  а не список всех объектов из БД
class PostDetail(PermissionRequiredMixin, DetailView):
    permission_required = ('news.view_post',)  # название права на добавление постов
    # form_class = PostForm # ЭТО ДОБАВКА ДЛЯОТОБРАЖЕНИЯ КАТЕГОРИЙ
    model = Post    # Указываем нашу разработанную форму
    template_name = 'post_uno.html' # Используемый шаблон — product.html
    context_object_name = 'post' # Название объекта, в котором будет выбранный пользователем продукт

    # ДЛЯ ВЫДАЧИ КОММЕНТАРИЕВ В НУЖНОМ ПОРЯДКЕ И ФИЛЬТРЕ
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Получаем отфильтрованные комментарии
        filtered_comments = self.object.post_comm.filter(
            models.Q(stat='2')
           | models.Q(user=self.request.user)  # комментарии просматривающего пользователя
           # | models.Q(user=self.object.user) # комментарии самого автора поста
        ).order_by('-time_in')

        # filtered_comments = self.object.post_comm.filter(
        #     models.Q(self.stat in('0','1','2')) | models.Q(user=self.object.user)
        # ).order_by('-time_in')  # Сортировка по убыванию времени создания

        context['filtered_comments'] = filtered_comments
        return context

class PostPrivatDetail (PostDetail):
    template_name = 'post_privat_uno.html' # Используемый шаблон — product.html
    # ДЛЯ ВЫДАЧИ КОММЕНТАРИЕВ В НУЖНОМ ПОРЯДКЕ И ФИЛЬТРЕ

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Получаем отфильтрованные комментарии
        filtered_comments = self.object.post_comm.filter(
            # models.Q(stat = '1')
            models.Q(stat__in=['1', '2'])
           # | models.Q(user=self.request.user)  # комментарии просматривающего пользователя
           # | models.Q(user=self.object.user) # комментарии самого автора поста
        ).order_by('-time_in')

        # filtered_comments = self.object.post_comm.filter(
        #     models.Q(self.stat in('0','1','2')) | models.Q(user=self.object.user)
        # ).order_by('-time_in')  # Сортировка по убыванию времени создания

        context['filtered_comments'] = filtered_comments
        return context



# Добавляем новое представление для создания товаров.
class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)  # название права на добавление постов
    # fields = ['title', 'content'] # не нужна, потому что есть строка form_class = PostForm
    # Указываем нашу разработанную форму
    form_class = PostForm
    model = Post  # модель товаров
    # и новый шаблон, в котором используется форма.
    # template_name = 'post_edit.html' # заменил на специальный с фиксированным автором
    template_name = 'post_create.html'
    success_url = reverse_lazy('post_list')  # путь после успешного ввода
    # ПРИНУДИТЕЛЬНО СТАВИМ ПАРАМЕТР НОВОСТЬ
    # param = 'n'  # Атрибут класса

    # ДЛЯ МЕДИАФАЙЛОВ
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['media_formset'] = MediaFileFormSet(self.request.POST, self.request.FILES)
        else:
            context['media_formset'] = MediaFileFormSet()
        return context


    def form_valid(self, form):
        context = self.get_context_data()
        media_formset = context['media_formset']
        # Используем транзакцию для атомарности операций
        with transaction.atomic():
            user = self.request.user
            print(f'user={user}')
            # author, created = Author.objects.get_or_create(user=user)
            # print(f'user={user} author={author}')
            form.instance.user = user
            print(f'form=={form.instance}')

            # Сохраняем пост
            self.object = form.save()

            # Проверяем и сохраняем медиафайлы
            if media_formset.is_valid():
                media_formset.instance = self.object
                media_formset.save()
            else:
                # Если формсет невалиден, откатываем транзакцию
                return self.form_invalid(form)

        return super().form_valid(form)

    def form_invalid(self, form):
        context = self.get_context_data()
        context['media_formset'] = MediaFileFormSet(self.request.POST, self.request.FILES)
        return self.render_to_response(context)


# Добавляем представление для изменения товара.
class PostUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)  # название права на добавление постов
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    # путь после успешного ввода
    success_url = reverse_lazy('post_list')

# Представление удаляющее товар.
class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)  # название права на добавление постов
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')


# НАПИСАНИЕ НОВОГО КОММЕНТАРИЯ
from django.shortcuts import render, get_object_or_404, redirect
from .forms import CommentForm


# Вариант 2: Class-based view
from django.contrib.auth.mixins import LoginRequiredMixin


class PostCommentView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'post_comment.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):  # Исправлено: args -> *args, *kwargs -> **kwargs
        self.object = self.get_object()
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = self.object
            comment.user = request.user
            comment.save()
            # return redirect('news:post_comment', pk=self.object.pk)
            return redirect('post_list_uno', pk=self.object.pk)

        return self.render_to_response(self.get_context_data(form=form))



# МОДЕРАЦИЯ КОММЕНТАРИЯ
# Добавьте в views.py

from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden


@login_required
def moderate_comment(request, post_id, comment_id, action):
    """Простая модерация комментария"""
    post = get_object_or_404(Post, id=post_id)
    comment = get_object_or_404(Comment, id=comment_id, post=post)

    # Проверка прав
    if request.user != post.user:
        return HttpResponseForbidden()

    if action == 'like':
        comment.like()
    elif action == 'dislike':
        comment.dislike()

    # Возврат на ту же страницу
    return redirect('post_privat_uno', pk=post_id)
