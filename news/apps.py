from django.apps import AppConfig


class NewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'news'
    def ready(self):
        import  news.signals

# УЧЕБНЫЙ ВАРИАНТ
# from django.apps import AppConfig
# class AppointmentConfig(AppConfig):
#     name = 'appointment'
#     def ready(self):
#         import appointment.signals