from django.shortcuts import render

from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
from .models import BaseRegisterForm


class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/'

# ДОБАВЛЕНИЕ ИСПОЛНЕНИЯ ЖЕЛАНИЯ БЫТЬ АВТОРОМ
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required

# добавление авторства в таблицу авторов
from news.models import Author

@login_required
def upgrade_me(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
        # Создаем запись в модели Author, если она еще не существует
        Author.objects.get_or_create(user=user)
    return redirect('/')

