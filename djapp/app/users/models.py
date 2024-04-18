from django.db import models

# Модель пользователя
class User(models.Model):
    username = models.CharField(max_length=100)  # Имя пользователя
    points = models.IntegerField(default=0)  # Количество очков пользователя
    tips_first_type = models.IntegerField(default=0)  # Количество подсказок первого типа у пользователя
    tips_second_type = models.IntegerField(default=0)  # Количество подсказок второго типа у пользователя

    def __str__(self):
        """
        Возвращает строковое представление объекта пользователя
        """
        return self.username

    def SubstractClueFirstType(self):
        """
        Вычитает одну подсказку первого типа из общего количества у пользователя.
        """
        self.tips_first_type -= 1  # Уменьшаем количество доступных подсказок первого типа на 1
        self.save()  # Сохраняем изменения

# Модель ответа
class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Связь с пользователем
    text = models.CharField(max_length=255)  # Текст ответа
    used = models.BooleanField(default=False)  # Флаг использования ответа
    created_at = models.DateTimeField(auto_now_add=True)  # Дата и время создания ответа
