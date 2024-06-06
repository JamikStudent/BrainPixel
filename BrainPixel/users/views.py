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
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    user_data = {
        'username': user.username,
        'user_save_topic': user.user_save_topic,
        'coin': user.coin,
        'tips_first_type': user.tips_first_type,
        'tips_second_type': user.tips_second_type,
        'skin': user.skin,
        'skin_b': user.skin_b,
        'skin_p': user.skin_p,
        'skin_g': user.skin_g,
        'test_num': user.test_num,
    }

    return Response(user_data, status=status.HTTP_200_OK)

# Представление для проверки баланса пользователя
@api_view(['GET'])
def check_balance(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    return Response({'balance': user.coin}, status=status.HTTP_200_OK)

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

@api_view(['POST'])
def buy_skin(request, user_id, skin_name):
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    skin_cost = 150
    if skin_name not in ['pink', 'green']:
        return Response({'error': 'Invalid skin name'}, status=status.HTTP_400_BAD_REQUEST)

    if user.coin < skin_cost:
        return Response({'error': 'Insufficient coin'}, status=status.HTTP_400_BAD_REQUEST)

    if skin_name == 'pink':
        user.coin -= skin_cost
        user.skin_p = True
    elif skin_name == 'green':
        user.coin -= skin_cost
        user.skin_g = True

    user.skin = skin_name
    user.save()

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
        'skin_b': user.skin_b,
        'skin_p': user.skin_p,
        'skin_g': user.skin_g,
    }

    return Response(data, status=status.HTTP_200_OK)

@api_view(['POST'])
def change_skin(request, user_id, skin_name):
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    if getattr(user, f'skin_{skin_name}', False):
        user.skin = skin_name
        user.save()
        return Response({'message': f'Successfully changed skin to {skin_name}'}, status=status.HTTP_200_OK)
    else:
        return Response({'error': f'Skin {skin_name} is not available for this user'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_user_info(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    data = {
        'skin': user.skin,
        'test_num': user.test_num
    }

    return Response(data, status=status.HTTP_200_OK)

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

@api_view(['POST'])
def decrement_first_type_hint(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        if user.tips_first_type > 0:
            user.SubstractClueFirstType()
            return Response({'status': 'Hint used'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'No hints left'}, status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def decrement_second_type_hint(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        if user.tips_second_type > 0:
            user.SubstractClueSecondType()
            return Response({'status': 'Hint used'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'No hints left'}, status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def use_one_correct_hint(request):
    user_id = request.data.get('user_id')
    question_id = request.data.get('question_id')

    try:
        user = User.objects.get(id=user_id)
        question = Question.objects.get(id=question_id)

        if user.tips_first_type > 0:
            user.subtract_clue_first_type()
            return Response({
                'remaining_clues': user.tips_first_type,
                'answers': [question.answer_true]
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'No remaining clues of this type'}, status=status.HTTP_400_BAD_REQUEST)

    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    except Question.DoesNotExist:
        return Response({'error': 'Question not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def use_fifty_fifty_hint(request):
    user_id = request.data.get('user_id')
    question_id = request.data.get('question_id')

    try:
        user = User.objects.get(id=user_id)
        question = Question.objects.get(id=question_id)

        if user.tips_second_type > 0:
            user.subtract_clue_second_type()
            answers = [question.answer_true, question.answer_false_1]  # Оставляем один правильный и один случайный неверный
            return Response({
                'remaining_clues': user.tips_second_type,
                'answers': answers
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'No remaining clues of this type'}, status=status.HTTP_400_BAD_REQUEST)

    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    except Question.DoesNotExist:
        return Response({'error': 'Question not found'}, status=status.HTTP_404_NOT_FOUND)

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
def update_test_num(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    test_num = request.data.get('test_num')
    if test_num is not None:
        user.test_num = test_num
        user.save()
        return Response({'message': 'Test number updated successfully'}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid test number'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def submit_answers(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

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

        if question.answer_true == answer_text:
            correct_answers += 1
            user.coin += 50
            user.save()

    score = (correct_answers / total_questions) * 100

    if score < 50:
        user.test_num -= 1
        user.save()
        message = "Your score is less than 50%. Do you want to restart the test?"
    else:
        user.test_num += 1
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