from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'coin', 'tips_first_type', 'tips_second_type', 'user_save_topic', 'skin', 'skin_b', 'skin_p', 'skin_g']

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'

class TopicSerializer(serializers.ModelSerializer):
    #questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Topic
        fields = ['id', 'topic_title', 'topic_info', 'topic_question_number']