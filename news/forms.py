from django import forms
from django.core.exceptions import ValidationError
from .models import Post, MediaFile , Category #, Subscribers
from datetime import date
from django.forms import inlineformset_factory


# # ФОРМА ПОДПИСКИ НА КАТЕГОРИИ НОВОСТЕЙ - УБИРАЮ
# class SubscriptionForm(forms.Form):
#     categories = forms.ModelMultipleChoiceField(
#         queryset=Category.objects.all(),
#         widget=forms.CheckboxSelectMultiple,
#         required=True,
#         label="Выберите категории для подписки"
#     )
#     class Meta:
#         model = Subscribers
#         fields = ['categories']  # Убедитесь, что это поле включено
#         widgets = {'categories': forms.CheckboxSelectMultiple(),} # другой способ отображения. галочками



# ЭТО УЖЕ НЕ МОДЕЛЬ КАК Product, а некая форма, чуть иное описание
class PostForm(forms.ModelForm):
    # этот блок нужен для нормального отображения с помощью выбора многих ваариантов
    # УБИРАЮ ВЕСЬ БЛОК ВЫБОРА МНОГИХ ВАРИАНТОВ
    # categorys = forms.ModelMultipleChoiceField(
    #     queryset=Category.objects.all(),
    #     widget=forms.CheckboxSelectMultiple,  # или SelectMultiple, если хочешь выпадающий список
    #     required=True,
    #     label='категория новостей (можно много вариантов, но выбрать надо один!)'
    # )

    # description = forms.CharField(min_length=20)
    class Meta:
       # То, с чем форма обязана сравнить вводимые значения
       model = Post
       # можно взять вообще все поля (кроме id!) а можно перечислить только нужные
       # fields = [ 'zagolov', 'text', 'raiting','categorys'] #убрать автора, чтобы не могли менять!
       fields = ['zagolov', 'text', 'category']  # убрал так же рейтинг, и меняю 'categorys' на 'category'
       # ЧТОБЫ АВТОР ПОКАЗЫВАЛСЯ НО НЕ ИЗМЕНЯЛСЯ - НЕ РАБОТАЕТ!!!
       # fields = ['author', 'zagolov', 'text', 'raiting']
       # widgets = {'author': forms.TextInput(attrs={'disabled': 'disabled'}),}

       labels = {
           'author': 'Автор',
           'zagolov': 'Заголовок',
           'text': 'Текст',
           # 'raiting': 'Рейтинг+',
           'category': 'категория для поста'
       }

    def clean(self):
       cleaned_data = super().clean()

       # text = cleaned_data.get("text")
       # zagolov = cleaned_data.get("zagolov")
       # if zagolov == text:
       #     raise ValidationError("Описание не должно быть идентичным названию.")

        # if text is not None and len(text) < 20:
        #     # ТЕКСТ ОШИБКИ = "{'text': ['Описание не может быть менее 20 символов.']}"
        #     raise ValidationError({"text": "Описание не может быть менее 20 символов."})

        # ЕЩЁ ДОБАВИЛЯЮ ПРОВЕРКУ НЕ БОЛЕЕ 6 СООБЩЕНИЙ В СУТКИ (ПЛЮС К 3 В 10 МИНУТ) - ПО ВИДЕО https://disk.yandex.ru/i/swu7JudE2Squ2Q
       # author = cleaned_data.get('author') # НЕ РАБОТАЕТ - АВТОР НЕ ПЕРЕЧИСЛЕН В ПЕРЕЧНЕ fields = [ 'zagolov', 'text', 'raiting','categorys']
       # today=date.today()
       # kolpost=0
       # # kolpost=Post.objects.filter(author=author, time_in__date=today).count() #почему-то перестало срабатывать!
       # print('KOLPOST='+str(kolpost)+ ' author='+str(author)+' today='+str(today))
       # if kolpost>=6:
       #     raise ValidationError("ОГРАНИЧЕНИЕ 6 ПОСТОВ В СУТКИ (ПОМИМО 3 В 10 МИНУТ!) (FORMS.PY) ")

       return cleaned_data

# ДЛЯ МЕДИАФАЙЛОВ
class MediaFileForm(forms.ModelForm):
    class Meta:
        model = MediaFile
        fields = ['file', 'media_type', 'title', 'description']
        labels = {
            'file': 'Файл',
            'media_type': 'Тип медиа',
            'title': 'Название',
            'description': 'Описание'
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'file': forms.FileInput(attrs={'accept': 'image/*,video/*,audio/*,.pdf,.doc,.docx,.txt'}),
        }

# Создаем formset для множественной загрузки файлов
MediaFileFormSet = inlineformset_factory(
    Post,
    MediaFile,
    form=MediaFileForm,
    extra=3,  # количество пустых форм для добавления файлов - максимальное количество
    can_delete=True
)

#ДЛЯ КОММЕНТАРИЕВ
from .models import Comment
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']
        labels = {'comment': 'Ваш комментарий'}
        widgets = {'comment': forms.Textarea(attrs={'rows': 4})}

