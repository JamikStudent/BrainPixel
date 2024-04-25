from rest_framework import status, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User, Topic, Answer
from .serializers import UserSerializer, TopicSerializer
from .utils import OneCorrectAnswer, FiftyFiftyAnswer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.renderers import JSONRenderer

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
    return Response({'balance': user.points})

# Представление для покупки подсказок
@api_view(['GET', 'POST'])
def buy_tips(request, user_id, type_of_tip):
    try:
        # Получаем пользователя по его идентификатору из базы данных
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        # Возвращаем сообщение об ошибке, если пользователь не найден
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    # Получаем количество подсказок из запроса
    num_of_tips = request.data.get('num_of_tips')

    # Проверяем, было ли передано количество подсказок в запросе
    if num_of_tips is None:
        return Response({'error': 'Number of tips is missing'}, status=status.HTTP_400_BAD_REQUEST)
    elif not isinstance(num_of_tips, int) or num_of_tips <= 0:
        return Response({'error': 'Invalid number of tips'}, status=status.HTTP_400_BAD_REQUEST)

    # Рассчитываем стоимость подсказок
    cost_per_tip = 10 if type_of_tip == 'first' else 15
    total_cost = num_of_tips * cost_per_tip

    # Проверяем, достаточно ли у пользователя баллов для покупки подсказок
    if user.points < total_cost:
        return Response({'error': 'Insufficient points'}, status=status.HTTP_400_BAD_REQUEST)

    # Вычитаем баллы у пользователя и добавляем подсказки в его аккаунт
    if type_of_tip == 'first':
        user.tips_first_type += num_of_tips
    else:
        user.tips_second_type += num_of_tips
    user.points -= total_cost
    user.save()

    # Возвращаем сообщение об успешной покупке подсказок и информацию о текущем балансе
    return Response({
        'message': f'Tips of the {type_of_tip} type bought successfully',
        'num_of_tips': user.tips_first_type if type_of_tip == 'first' else user.tips_second_type,
        'balance': user.points
    })

# Представление для использования подсказок
@api_view(['GET', 'POST'])
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

@api_view(['POST', 'GET'])
def submit_answers(request):
    user = request.user
    data = request.data.get('answers')
    if not data:
        return Response({'error': 'No answers provided'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Обработка данных ответов и сохранение их в базу данных
    for answer_data in data:
        question_id = answer_data.get('question_id')
        answer_text = answer_data.get('answer_text')

        # Проверка наличия данных ответов
        if question_id is None or answer_text is None:
            return Response({'error': 'Invalid answer format'}, status=status.HTTP_400_BAD_REQUEST)

        # Создание и сохранение экземпляра модели Answer
        answer = Answer(user=user, question_id=question_id, text=answer_text)
        answer.save()

    return Response({'success': 'Answers submitted successfully'}, status=status.HTTP_200_OK)

@api_view(['POST'])
def evaluate_answers(request):
    user = request.user  # Получение пользователя из запроса
    user_answers = request.data.get('answers')  # получение ответов пользователя из запроса
    if not user_answers:
        return Response({'error': 'No answers provided'}, status=status.HTTP_400_BAD_REQUEST)

    # Получение правильных ответов из базы данных
    correct_answers = Answer.objects.filter(is_correct=True)
    
    # Инициализация переменной для хранения количества баллов пользователя
    user_score = 0

    # Сравнение ответов пользователя с правильными ответами
    for user_answer in user_answers:
        # Проверка наличия данных ответов
        if 'question_id' not in user_answer or 'answer_text' not in user_answer:
            return Response({'error': 'Invalid answer format'}, status=status.HTTP_400_BAD_REQUEST)

        question_id = user_answer['question_id']
        answer_text = user_answer['answer_text']

        # Проверка правильности ответа пользователя
        if correct_answers.filter(question_id=question_id, text=answer_text).exists():
            user_score += 1  # Увеличение баллов при правильном ответе

    return Response({'user_score': user_score}, status=status.HTTP_200_OK)

@api_view(['POST', 'GET'])
def authenticate_user(request):
    data = request.data
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return Response({'error': 'Username or password is missing'}, status=status.HTTP_400_BAD_REQUEST)
    
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    
    # Генерация или получение токена аутентификации
    token, created = Token.objects.get_or_create(user=user)
    return Response({'token': token.key}, status=status.HTTP_200_OK)