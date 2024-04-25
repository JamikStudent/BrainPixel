from django.db import models
from django.contrib.auth.models import User as DjangoUser
from django.contrib.auth import get_user_model

# Модель пользователя
class User(models.Model):
    username = models.CharField(max_length=100)  # Имя пользователя
    points = models.IntegerField(default=0)  # Количество очков пользователя
    tips_first_type = models.IntegerField(default=0)  # Количество подсказок первого типа у пользователя
    tips_second_type = models.IntegerField(default=0)  # Количество подсказок второго типа у пользователя

    #def __str__(self):
    #    """
    #    Возвращает строковое представление объекта пользователя
    #    """
    #    return self.username

    def SubstractClueFirstType(self):
        """
        Вычитает одну подсказку первого типа из общего количества у пользователя
        """
        self.tips_first_type -= 1
        self.save()  # Сохраняем изменения
    
    def SubstractClueSecondType(self):
        """
        Вычитает одну подсказку второго типа из общего количества у пользователя
        """
        self.tips_second_type -= 1
        self.save()  # Сохраняем изменения

class Topic(models.Model):
    title = models.CharField(max_length=255)

class Question(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    text = models.TextField()

class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)
