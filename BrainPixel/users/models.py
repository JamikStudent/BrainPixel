from django.db import models
from django.contrib.auth.models import User as DjangoUser
from django.contrib.auth import get_user_model

# Модель пользователя
class User(models.Model):
    username = models.CharField(max_length=100)
    user_save_topic = models.IntegerField(default=0)
    coin = models.IntegerField(default=0)
    tips_first_type = models.IntegerField(default=0)
    tips_second_type = models.IntegerField(default=0)
    skin = models.CharField(max_length=10, default='blue')
    skin_b = models.BooleanField(default=True)
    skin_p = models.BooleanField(default=False)
    skin_g = models.BooleanField(default=False)
    has_completed_test = models.BooleanField(default=False)

    def __str__(self):
        """
        Возвращает строковое представление объекта пользователя
        """
        return self.username

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
    topic_title = models.CharField(max_length=255)
    topic_info = models.CharField(max_length=255)
    topic_question_number = models.IntegerField(default=0)

class Question(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=255)
    answer_true = models.CharField(max_length=255)
    answer_false_1 = models.CharField(max_length=255)
    answer_false_2 = models.CharField(max_length=255)
    answer_false_3 = models.CharField(max_length=255)

class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)
