import psycopg2
connection = psycopg2.connect(user="postgres",
                              password="Fuckingpassword1",
                              host="127.0.0.1",
                              port="5432",
                              database="candidate_testing_db")
cursor = connection.cursor()
cursor.execute('SET search_path TO main_schema,public')

def add_candidate(fio, age, city, access_code, phone_number):
    try:
        # Находим максимальный существующий номер кандидата и увеличиваем на 1
        cursor.execute('SELECT MAX("ID_candidate") FROM candidates')
        max_number = cursor.fetchone()[0]
        new_number = 1 if max_number is None else max_number + 1
        
        # SQL запрос для вставки новой записи
        insert_query = """
            INSERT INTO candidates ("ID_candidate", fio, age, city, access_code, phone_number)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        record_to_insert = (new_number, fio, age, city, access_code, phone_number)
        
        # Выполняем запрос
        cursor.execute(insert_query, record_to_insert)
        connection.commit()
        return True, access_code
        
    except (Exception, psycopg2.Error) as error:
        connection.rollback()
        return False, str(error)

def add_recruiter(fio, age, city, access_code, phone_number):
    try:
        # Находим максимальный существующий номер рекрутера и увеличиваем на 1
        cursor.execute('SELECT MAX("ID_recruiter") FROM recruiters')
        max_number = cursor.fetchone()[0]
        new_number = 1 if max_number is None else max_number + 1
        
        # SQL запрос для вставки новой записи
        insert_query = """
            INSERT INTO recruiters ("ID_recruiter", fio, age, city, access_code, phone_number)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        record_to_insert = (new_number, fio, age, city, access_code, phone_number)
        
        # Выполняем запрос
        cursor.execute(insert_query, record_to_insert)
        connection.commit()
        return True, access_code
        
    except (Exception, psycopg2.Error) as error:
        connection.rollback()
        return False, str(error)

def get_candidate_id_by_access_code(access_code):
    try:
        # SQL запрос для поиска ID кандидата по коду доступа
        select_query = """
            SELECT "ID_candidate" 
            FROM candidates 
            WHERE access_code = %s
        """
        
        # Выполняем запрос
        cursor.execute(select_query, (access_code,))
        result = cursor.fetchone()
        
        # Если найден кандидат, возвращаем его ID
        if result:
            return True, result[0]
        else:
            return False, "Кандидат с таким кодом доступа не найден"
            
    except (Exception, psycopg2.Error) as error:
        return False, str(error)

def get_recruiter_id_by_access_code(access_code):
    try:
        # SQL запрос для поиска ID рекрутера по коду доступа
        select_query = """
            SELECT "ID_recruiter" 
            FROM recruiters 
            WHERE access_code = %s
        """
        
        # Выполняем запрос
        cursor.execute(select_query, (access_code,))
        result = cursor.fetchone()
        
        # Если найден рекрутер, возвращаем его ID
        if result:
            return True, result[0]
        else:
            return False, "Рекрутер с таким кодом доступа не найден"
            
    except (Exception, psycopg2.Error) as error:
        return False, str(error)

def get_candidate_fio_by_id(id_candidate):
    try:
        # SQL запрос для поиска ФИО кандидата по ID
        select_query = """
            SELECT fio 
            FROM candidates 
            WHERE "ID_candidate" = %s
        """
        
        # Выполняем запрос
        cursor.execute(select_query, (id_candidate,))
        result = cursor.fetchone()
        
        # Если найден кандидат, возвращаем его ФИО
        if result:
            return True, result[0]
        else:
            return False, "Кандидат с таким ID не найден"
            
    except (Exception, psycopg2.Error) as error:
        return False, str(error)

def get_recruiter_fio_by_id(id_recruiter):
    try:
        # SQL запрос для поиска ФИО рекрутера по ID
        select_query = """
            SELECT fio 
            FROM recruiters 
            WHERE "ID_recruiter" = %s
        """
        
        # Выполняем запрос
        cursor.execute(select_query, (id_recruiter,))
        result = cursor.fetchone()
        
        # Если найден рекрутер, возвращаем его ФИО
        if result:
            return True, result[0]
        else:
            return False, "Рекрутер с таким ID не найден"
            
    except (Exception, psycopg2.Error) as error:
        return False, str(error)

def get_candidates_count():
    try:
        # SQL запрос для подсчета всех записей в таблице candidates
        select_query = """
            SELECT COUNT(*)
            FROM candidates
        """
        
        # Выполняем запрос
        cursor.execute(select_query)
        result = cursor.fetchone()
        
        # Возвращаем количество записей
        if result:
            return True, result[0]
        else:
            return False, "Не удалось получить количество кандидатов"
            
    except (Exception, psycopg2.Error) as error:
        return False, str(error)

def delete_candidate_by_id(id_candidate):
    try:
        # SQL запросы для удаления ответов кандидата из всех таблиц с ответами
        delete_answers_queries = [
            """DELETE FROM candidates_answers_theory1 WHERE "ID_candidate" = %s""",
            """DELETE FROM candidates_answers_theory2 WHERE "ID_candidate" = %s""",
            """DELETE FROM candidates_answers_theory3 WHERE "ID_candidate" = %s""",
            """DELETE FROM candidates_answers_theory4 WHERE "ID_candidate" = %s""",
            """DELETE FROM candidates_answers_logic WHERE "ID_candidate" = %s"""
        ]
        
        # Удаляем ответы кандидата из всех таблиц
        for query in delete_answers_queries:
            cursor.execute(query, (id_candidate,))
        
        # SQL запрос для удаления кандидата по ID
        delete_query = """
            DELETE FROM candidates 
            WHERE "ID_candidate" = %s
        """
        
        # Выполняем запрос на удаление кандидата
        cursor.execute(delete_query, (id_candidate,))
        
        # Подтверждаем изменения
        connection.commit()
        
        # Проверяем, была ли удалена запись
        if cursor.rowcount > 0:
            return True, "Кандидат успешно удален"
        else:
            return False, "Кандидат с таким ID не найден"
            
    except (Exception, psycopg2.Error) as error:
        # Откатываем изменения в случае ошибки
        connection.rollback()
        return False, str(error)

def delete_recruiter_by_id(id_recruiter):
    try:
        # SQL запрос для удаления рекрутера по ID
        delete_query = """
            DELETE FROM recruiters 
            WHERE "ID_recruiter" = %s
        """
        
        # Выполняем запрос на удаление рекрутера
        cursor.execute(delete_query, (id_recruiter,))
        
        # Подтверждаем изменения
        connection.commit()
        
        # Проверяем, была ли удалена запись
        if cursor.rowcount > 0:
            return True, "Рекрутер успешно удален"
        else:
            return False, "Рекрутер с таким ID не найден"
            
    except (Exception, psycopg2.Error) as error:
        # Откатываем изменения в случае ошибки
        connection.rollback()
        return False, str(error)

def get_candidate_info_by_id(id_candidate):
    try:
        # SQL запрос для поиска информации о кандидате по ID
        select_query = """
            SELECT fio, city, phone_number
            FROM candidates 
            WHERE "ID_candidate" = %s
        """
        
        # Выполняем запрос
        cursor.execute(select_query, (id_candidate,))
        result = cursor.fetchone()
        
        # Если найден кандидат, возвращаем его данные
        if result:
            return True, {
                'fio': result[0],
                'city': result[1],
                'number': result[2]
            }
        else:
            return False, "Кандидат с таким ID не найден"
            
    except (Exception, psycopg2.Error) as error:
        return False, str(error)

def check_answers_exist_theory1(id_candidate):
    try:
        # SQL запрос для проверки наличия записей для данного кандидата
        select_query = """
            SELECT COUNT(*) 
            FROM candidates_answers_theory1 
            WHERE "ID_candidate" = %s
        """
        
        # Выполняем запрос
        cursor.execute(select_query, (id_candidate,))
        result = cursor.fetchone()
        
        # Если количество записей больше 0, возвращаем True
        if result and result[0] > 0:
            return True, "Записи найдены"
        else:
            return False, "Записи не найдены"
            
    except (Exception, psycopg2.Error) as error:
        return False, str(error)

def check_answers_exist_theory2(id_candidate):
    try:
        # SQL запрос для проверки наличия записей для данного кандидата
        select_query = """
            SELECT COUNT(*) 
            FROM candidates_answers_theory2 
            WHERE "ID_candidate" = %s
        """
        
        # Выполняем запрос
        cursor.execute(select_query, (id_candidate,))
        result = cursor.fetchone()
        
        # Если количество записей больше 0, возвращаем True
        if result and result[0] > 0:
            return True, "Записи найдены"
        else:
            return False, "Записи не найдены"
            
    except (Exception, psycopg2.Error) as error:
        return False, str(error)

def check_answers_exist_theory3(id_candidate):
    try:
        # SQL запрос для проверки наличия записей для данного кандидата
        select_query = """
            SELECT COUNT(*) 
            FROM candidates_answers_theory3 
            WHERE "ID_candidate" = %s
        """
        
        # Выполняем запрос
        cursor.execute(select_query, (id_candidate,))
        result = cursor.fetchone()
        
        # Если количество записей больше 0, возвращаем True
        if result and result[0] > 0:
            return True, "Записи найдены"
        else:
            return False, "Записи не найдены"
            
    except (Exception, psycopg2.Error) as error:
        return False, str(error)

def check_answers_exist_theory4(id_candidate):
    try:
        # SQL запрос для проверки наличия записей для данного кандидата
        select_query = """
            SELECT COUNT(*) 
            FROM candidates_answers_theory4 
            WHERE "ID_candidate" = %s
        """
        
        # Выполняем запрос
        cursor.execute(select_query, (id_candidate,))
        result = cursor.fetchone()
        
        # Если количество записей больше 0, возвращаем True
        if result and result[0] > 0:
            return True, "Записи найдены"
        else:
            return False, "Записи не найдены"
            
    except (Exception, psycopg2.Error) as error:
        return False, str(error)

    try:
        # SQL запрос для получения правильных ответов
        select_query = """
            SELECT correct_answer
            FROM py_theory4
            ORDER BY "ID_question"
        """
        
        # Выполняем запрос
        cursor.execute(select_query)
        results = cursor.fetchall()
        
        # Преобразуем результаты в список чисел
        if results:
            answers = [row[0] for row in results]
            return True, answers
        else:
            return False, "Ответы не найдены"
            
    except (Exception, psycopg2.Error) as error:
        return False, str(error)

def check_answers_exist_logic(id_candidate):
    try:
        # SQL запрос для проверки наличия записей для данного кандидата
        select_query = """
            SELECT COUNT(*) 
            FROM candidates_answers_logic 
            WHERE "ID_candidate" = %s
        """
        
        # Выполняем запрос
        cursor.execute(select_query, (id_candidate,))
        result = cursor.fetchone()
        
        # Если количество записей больше 0, возвращаем True
        if result and result[0] > 0:
            return True, "Записи найдены"
        else:
            return False, "Записи не найдены"
            
    except (Exception, psycopg2.Error) as error:
        return False, str(error)

def get_recruiters_info():
    try:
        # SQL запрос для получения ФИО и телефона всех рекрутеров
        select_query = """
            SELECT fio, phone_number, age, city, access_code
            FROM recruiters
            ORDER BY "ID_recruiter"
        """
        
        # Выполняем запрос
        cursor.execute(select_query)
        results = cursor.fetchall()
        
        # Если найдены рекрутеры, возвращаем список их данных
        if results:
            recruiters = [{'fio': row[0], 'phone_number': row[1], 'age': row[2], 'city': row[3], 'access_code': row[4]} for row in results]
            return True, recruiters
        else:
            return False, "Рекрутеры не найдены"
            
    except (Exception, psycopg2.Error) as error:
        return False, str(error)

def get_recruiters_count():
    try:
        # SQL запрос для подсчета количества рекрутеров
        select_query = """
            SELECT COUNT(*)
            FROM recruiters
        """
        
        # Выполняем запрос
        cursor.execute(select_query)
        result = cursor.fetchone()
        
        # Возвращаем количество рекрутеров
        if result:
            return True, result[0]
        else:
            return False, "Не удалось получить количество рекрутеров"
            
    except (Exception, psycopg2.Error) as error:
        return False, str(error)

def get_answers_list_by_candidate_theory1(id_candidate):
    try:
        # SQL запрос для получения ответов кандидата
        select_query = """
            SELECT answer
            FROM candidates_answers_theory1
            WHERE "ID_candidate" = %s
            ORDER BY "ID_question"
        """
        
        # Выполняем запрос
        cursor.execute(select_query, (id_candidate,))
        results = cursor.fetchall()
        
        # Преобразуем результаты в список чисел
        if results:
            answers = [row[0] for row in results]
            return True, answers
        else:
            return False, "Ответы не найдены"
            
    except (Exception, psycopg2.Error) as error:
        return False, str(error)

def get_answers_list_by_candidate_theory2(id_candidate):
    try:
        # SQL запрос для получения ответов кандидата
        select_query = """
            SELECT answer
            FROM candidates_answers_theory2
            WHERE "ID_candidate" = %s
            ORDER BY "ID_question"
        """
        
        # Выполняем запрос
        cursor.execute(select_query, (id_candidate,))
        results = cursor.fetchall()
        
        # Преобразуем результаты в список чисел
        if results:
            answers = [row[0] for row in results]
            return True, answers
        else:
            return False, "Ответы не найдены"
            
    except (Exception, psycopg2.Error) as error:
        return False, str(error)

def get_answers_list_by_candidate_theory3(id_candidate):
    try:
        # SQL запрос для получения ответов кандидата
        select_query = """
            SELECT answer
            FROM candidates_answers_theory3
            WHERE "ID_candidate" = %s
            ORDER BY "ID_question"
        """
        
        # Выполняем запрос
        cursor.execute(select_query, (id_candidate,))
        results = cursor.fetchall()
        
        # Преобразуем результаты в список чисел
        if results:
            answers = [row[0] for row in results]
            return True, answers
        else:
            return False, "Ответы не найдены"
            
    except (Exception, psycopg2.Error) as error:
        return False, str(error)

def get_answers_list_by_candidate_theory4(id_candidate):
    try:
        # SQL запрос для получения ответов кандидата
        select_query = """
            SELECT answer
            FROM candidates_answers_theory4
            WHERE "ID_candidate" = %s
            ORDER BY "ID_question"
        """
        
        # Выполняем запрос
        cursor.execute(select_query, (id_candidate,))
        results = cursor.fetchall()
        
        # Преобразуем результаты в список чисел
        if results:
            answers = [row[0] for row in results]
            return True, answers
        else:
            return False, "Ответы не найдены"
            
    except (Exception, psycopg2.Error) as error:
        return False, str(error)

def get_answers_list_by_candidate_logic(id_candidate):
    try:
        # SQL запрос для получения ответов кандидата
        select_query = """
            SELECT answer
            FROM candidates_answers_logic
            WHERE "ID_candidate" = %s
            ORDER BY "ID_question"
        """
        
        # Выполняем запрос
        cursor.execute(select_query, (id_candidate,))
        results = cursor.fetchall()
        
        # Преобразуем результаты в список чисел
        if results:
            answers = [row[0] for row in results]
            return True, answers
        else:
            return False, "Ответы не найдены"
            
    except (Exception, psycopg2.Error) as error:
        return False, str(error)

def get_question_by_id_theory1(id_question):
    try:
        # SQL запрос для получения вопроса и вариантов ответа по ID
        select_query = """
            SELECT question, answer1, answer2, answer3, answer4, correct_answer
            FROM py_theory1 
            WHERE "ID_question" = %s
        """
        
        # Выполняем запрос
        cursor.execute(select_query, (id_question,))
        result = cursor.fetchone()
        
        # Если найден вопрос, возвращаем его и варианты ответов
        if result:
            return True, {
                'question': result[0],
                'answer1': result[1], 
                'answer2': result[2],
                'answer3': result[3],
                'answer4': result[4],
                'correct_answer': result[5]
            }
        else:
            return False, "Вопрос с таким ID не найден"
            
    except (Exception, psycopg2.Error) as error:
        return False, str(error)

def get_question_by_id_theory2(id_question):
    try:
        # SQL запрос для получения вопроса и вариантов ответа по ID
        select_query = """
            SELECT question, answer1, answer2, answer3, answer4, correct_answer
            FROM py_theory2 
            WHERE "ID_question" = %s
        """
        
        # Выполняем запрос
        cursor.execute(select_query, (id_question,))
        result = cursor.fetchone()
        
        # Если найден вопрос, возвращаем его и варианты ответов
        if result:
            return True, {
                'question': result[0],
                'answer1': result[1], 
                'answer2': result[2],
                'answer3': result[3],
                'answer4': result[4],
                'correct_answer': result[5]
            }
        else:
            return False, "Вопрос с таким ID не найден"
            
    except (Exception, psycopg2.Error) as error:
        return False, str(error)

def get_question_by_id_theory3(id_question):
    try:
        # SQL запрос для получения вопроса и вариантов ответа по ID
        select_query = """
            SELECT question, answer1, answer2, answer3, answer4, correct_answer
            FROM py_theory3 
            WHERE "ID_question" = %s
        """
        
        # Выполняем запрос
        cursor.execute(select_query, (id_question,))
        result = cursor.fetchone()
        
        # Если найден вопрос, возвращаем его и варианты ответов
        if result:
            return True, {
                'question': result[0],
                'answer1': result[1], 
                'answer2': result[2],
                'answer3': result[3],
                'answer4': result[4],
                'correct_answer': result[5]
            }
        else:
            return False, "Вопрос с таким ID не найден"
            
    except (Exception, psycopg2.Error) as error:
        return False, str(error)

def get_question_by_id_theory4(id_question):
    try:
        # SQL запрос для получения вопроса и вариантов ответа по ID
        select_query = """
            SELECT question, answer1, answer2, answer3, answer4, correct_answer
            FROM py_theory4 
            WHERE "ID_question" = %s
        """
        
        # Выполняем запрос
        cursor.execute(select_query, (id_question,))
        result = cursor.fetchone()
        
        # Если найден вопрос, возвращаем его и варианты ответов
        if result:
            return True, {
                'question': result[0],
                'answer1': result[1], 
                'answer2': result[2],
                'answer3': result[3],
                'answer4': result[4],
                'correct_answer': result[5]
            }
        else:
            return False, "Вопрос с таким ID не найден"
            
    except (Exception, psycopg2.Error) as error:
        return False, str(error)

def get_question_by_id_logic(id_question):
    try:
        # SQL запрос для получения вопроса и вариантов ответа по ID
        select_query = """
            SELECT question, answer1, answer2, answer3, answer4, correct_answer
            FROM logic 
            WHERE "ID_question" = %s
        """
        
        # Выполняем запрос
        cursor.execute(select_query, (id_question,))
        result = cursor.fetchone()
        
        # Если найден вопрос, возвращаем его и варианты ответов
        if result:
            return True, {
                'question': result[0],
                'answer1': result[1], 
                'answer2': result[2],
                'answer3': result[3],
                'answer4': result[4],
                'correct_answer': result[5]
            }
        else:
            return False, "Вопрос с таким ID не найден"
            
    except (Exception, psycopg2.Error) as error:
        return False, str(error)

def save_answer(id_candidate, id_question, answer):
    try:
        # SQL запрос для вставки ответа кандидата
        insert_query = """
            INSERT INTO candidates_answers_theory1 ("ID_candidate", "ID_question", answer)
            VALUES (%s, %s, %s)
        """
        
        # Выполняем запрос
        cursor.execute(insert_query, (id_candidate, id_question, answer))
        connection.commit()
        
        return True, "Ответ успешно сохранен"
            
    except (Exception, psycopg2.Error) as error:
        return False, str(error)

def save_answer_theory2(id_candidate, id_question, answer):
    try:
        # SQL запрос для вставки ответа кандидата
        insert_query = """
            INSERT INTO candidates_answers_theory2 ("ID_candidate", "ID_question", answer)
            VALUES (%s, %s, %s)
        """
        
        # Выполняем запрос
        cursor.execute(insert_query, (id_candidate, id_question, answer))
        connection.commit()
        
        return True, "Ответ успешно сохранен"
            
    except (Exception, psycopg2.Error) as error:
        return False, str(error)

def save_answer_theory3(id_candidate, id_question, answer):
    try:
        # SQL запрос для вставки ответа кандидата
        insert_query = """
            INSERT INTO candidates_answers_theory3 ("ID_candidate", "ID_question", answer)
            VALUES (%s, %s, %s)
        """
        
        # Выполняем запрос
        cursor.execute(insert_query, (id_candidate, id_question, answer))
        connection.commit()
        
        return True, "Ответ успешно сохранен"
            
    except (Exception, psycopg2.Error) as error:
        return False, str(error)

def save_answer_theory4(id_candidate, id_question, answer):
    try:
        # SQL запрос для вставки ответа кандидата
        insert_query = """
            INSERT INTO candidates_answers_theory4 ("ID_candidate", "ID_question", answer)
            VALUES (%s, %s, %s)
        """
        
        # Выполняем запрос
        cursor.execute(insert_query, (id_candidate, id_question, answer))
        connection.commit()
        
        return True, "Ответ успешно сохранен"
            
    except (Exception, psycopg2.Error) as error:
        return False, str(error)

def save_answer_logic(id_candidate, id_question, answer):
    try:
        # SQL запрос для вставки ответа кандидата
        insert_query = """
            INSERT INTO candidates_answers_logic ("ID_candidate", "ID_question", answer)
            VALUES (%s, %s, %s)
        """
        
        # Выполняем запрос
        cursor.execute(insert_query, (id_candidate, id_question, answer))
        connection.commit()
        
        return True, "Ответ успешно сохранен"
            
    except (Exception, psycopg2.Error) as error:
        return False, str(error)

def get_answers_list_theory1(id_candidate):
    try:
        # SQL запрос для получения ответов кандидата
        select_query = """
            SELECT "ID_question", answer 
            FROM candidates_answers_theory1
            WHERE "ID_candidate" = %s
            ORDER BY "ID_question"
        """
        
        # Выполняем запрос
        cursor.execute(select_query, (id_candidate,))
        results = cursor.fetchall()
        
        # Преобразуем результаты в список кортежей
        answers = [(row[0], row[1]) for row in results]
        
        return True, answers
            
    except (Exception, psycopg2.Error) as error:
        return False, str(error)

def get_answers_list_theory2(id_candidate):
    try:
        # SQL запрос для получения ответов кандидата
        select_query = """
            SELECT "ID_question", answer 
            FROM candidates_answers_theory2
            WHERE "ID_candidate" = %s
            ORDER BY "ID_question"
        """
        
        # Выполняем запрос
        cursor.execute(select_query, (id_candidate,))
        results = cursor.fetchall()
        
        # Преобразуем результаты в список кортежей
        answers = [(row[0], row[1]) for row in results]
        
        return True, answers
            
    except (Exception, psycopg2.Error) as error:
        return False, str(error)

def get_answers_list_theory3(id_candidate):
    try:
        # SQL запрос для получения ответов кандидата
        select_query = """
            SELECT "ID_question", answer 
            FROM candidates_answers_theory3
            WHERE "ID_candidate" = %s
            ORDER BY "ID_question"
        """
        
        # Выполняем запрос
        cursor.execute(select_query, (id_candidate,))
        results = cursor.fetchall()
        
        # Преобразуем результаты в список кортежей
        answers = [(row[0], row[1]) for row in results]
        
        return True, answers
            
    except (Exception, psycopg2.Error) as error:
        return False, str(error)

def get_answers_list_theory4(id_candidate):
    try:
        # SQL запрос для получения ответов кандидата
        select_query = """
            SELECT "ID_question", answer 
            FROM candidates_answers_theory4
            WHERE "ID_candidate" = %s
            ORDER BY "ID_question"
        """
        
        # Выполняем запрос
        cursor.execute(select_query, (id_candidate,))
        results = cursor.fetchall()
        
        # Преобразуем результаты в список кортежей
        answers = [(row[0], row[1]) for row in results]
        
        return True, answers
            
    except (Exception, psycopg2.Error) as error:
        return False, str(error)

def get_answers_list_logic(id_candidate):
    try:
        # SQL запрос для получения ответов кандидата
        select_query = """
            SELECT "ID_question", answer 
            FROM candidates_answers_logic
            WHERE "ID_candidate" = %s
            ORDER BY "ID_question"
        """
        
        # Выполняем запрос
        cursor.execute(select_query, (id_candidate,))
        results = cursor.fetchall()
        
        # Преобразуем результаты в список кортежей
        answers = [(row[0], row[1]) for row in results]
        
        return True, answers
            
    except (Exception, psycopg2.Error) as error:
        return False, str(error)

def get_question_text_by_id_theory1(id_question):
    try:
        # SQL запрос для получения текста вопроса по ID
        select_query = """
            SELECT question
            FROM py_theory1 
            WHERE "ID_question" = %s
        """
        
        # Выполняем запрос
        cursor.execute(select_query, (id_question,))
        result = cursor.fetchone()
        
        # Если найден вопрос, возвращаем его текст
        if result:
            return True, result[0]
        else:
            return False, "Вопрос с таким ID не найден"
            
    except (Exception, psycopg2.Error) as error:
        return False, str(error)

def get_question_text_by_id_theory2(id_question):
    try:
        # SQL запрос для получения текста вопроса по ID
        select_query = """
            SELECT question
            FROM py_theory2 
            WHERE "ID_question" = %s
        """
        
        # Выполняем запрос
        cursor.execute(select_query, (id_question,))
        result = cursor.fetchone()
        
        # Если найден вопрос, возвращаем его текст
        if result:
            return True, result[0]
        else:
            return False, "Вопрос с таким ID не найден"
            
    except (Exception, psycopg2.Error) as error:
        return False, str(error)

def get_question_text_by_id_theory3(id_question):
    try:
        # SQL запрос для получения текста вопроса по ID
        select_query = """
            SELECT question
            FROM py_theory3 
            WHERE "ID_question" = %s
        """
        
        # Выполняем запрос
        cursor.execute(select_query, (id_question,))
        result = cursor.fetchone()
        
        # Если найден вопрос, возвращаем его текст
        if result:
            return True, result[0]
        else:
            return False, "Вопрос с таким ID не найден"
            
    except (Exception, psycopg2.Error) as error:
        return False, str(error)

def get_question_text_by_id_theory4(id_question):
    try:
        # SQL запрос для получения текста вопроса по ID
        select_query = """
            SELECT question
            FROM py_theory4 
            WHERE "ID_question" = %s
        """
        
        # Выполняем запрос
        cursor.execute(select_query, (id_question,))
        result = cursor.fetchone()
        
        # Если найден вопрос, возвращаем его текст
        if result:
            return True, result[0]
        else:
            return False, "Вопрос с таким ID не найден"
            
    except (Exception, psycopg2.Error) as error:
        return False, str(error)

def get_question_text_by_id_logic(id_question):
    try:
        # SQL запрос для получения текста вопроса по ID
        select_query = """
            SELECT question
            FROM logic 
            WHERE "ID_question" = %s
        """
        
        # Выполняем запрос
        cursor.execute(select_query, (id_question,))
        result = cursor.fetchone()
        
        # Если найден вопрос, возвращаем его текст
        if result:
            return True, result[0]
        else:
            return False, "Вопрос с таким ID не найден"
            
    except (Exception, psycopg2.Error) as error:
        return False, str(error)

def get_answer_by_id_theory1(id_question, answer_number):
    try:
        # Проверяем корректность номера ответа
        if answer_number not in [1, 2, 3, 4]:
            return False, "Некорректный номер ответа. Допустимые значения: 1, 2, 3, 4"
            
        # SQL запрос для получения конкретного варианта ответа по ID вопроса
        select_query = f"""
            SELECT answer{answer_number}
            FROM py_theory1 
            WHERE "ID_question" = %s
        """
        
        # Выполняем запрос
        cursor.execute(select_query, (id_question,))
        result = cursor.fetchone()
        
        # Если найден ответ, возвращаем его
        if result:
            return True, result[0]
        else:
            return False, "Вопрос с таким ID не найден"
            
    except (Exception, psycopg2.Error) as error:
        return False, str(error)

def get_answer_by_id_theory2(id_question, answer_number):
    try:
        # Проверяем корректность номера ответа
        if answer_number not in [1, 2, 3, 4]:
            return False, "Некорректный номер ответа. Допустимые значения: 1, 2, 3, 4"
            
        # SQL запрос для получения конкретного варианта ответа по ID вопроса
        select_query = f"""
            SELECT answer{answer_number}
            FROM py_theory2 
            WHERE "ID_question" = %s
        """
        
        # Выполняем запрос
        cursor.execute(select_query, (id_question,))
        result = cursor.fetchone()
        
        # Если найден ответ, возвращаем его
        if result:
            return True, result[0]
        else:
            return False, "Вопрос с таким ID не найден"
            
    except (Exception, psycopg2.Error) as error:
        return False, str(error)

def get_answer_by_id_theory3(id_question, answer_number):
    try:
        # Проверяем корректность номера ответа
        if answer_number not in [1, 2, 3, 4]:
            return False, "Некорректный номер ответа. Допустимые значения: 1, 2, 3, 4"
            
        # SQL запрос для получения конкретного варианта ответа по ID вопроса
        select_query = f"""
            SELECT answer{answer_number}
            FROM py_theory3 
            WHERE "ID_question" = %s
        """
        
        # Выполняем запрос
        cursor.execute(select_query, (id_question,))
        result = cursor.fetchone()
        
        # Если найден ответ, возвращаем его
        if result:
            return True, result[0]
        else:
            return False, "Вопрос с таким ID не найден"
            
    except (Exception, psycopg2.Error) as error:
        return False, str(error)

def get_answer_by_id_theory4(id_question, answer_number):
    try:
        # Проверяем корректность номера ответа
        if answer_number not in [1, 2, 3, 4]:
            return False, "Некорректный номер ответа. Допустимые значения: 1, 2, 3, 4"
            
        # SQL запрос для получения конкретного варианта ответа по ID вопроса
        select_query = f"""
            SELECT answer{answer_number}
            FROM py_theory4 
            WHERE "ID_question" = %s
        """
        
        # Выполняем запрос
        cursor.execute(select_query, (id_question,))
        result = cursor.fetchone()
        
        # Если найден ответ, возвращаем его
        if result:
            return True, result[0]
        else:
            return False, "Вопрос с таким ID не найден"
            
    except (Exception, psycopg2.Error) as error:
        return False, str(error)

def get_answer_by_id_logic(id_question, answer_number):
    try:
        # Проверяем корректность номера ответа
        if answer_number not in [1, 2, 3, 4]:
            return False, "Некорректный номер ответа. Допустимые значения: 1, 2, 3, 4"
            
        # SQL запрос для получения конкретного варианта ответа по ID вопроса
        select_query = f"""
            SELECT answer{answer_number}
            FROM logic 
            WHERE "ID_question" = %s
        """
        
        # Выполняем запрос
        cursor.execute(select_query, (id_question,))
        result = cursor.fetchone()
        
        # Если найден ответ, возвращаем его
        if result:
            return True, result[0]
        else:
            return False, "Вопрос с таким ID не найден"
            
    except (Exception, psycopg2.Error) as error:
        return False, str(error)

def check_answers_exist_theory1(id_candidate):
    try:
        # SQL запрос для проверки наличия записей для данного кандидата
        select_query = """
            SELECT COUNT(*) 
            FROM candidates_answers_theory1 
            WHERE "ID_candidate" = %s
        """
        
        # Выполняем запрос
        cursor.execute(select_query, (id_candidate,))
        result = cursor.fetchone()
        
        # Если количество записей больше 0, возвращаем True
        if result and result[0] > 0:
            return True, "Записи найдены"
        else:
            return False, "Записи не найдены"
            
    except (Exception, psycopg2.Error) as error:
        return False, str(error)

def check_answers_exist_theory2(id_candidate):
    try:
        # SQL запрос для проверки наличия записей для данного кандидата
        select_query = """
            SELECT COUNT(*) 
            FROM candidates_answers_theory2 
            WHERE "ID_candidate" = %s
        """
        
        # Выполняем запрос
        cursor.execute(select_query, (id_candidate,))
        result = cursor.fetchone()
        
        # Если количество записей больше 0, возвращаем True
        if result and result[0] > 0:
            return True, "Записи найдены"
        else:
            return False, "Записи не найдены"
            
    except (Exception, psycopg2.Error) as error:
        return False, str(error)

def check_answers_exist_theory3(id_candidate):
    try:
        # SQL запрос для проверки наличия записей для данного кандидата
        select_query = """
            SELECT COUNT(*) 
            FROM candidates_answers_theory3 
            WHERE "ID_candidate" = %s
        """
        
        # Выполняем запрос
        cursor.execute(select_query, (id_candidate,))
        result = cursor.fetchone()
        
        # Если количество записей больше 0, возвращаем True
        if result and result[0] > 0:
            return True, "Записи найдены"
        else:
            return False, "Записи не найдены"
            
    except (Exception, psycopg2.Error) as error:
        return False, str(error)

def check_answers_exist_theory4(id_candidate):
    try:
        # SQL запрос для проверки наличия записей для данного кандидата
        select_query = """
            SELECT COUNT(*) 
            FROM candidates_answers_theory4 
            WHERE "ID_candidate" = %s
        """
        
        # Выполняем запрос
        cursor.execute(select_query, (id_candidate,))
        result = cursor.fetchone()
        
        # Если количество записей больше 0, возвращаем True
        if result and result[0] > 0:
            return True, "Записи найдены"
        else:
            return False, "Записи не найдены"
            
    except (Exception, psycopg2.Error) as error:
        return False, str(error)

def check_answers_exist_logic(id_candidate):
    try:
        # SQL запрос для проверки наличия записей для данного кандидата
        select_query = """
            SELECT COUNT(*) 
            FROM candidates_answers_logic 
            WHERE "ID_candidate" = %s
        """
        
        # Выполняем запрос
        cursor.execute(select_query, (id_candidate,))
        result = cursor.fetchone()
        
        # Если количество записей больше 0, возвращаем True
        if result and result[0] > 0:
            return True, "Записи найдены"
        else:
            return False, "Записи не найдены"
            
    except (Exception, psycopg2.Error) as error:
        return False, str(error)

def get_answers_listt_theory1():
    try:
        # SQL запрос для получения всех правильных ответов из таблицы py_theory1
        select_query = """
            SELECT correct_answer
            FROM py_theory1
            ORDER BY "ID_question"
        """
        
        # Выполняем запрос
        cursor.execute(select_query)
        results = cursor.fetchall()
        
        # Преобразуем результаты в список
        correct_answers = [result[0] for result in results]
        
        return True, correct_answers
            
    except (Exception, psycopg2.Error) as error:
        return False, str(error)

def get_answers_listt_theory2():
    try:
        # SQL запрос для получения всех правильных ответов из таблицы py_theory2
        select_query = """
            SELECT correct_answer
            FROM py_theory2
            ORDER BY "ID_question"
        """
        
        # Выполняем запрос
        cursor.execute(select_query)
        results = cursor.fetchall()
        
        # Преобразуем результаты в список
        correct_answers = [result[0] for result in results]
        
        return True, correct_answers
            
    except (Exception, psycopg2.Error) as error:
        return False, str(error)

def get_answers_listt_theory3():
    try:
        # SQL запрос для получения всех правильных ответов из таблицы py_theory3
        select_query = """
            SELECT correct_answer
            FROM py_theory3
            ORDER BY "ID_question"
        """
        
        # Выполняем запрос
        cursor.execute(select_query)
        results = cursor.fetchall()
        
        # Преобразуем результаты в список
        correct_answers = [result[0] for result in results]
        
        return True, correct_answers
            
    except (Exception, psycopg2.Error) as error:
        return False, str(error)

def get_answers_listt_theory4():
    try:
        # SQL запрос для получения всех правильных ответов из таблицы py_theory4
        select_query = """
            SELECT correct_answer
            FROM py_theory4
            ORDER BY "ID_question"
        """
        
        # Выполняем запрос
        cursor.execute(select_query)
        results = cursor.fetchall()
        
        # Преобразуем результаты в список
        correct_answers = [result[0] for result in results]
        
        return True, correct_answers
            
    except (Exception, psycopg2.Error) as error:
        return False, str(error)

def get_answers_listt_logic():
    try:
        # SQL запрос для получения всех правильных ответов из таблицы logic
        select_query = """
            SELECT correct_answer
            FROM logic
            ORDER BY "ID_question"
        """
        
        # Выполняем запрос
        cursor.execute(select_query)
        results = cursor.fetchall()
        
        # Преобразуем результаты в список
        correct_answers = [result[0] for result in results]
        
        return True, correct_answers
            
    except (Exception, psycopg2.Error) as error:
        return False, str(error)

def reorder_candidate_ids():
    try:
        # Получаем все ID кандидатов и сортируем их
        select_query = """
            SELECT "ID_candidate"
            FROM candidates
            ORDER BY "ID_candidate"
        """
        cursor.execute(select_query)
        old_ids = [row[0] for row in cursor.fetchall()]
        
        # Создаем новый список ID (1, 2, 3, ...)
        new_ids = list(range(1, len(old_ids) + 1))
        
        # Обновляем ID в таблице candidates
        for old_id, new_id in zip(old_ids, new_ids):
            if old_id != new_id:
                # Обновляем ID в таблице candidates
                update_candidate_query = """
                    UPDATE candidates
                    SET "ID_candidate" = %s
                    WHERE "ID_candidate" = %s
                """
                cursor.execute(update_candidate_query, (new_id, old_id))
                
                # Обновляем ID в связанных таблицах
                tables = [
                    "candidates_answers_theory1",
                    "candidates_answers_theory2",
                    "candidates_answers_theory3",
                    "candidates_answers_theory4",
                    "candidates_answers_logic"
                ]
                
                for table in tables:
                    update_answers_query = f"""
                        UPDATE {table}
                        SET "ID_candidate" = %s
                        WHERE "ID_candidate" = %s
                    """
                    cursor.execute(update_answers_query, (new_id, old_id))
        
        # Подтверждаем изменения
        connection.commit()
        return True, "ID кандидатов успешно перенумерованы"
            
    except (Exception, psycopg2.Error) as error:
        # Откатываем изменения в случае ошибки
        connection.rollback()
        return False, str(error)


