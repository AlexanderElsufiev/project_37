
from django.urls import path


# Импортируем созданное нами представление
from .views import PostsList, PostsListSearch, PostDetail, ArtDetail
# , ProductDetail
# from .views import ProductsList, ProductDetail, ProductCreate, ProductUpdate, ProductDelete
from .views import PostCreate, PostUpdate, PostDelete, ArtCreate, ArtUpdate, ArtList, ArtDelete, ArtListSearch

urlpatterns = [
   # path — означает путь.
   # В данном случае путь ко всем товарам у нас останется пустым.
   # Т.к. наше объявленное представление является классом,
   # а Django ожидает функцию, нам надо представить этот класс в виде view.
   # Для этого вызываем метод as_view.
   # path('', PostsList.as_view()),
   # ПОСЛЕДУЮЩЕЕ БУДЕТ ПОЗЖЕ
   # pk — это первичный ключ товара, который будет выводиться у нас в шаблон
   # int — указывает на то, что принимаются только целочисленные значения

   # path('news/', PostsList.as_view(), name='post_list'),
   # path('news/search/', PostsListSearch.as_view()),
   # path('news/<int:pk>', PostDetail.as_view(), name='post_list_uno'),
   # # path('create/', create_product, name='product_create'),
   # path('news/create/', PostCreate.as_view(), name='post_create'),
   # path('news/<int:pk>/edit/', PostUpdate.as_view(), name='post_edit'),
   # path('news/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),


   path('', ArtList.as_view(), name='art_list'),
   path('<int:pk>', ArtDetail.as_view(), name='art_list_uno'),
   path('create/', ArtCreate.as_view(), name='art_create'),
   path('<int:pk>/edit/', ArtUpdate.as_view(), name='art_edit'),
   path('<int:pk>/delete/', ArtDelete.as_view(), name='art_delete'),
   path('search/', ArtListSearch.as_view()),
]
