# Глобальная переменная для хранения приоритетов
priorities = [[1.0 for _ in range(5)] for _ in range(5)]

def get_priorities():
    return priorities

def set_priorities(new_priorities):
    global priorities
    priorities = new_priorities 