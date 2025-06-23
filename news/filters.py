from django_filters import FilterSet
import django_filters
from django import forms


from .models import Post


# Создаем свой набор фильтров для модели Product.
# FilterSet, который мы наследуем,
# должен чем-то напомнить знакомые вам Django дженерики.
class PostFilter(FilterSet):
    # time_in__lt = django_filters.DateFilter(
    #     field_name='time_in',lookup_expr='lt',label='Дата раньше чем:'
    # )
    # time_in__gt = django_filters.DateFilter(
    #     field_name='time_in',lookup_expr='lt',label='Дата больше чем:'
    # )

    time_in__gt = django_filters.DateFilter(
        field_name='time_in',lookup_expr='gte',label='С даты:',
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    time_in__lt = django_filters.DateFilter(
        # ФИЛЬТ БЛАГОДАРЯ field_name='time_in__date' СРАВНИВАЕТ С ОБРЕЗАННЫМ ВРЕМЕНЕМ, ПРАВИЛЬНО
        field_name='time_in__date',lookup_expr='lte',label='По дату:',
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    zagolov__icontains = django_filters.CharFilter(
        field_name='zagolov',lookup_expr='icontains',label='заголовок содержит'
    )
    author = django_filters.CharFilter(
        field_name='author__user__username',lookup_expr='icontains',label='Имя автора содержит'
    )
    raiting__gt = django_filters.NumberFilter(
        field_name='raiting',lookup_expr='gte',label='Рейтинг поста от:'
    )
    raiting__lt = django_filters.NumberFilter(
        field_name='raiting',lookup_expr='lte',label='до:'
    )


    class Meta:
       # В Meta классе мы должны указать Django модель,
       # в которой будем фильтровать записи.
       model = Post
       # В fields мы описываем по каким полям модели
       # будет производиться фильтрация.
       # fields = {
       #     # поиск по названию. МОЖНО ТОЧНОЕ СОВПАДЕНИЕ = ''
       #     'zagolov': ['icontains'],
       #     'time_in':['lt','gt' ],
       #     'raiting':['lt','gt' ],
       # }
       # УКАЗЫВАЕТ ПОРЯДОК ФИЛЬТРОВ, ВСЕ НЕ ПЕРЕЧИСЛЕННЫЕ ЗДЕСЬ ПОЙДУТ В ПОРЯДКЕ ОПИСАНИЯ
       fields = ['time_in__gt','time_in__lt','author','zagolov__icontains','raiting__lt','raiting__gt']






