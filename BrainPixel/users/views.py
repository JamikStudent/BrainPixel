from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import *
from .serializers import *
from .utils import OneCorrectAnswer, FiftyFiftyAnswer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

# Представление для получения списка пользователей
class UserAPIView(generics.ListAPIView):
    # Определение запроса к базе данных для получения списка всех пользователей
    queryset = User.objects.all()

    # Определение класса сериализатора для преобразования данных пользователя в JSON
    serializer_class = UserSerializer

# Представление для создания нового пользователя
@api_view(['POST'])
def create_user(request):
    # Проверяем, были ли переданы данные формы в запросе
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        # Сохраняем нового пользователя, если данные формы валидны
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    # Возвращаем сообщение об ошибке, если данные формы невалидны
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Представление для получения информации о пользователе по его идентификатору
@api_view(['GET'])
def get_user(request, user_id):
    try:
        # Получаем пользователя по его идентификатору из базы данных
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        # Возвращаем сообщение об ошибке, если пользователь не найден
        return Response(status=status.HTTP_404_NOT_FOUND)

    # Возвращаем информацию о пользователе
    serializer = UserSerializer(user)
    return Response(serializer.data)

# Представление для проверки баланса пользователя
@api_view(['GET'])
def check_balance(request, user_id):
    try:
        # Получаем пользователя по его идентификатору из базы данных
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        # Возвращаем сообщение об ошибке, если пользователь не найден
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    # Возвращаем текущий баланс пользователя
    return Response({'balance': user.coin})

@api_view(['GET'])
def buy_tips(request, user_id, type_of_tip):
    try:
        # Получаем пользователя по его идентификатору из базы данных
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        # Возвращаем сообщение об ошибке, если пользователь не найден
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    # Рассчитываем стоимость одной подсказки
    cost_per_tip = 50 if type_of_tip == 'first' else 100

    # Проверяем, достаточно ли у пользователя баллов для покупки подсказки
    if user.coin < cost_per_tip:
        return Response({'error': 'Insufficient coin'}, status=status.HTTP_400_BAD_REQUEST)

    # Вычитаем баллы у пользователя и добавляем подсказку в его аккаунт
    if type_of_tip == 'first':
        user.tips_first_type += 1
    else:
        user.tips_second_type += 1
    user.coin -= cost_per_tip
    user.save()

    # Возвращаем сообщение об успешной покупке подсказки и информацию о текущем балансе
    return Response({
        'message': f'Tip of the {type_of_tip} type bought successfully',
        'num_of_tips': user.tips_first_type if type_of_tip == 'first' else user.tips_second_type,
        'balance': user.coin
    })

@api_view(['POST'])  # Представление должно принимать POST-запросы
def buy_skin(request, user_id, skin_name):
    try:
        # Получаем пользователя по его идентификатору из базы данных
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        # Возвращаем сообщение об ошибке, если пользователь не найден
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    # Проверяем, доступна ли тема для покупки
    if skin_name not in ['pink', 'green']:
        return Response({'error': 'Invalid skin name'}, status=status.HTTP_400_BAD_REQUEST)

    # Проверяем, достаточно ли у пользователя баллов для покупки темы
    if skin_name == 'pink' and user.coin < 100:  # Устанавливаем цену для розовой темы в 200 баллов
        return Response({'error': 'Insufficient coin'}, status=status.HTTP_400_BAD_REQUEST)
    elif skin_name == 'green' and user.coin < 100:  # Устанавливаем цену для зеленой темы в 300 баллов
        return Response({'error': 'Insufficient coin'}, status=status.HTTP_400_BAD_REQUEST)

    # Вычитаем баллы у пользователя и добавляем информацию о покупке темы
    if skin_name == 'pink':
        user.coin -= 100
        user.skin_p = True
    elif skin_name == 'green':
        user.coin -= 100
        user.skin_g = True
    user.skin = skin_name
    user.save()

    # Возвращаем сообщение об успешной покупке темы и информацию о текущем балансе
    return Response({
        'message': f'Skin {skin_name} bought successfully',
        'balance': user.coin
    })

@api_view(['GET'])
def user_skin_info(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    data = {
        'skin': user.skin,
        'skin_b': user.skin_b,
        'skin_p': user.skin_p,
        'skin_g': user.skin_g,
    }

    return Response(data, status=status.HTTP_200_OK)

@api_view(['POST'])
def change_skin(request, user_id, skin_name):
    try:
        # Получаем пользователя по его идентификатору из базы данных
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        # Возвращаем сообщение об ошибке, если пользователь не найден
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    # Проверяем, есть ли такой скин у пользователя
    if getattr(user, f'skin_{skin_name}', False):
        # Обновляем скин пользователя
        user.skin = skin_name
        user.save()
        return Response({'message': f'Successfully changed skin to {skin_name}'}, status=status.HTTP_200_OK)
    else:
        return Response({'error': f'Skin {skin_name} is not available for this user'}, status=status.HTTP_400_BAD_REQUEST)

# Представление для использования подсказок
@api_view(['GET'])
def use_hints_view(request):
    # Получаем данные ответов из запроса
    answers_data = request.data.get('answers')

    # Проверяем, что предоставлен список корректных ответов
    if not answers_data or not isinstance(answers_data, list):
        return Response({'error': 'Invalid answers data'}, status=status.HTTP_400_BAD_REQUEST)

    # Получаем идентификатор пользователя из запроса
    user_id = request.data.get('user_id')

    # Проверяем, что предоставлен идентификатор пользователя
    if not user_id:
        return Response({'error': 'User ID is missing'}, status=status.HTTP_400_BAD_REQUEST)

    # Получаем пользователя из базы данных
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    # Передаем данные ответов в функцию для использования подсказок первого типа
    updated_answers = OneCorrectAnswer(answers_data, user)

    # Передаем данные ответов в функцию для использования подсказок второго типа
    updated_answers = FiftyFiftyAnswer(updated_answers, user)

    # Возвращаем обновленные данные ответов
    return Response({'updated_answers': updated_answers}, status=status.HTTP_200_OK)

class TopicList(generics.ListAPIView):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer

class QuestionListAPIView(generics.ListAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

class TopicQuestionListAPIView(generics.ListAPIView):
    serializer_class = QuestionSerializer

    def get_queryset(self):
        topic_id = self.kwargs['topic_id']
        return Question.objects.filter(topic_id=topic_id)

class TopicInfoAPIView(APIView):
    def get(self, request, topic_id):
        try:
            topic = Topic.objects.get(pk=topic_id)
            serializer = TopicSerializer(topic)
            return Response(serializer.data)
        except Topic.DoesNotExist:
            return Response({'error': 'Topic does not exist'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def bonus_coin(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    user.coin += 50
    user.save()

    return Response({
        'message': 'Bonus points received successfully',
        'balance': user.coin
    })

@api_view(['POST'])
def submit_answers(request, user_id):
    user = request.user
    data = request.data.get('answers')

    if not data:
        return Response({'error': 'No answers provided'}, status=status.HTTP_400_BAD_REQUEST)

    total_questions = len(data)
    correct_answers = 0

    for answer in data:
        question_id = answer.get('question_id')
        answer_text = answer.get('answer_text')

        try:
            question = Question.objects.get(id=question_id)
        except Question.DoesNotExist:
            return Response({'error': f'Question with id {question_id} does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        if question.answer_true == answer_text:
            correct_answers += 1
            user.coin += 50
            user.save()

    score = (correct_answers / total_questions) * 100

    if score < 50:
        user.has_completed_test = False  # Откат теста
        user.save()
        message = "Your score is less than 50%. Do you want to restart the test?"
    else:
        user.has_completed_test = True  # Успешное завершение теста
        user.save()
        message = "Congratulations! Your score is 50% or higher."

    return Response({"message": message, "score": score}, status=status.HTTP_200_OK)

@api_view(['POST'])
def start_test(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    if user.has_completed_test:
        return Response({'error': 'You have already completed the test'}, status=status.HTTP_403_FORBIDDEN)

    # Логика для начала теста

    return Response({'message': 'Test started'}, status=status.HTTP_200_OK)

