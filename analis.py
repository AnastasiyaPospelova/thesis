from server import (get_answers_list_theory1, get_answers_listt_theory1, get_answers_list_theory2, 
                    get_answers_listt_theory2, get_answers_list_theory3, get_answers_listt_theory3, 
                    get_answers_list_theory4, get_answers_listt_theory4, get_answers_list_logic, get_answers_listt_logic)
from priorities import get_priorities as get_priorities_from_module

def get_correct_answers_count_theory1(id_candidate):
    try:
        # Получаем ответы кандидата
        success, candidate_answers = get_answers_list_theory1(id_candidate)
        if not success:
            return False, candidate_answers  # Возвращаем ошибку
            
        # Получаем правильные ответы
        success, correct_answers = get_answers_listt_theory1()
        if not success:
            return False, correct_answers  # Возвращаем ошибку
            
        # Считаем количество правильных ответов
        correct_count = 0
        for candidate_answer, correct_answer in zip(candidate_answers, correct_answers):
            if candidate_answer[1] == correct_answer:  # candidate_answer[1] - это ответ кандидата
                correct_count += 1
                
        return True, correct_count
            
    except Exception as error:
        return False, str(error)

def get_correct_answers_count_theory2(id_candidate):
    try:
        # Получаем ответы кандидата
        success, candidate_answers = get_answers_list_theory2(id_candidate)
        if not success:
            return False, candidate_answers  # Возвращаем ошибку
            
        # Получаем правильные ответы
        success, correct_answers = get_answers_listt_theory2()
        if not success:
            return False, correct_answers  # Возвращаем ошибку
            
        # Считаем количество правильных ответов
        correct_count = 0
        for candidate_answer, correct_answer in zip(candidate_answers, correct_answers):
            if candidate_answer[1] == correct_answer:  # candidate_answer[1] - это ответ кандидата
                correct_count += 1
                
        return True, correct_count
            
    except Exception as error:
        return False, str(error)

def get_correct_answers_count_theory3(id_candidate):
    try:
        # Получаем ответы кандидата
        success, candidate_answers = get_answers_list_theory3(id_candidate)
        if not success:
            return False, candidate_answers  # Возвращаем ошибку
            
        # Получаем правильные ответы
        success, correct_answers = get_answers_listt_theory3()
        if not success:
            return False, correct_answers  # Возвращаем ошибку
            
        # Считаем количество правильных ответов
        correct_count = 0
        for candidate_answer, correct_answer in zip(candidate_answers, correct_answers):
            if candidate_answer[1] == correct_answer:  # candidate_answer[1] - это ответ кандидата
                correct_count += 1
                
        return True, correct_count
            
    except Exception as error:
        return False, str(error)

def get_correct_answers_count_theory4(id_candidate):
    try:
        # Получаем ответы кандидата
        success, candidate_answers = get_answers_list_theory4(id_candidate)
        if not success:
            return False, candidate_answers  # Возвращаем ошибку
            
        # Получаем правильные ответы
        success, correct_answers = get_answers_listt_theory4()
        if not success:
            return False, correct_answers  # Возвращаем ошибку
            
        # Считаем количество правильных ответов
        correct_count = 0
        for candidate_answer, correct_answer in zip(candidate_answers, correct_answers):
            if candidate_answer[1] == correct_answer:  # candidate_answer[1] - это ответ кандидата
                correct_count += 1
                
        return True, correct_count
            
    except Exception as error:
        return False, str(error)

def get_correct_answers_count_logic(id_candidate):
    try:
        # Получаем ответы кандидата
        success, candidate_answers = get_answers_list_logic(id_candidate)
        if not success:
            return False, candidate_answers  # Возвращаем ошибку
            
        # Получаем правильные ответы
        success, correct_answers = get_answers_listt_logic()
        if not success:
            return False, correct_answers  # Возвращаем ошибку
            
        # Считаем количество правильных ответов
        correct_count = 0
        for candidate_answer, correct_answer in zip(candidate_answers, correct_answers):
            if candidate_answer[1] == correct_answer:  # candidate_answer[1] - это ответ кандидата
                correct_count += 1
                
        return True, correct_count
            
    except Exception as error:
        return False, str(error)

def get_priorities():
    try:
        # Получаем приоритеты из модуля priorities
        return get_priorities_from_module()
    except Exception as error:
        return False, str(error)

def geometric_mean(numbers):
    product = 1
    for num in numbers:
        product *= num
    return product ** (1/len(numbers))

def final_prioritees(vector):
    sum_vector = sum(vector)
    for i in range(len(vector)):
        vector[i] = vector[i] / sum_vector
    return vector

def get_candidate_score(id_candidate):
    try:
        print(f"\nРасчет score для кандидата {id_candidate}:")
        
        priorities = get_priorities()
        print(f"Полученные приоритеты: {priorities}")
        
        if isinstance(priorities, tuple) and not priorities[0]:
            return False, priorities[1]
        
        vector_priorities = []
        for row in priorities:
            mean = geometric_mean(row)
            print(f"Геометрическое среднее для строки {row}: {mean}")
            vector_priorities.append(mean)
        
        vector_priorities = final_prioritees(vector_priorities)
        print(f"Нормализованные приоритеты: {vector_priorities}")

        # Получаем результаты тестов
        test_results = [
            get_correct_answers_count_theory1(id_candidate),
            get_correct_answers_count_theory2(id_candidate),
            get_correct_answers_count_theory3(id_candidate),
            get_correct_answers_count_theory4(id_candidate),
            get_correct_answers_count_logic(id_candidate)
        ]
        
        print(f"Результаты тестов: {test_results}")
        
        # Проверяем успешность получения ответов и извлекаем количество правильных ответов
        correct_answers = []
        for success, count in test_results:
            if not success:
                print(f"Ошибка при получении результатов теста: {count}")
                return False, count
            correct_answers.append(count)
        
        print(f"Количество правильных ответов: {correct_answers}")
        
        # Вычисляем итоговый score
        score = 0
        for i in range(5):
            score += vector_priorities[i] * correct_answers[i]
            print(f"Вклад теста {i+1}: {vector_priorities[i]} * {correct_answers[i]} = {vector_priorities[i] * correct_answers[i]}")
        
        print(f"Итоговый score: {score}")
        return True, score
    except Exception as error:
        print(f"Ошибка при расчете score: {str(error)}")
        return False, str(error)
    
