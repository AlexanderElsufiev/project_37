

# СПИСОК ЗАПРЕЩЁННЫХ СЛОВ
class Zapret(models.Model):
    zapret = models.CharField(max_length=50, default='', unique=True)


from .models import Zapret  # если функция в том же приложении

def sravn(text):
    # Получаем все запрещённые слова из базы
    zaprety = set(Zapret.objects.values_list('zapret', flat=True))
    # Разбиваем текст на слова
    words = text.split()
    # Фильтруем слова
    filtered = [word for word in words if word not in zaprety]
    # Собираем результат обратно в строку
    return ' '.join(filtered)



def sravn(text):
    zaprety = set(Zapret.objects.values_list('zapret', flat=True))
    words = text.split()
    result = []

    for word in words:
        if word in zaprety:
            result.append('*' * len(word))
        else:
            result.append(word)
    text = ' '.join(result)
    return text


