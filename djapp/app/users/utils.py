from random import shuffle

def OneCorrectAnswer(answers_data, user):
    """
    Функция для оставления только одного правильного ответа из четырех в тесте.

    Args:
        answers_data (list): Список ответов в формате словарей.
            Каждый словарь содержит ключи 'text', 'is_correct' и 'used'.
        user (User): Объект пользователя.

    Returns:
        list: Список обновленных данных ответов.
    """
    # Получаем все ответы из базы данных для данного пользователя (примерно так)
    all_answers = user.answer_set.all()

    # Перемешиваем ответы для предоставления случайного выбора
    shuffle(all_answers)

    # Находим первый правильный ответ в полученных данных
    correct_answer = next((answer for answer in all_answers if answer.is_correct), None)

    # Помечаем его как используемый
    if correct_answer:
        correct_answer.used = True
        correct_answer.save()

    # Обновляем данные ответов
    updated_answers = []
    for answer_data in answers_data:
        if answer_data['text'] == correct_answer.text:
            answer_data['used'] = True
        else:
            answer_data['used'] = False
        updated_answers.append(answer_data)

    return updated_answers

def FiftyFiftyAnswer(answers_data, user):
    """
    Функция для оставления двух ответов в тесте, один из которых правильный,
    а второй - случайный ответ (не обязательно правильный).

    Args:
        answers_data (list): Список ответов в формате словарей.
            Каждый словарь содержит ключи 'text', 'is_correct' и 'used'.
        user (User): Объект пользователя.

    Returns:
        list: Список обновленных данных ответов.
    """
    # Получаем все ответы из базы данных для данного пользователя (примерно так)
    all_answers = user.answer_set.all()

    # Перемешиваем ответы для предоставления случайного выбора
    shuffle(all_answers)

    # Находим первый правильный ответ в полученных данных
    correct_answer = next((answer for answer in all_answers if answer.is_correct), None)

    # Помечаем его как используемый
    if correct_answer:
        correct_answer.used = True
        correct_answer.save()

    # Выбираем случайный ответ (не обязательно правильный)
    random_answer = all_answers[0] if len(all_answers) > 1 else None

    # Помечаем его как используемый
    if random_answer:
        random_answer.used = True
        random_answer.save()

    # Обновляем данные ответов
    updated_answers = []
    for answer_data in answers_data:
        if answer_data['text'] == correct_answer.text or (random_answer and answer_data['text'] == random_answer.text):
            answer_data['used'] = True
        else:
            answer_data['used'] = False
        updated_answers.append(answer_data)

    return updated_answers