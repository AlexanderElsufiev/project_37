
from django.urls import path



# Импортируем созданное нами представление
# from .views import PostsList, PostsListSearch, PostDetail, ArtDetail
# # , ProductDetail
# # from .views import ProductsList, ProductDetail, ProductCreate, ProductUpdate, ProductDelete
# from .views import PostCreate, PostUpdate, PostDelete, ArtCreate, ArtUpdate, ArtList, ArtDelete, ArtListSearch

from .views import AppointmentView;
from django.urls import path
from . import views

urlpatterns = [


   # path('', ArtList.as_view(), name='art_list'),
   # path('<int:pk>', ArtDetail.as_view(), name='art_list_uno'),

   # path('make_appointment/', AppointmentView.as_view(), name='Appointment_View'),
   path('make_appointment/', views.AppointmentView.as_view(), name='make_appointment'),

   # path('<int:pk>/edit/', ArtUpdate.as_view(), name='art_edit'),
   # path('<int:pk>/delete/', ArtDelete.as_view(), name='art_delete'),
   # path('search/', ArtListSearch.as_view()),
]
