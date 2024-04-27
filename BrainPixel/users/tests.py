import json
from django.test import TestCase, Client
from django.urls import reverse
from users.models import User
from .utils import OneCorrectAnswer, FiftyFiftyAnswer

class UseHintsViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        # Создаем тестового пользователя
        self.user = User.objects.create(username='testuser', points=100, tips_first_type=0, tips_second_type=0)

    def test_use_hints_view(self):
        # Данные ответов
        answers_data = [
            {'text': 'Answer 1', 'is_correct': False, 'used': False},
            {'text': 'Answer 2', 'is_correct': True, 'used': False},
            {'text': 'Answer 3', 'is_correct': False, 'used': False}
        ]

        # Отправляем POST-запрос на эндпоинт use_hints_view
        response = self.client.post(reverse('use_hints'), data=json.dumps({'answers': answers_data, 'user_id': self.user.id}), content_type='application/json')

        # Проверяем, что запрос был успешным (код состояния 200)
        self.assertEqual(response.status_code, 200)

        # Проверяем, что ответ содержит обновленные данные ответов
        self.assertIn('updated_answers', response.data)

        # Проверяем, что данные ответов были обновлены правильно
        updated_answers = response.data['updated_answers']
        self.assertEqual(len(updated_answers), len(answers_data))
        for updated_answer, answer_data in zip(updated_answers, answers_data):
            # Проверяем, что атрибут hint_used был установлен
            self.assertTrue(all(updated_answer.get('hint_used', False) for updated_answer in updated_answers), "No hint was used")

class OneCorrectAnswerTestCase(TestCase):
    def setUp(self):
        # Создаем тестового пользователя
        self.user = User.objects.create(username='testuser', points=100, tips_first_type=0, tips_second_type=0)

    def test_one_correct_answer(self):
        # Тестовые данные ответов
        answers_data = [
            {'text': 'Answer 1', 'is_correct': False, 'used': False},
            {'text': 'Answer 2', 'is_correct': True, 'used': False},
            {'text': 'Answer 3', 'is_correct': False, 'used': False},
            {'text': 'Answer 4', 'is_correct': False, 'used': False}
        ]

        # Устанавливаем атрибут used для всех ответов в False
        for answer_data in answers_data:
            answer_data['used'] = False

        # Вызываем функцию OneCorrectAnswer
        updated_answers = OneCorrectAnswer(answers_data, self.user)

        # Проверяем, что только один правильный ответ остался неиспользованным
        correct_answers = [answer for answer in updated_answers if answer['is_correct'] and not answer['used']]
        self.assertEqual(len(correct_answers), 1)

class FiftyFiftyAnswerTestCase(TestCase):
    def setUp(self):
        # Создаем тестового пользователя
        self.user = User.objects.create(username='testuser', points=100, tips_first_type=0, tips_second_type=0)

    def test_fifty_fifty_answer(self):
        # Тестовые данные ответов
        answers_data = [
            {'text': 'Answer 1', 'is_correct': False, 'used': False},
            {'text': 'Answer 2', 'is_correct': True, 'used': False},
            {'text': 'Answer 3', 'is_correct': False, 'used': False},
            {'text': 'Answer 4', 'is_correct': False, 'used': False}
        ]

        # Устанавливаем атрибут used для всех ответов в False
        for answer_data in answers_data:
            answer_data['used'] = False

        # Вызываем функцию FiftyFiftyAnswer
        updated_answers = FiftyFiftyAnswer(answers_data, self.user)

        # Проверяем, что остались два ответа, один из которых правильный
        correct_answers = [answer for answer in updated_answers if answer['is_correct'] and not answer['used']]
        self.assertEqual(len(correct_answers), 1)

        unused_answers = [answer for answer in updated_answers if not answer['used']]
        self.assertEqual(len(unused_answers), 2)