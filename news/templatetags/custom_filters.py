from django import template
# from news.models import Zapret

register = template.Library()

# ВРЕМЕННО УБИРАЮ СОДЕРЖИМОЕ ФИЛЬТРА ЦЕНЗУРЫ, ОСТАВЛЯЯ САМУ ПРОГРАММУ
@register.filter
def censor(text):
    # # zaprety = set(z.zapret.lower() for z in Zapret.objects.all())
    # zaprety = 'НЕЛЬЗЯ'
    # # СПИСОК ВОЗМОЖНЫХ ЗНАКОВ ПРЕПИНАНИЙ, И ПРОБЕЛ
    # znaki='.,+-*/|\!?:; '
    # rez=[text]
    # # РАЗБИВКА НА СЛОВА И ЗНАКИ ПРЕПИНАНИЯ
    # for pr in range(len(znaki)):
    #     zn=znaki[pr]
    #     rz = []
    #     for text in rez:
    #         words = text.split(zn)
    #         k = 0
    #         for word in words:
    #             if k > 0: rz.append(zn)
    #             rz.append(word)
    #             k += 1
    #     rez=rz;rz=[]
    # words = rez
    # # ПРОВЕРКА НА ЗАПРЕТНЫЕ СЛОВА
    # for word in words:
    #     if word.lower() in zaprety:
    #         rz.append(word[0] + '*' * (len(word)-1))
    #     else:
    #         rz.append(word)
    # # СОБРАТЬ ВОЕДИНО
    # text = ''.join(rz)
    return text




