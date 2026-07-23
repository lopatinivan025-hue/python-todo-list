import json
from pathlib import Path


def load_tasks(file_path: str = "tasks.json") -> list[dict]:
    """Загружает список словарей из JSON-файла.

    Если файл отсутствует, возвращает пустой список.
    Если у пользователя нет прав доступа, выводит понятную ошибку.
    """
    path = Path(file_path)

    try:
        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)

        if isinstance(data, list):
            return data
        return []

    except FileNotFoundError:
        return []
    except PermissionError:
        print(f"Ошибка доступа: у вас нет прав на чтение файла '{path}'.")
        return []
    except json.JSONDecodeError:
        print(f"Ошибка: файл '{path}' содержит некорректный JSON.")
        return []


def save_tasks(tasks: list[dict], file_path: str = "tasks.json") -> bool:
    """Сохраняет список словарей в JSON-файл.

    Возвращает True при успешной записи и False при ошибке доступа.
    """
    path = Path(file_path)

    try:
        with path.open("w", encoding="utf-8") as file:
            json.dump(tasks, file, ensure_ascii=False, indent=2)
        return True

    except PermissionError:
        print(f"Ошибка доступа: у вас нет прав на запись файла '{path}'.")
        return False


def input_future_date() -> str:
    """Просит пользователя ввести дату в формате ДД.ММ.ГГГГ.

    Если дата введена неверно или уже прошла, функция просит
    ввести её заново до тех пор, пока не будет введена корректная
    будущая дата.
    """
    from datetime import datetime

    while True:
        date_str = input("Введите дату в формате ДД.ММ.ГГГГ: ")

        try:
            entered_date = datetime.strptime(date_str, "%d.%m.%Y").date()
        except ValueError:
            print("Ошибка: введите дату в формате ДД.ММ.ГГГГ.")
            continue

        today = datetime.today().date()
        if entered_date < today:
            print("Ошибка: дата уже прошла. Введите сегодняшнюю или будущую дату.")
            continue

        return date_str


def delete_task_by_index(tasks: list[dict], index: int) -> None:
    """Удаляет задачу из списка по индексу после подтверждения пользователя."""
    confirmation = input("Вы уверены, что хотите удалить задачу? (y/n): ").strip().lower()

    if confirmation == "n":
        print("Удаление отменено.")
        return

    if 0 <= index < len(tasks):
        removed_task = tasks.pop(index)
        print(f"Задача удалена: {removed_task}")
    else:
        print("Ошибка: неверный индекс задачи.")


def get_valid_priority() -> str:
    """Запрашивает приоритет, пока не будет введено правильное слово."""
    valid = ['высокий', 'средний', 'низкий']
    while True:
        p = input("Введите приоритет (высокий/средний/низкий): ").strip().lower()
        if p in valid:
            return p
        print("Ошибка: Выберите из предложенных вариантов.")

def add_task(tasks: list[dict]):
    """Собирает данные у пользователя и добавляет задачу в список."""
    print("\n--- Добавление задачи ---")
    title = input("Название задачи: ").strip()
    while not title:
        print("Название не может быть пустым!")
        title = input("Название задачи: ").strip()

    description = input("Описание (можно оставить пустым): ")
    # Здесь мы вызываем твою функцию проверки даты!
    deadline = input_future_date() 
    priority = get_valid_priority()

    # Упаковываем все ответы в один словарь (в одни фигурные скобки)
    task = {
        'title': title,
        'description': description,
        'deadline': deadline,
        'priority': priority,
        'status': 'активна'
    }
    tasks.append(task)
    save_tasks(tasks) # Вызываем твою функцию сохранения
    print("Задача успешно добавлена!")

def display_tasks(tasks: list[dict], filter_type: str = 'все'):
    """Показывает задачи на экране и сортирует их."""
    if not tasks:
        print("Список задач пуст.")
        return

    # Вот те самые словари для сортировки! Мы учим программу понимать важность слов.
    priority_weight = {'высокий': 1, 'средний': 2, 'низкий': 3}
    status_weight = {'активна': 1, 'выполнена': 2}

    from datetime import datetime
    # Сортировка: сначала по дате, потом по приоритету, потом по статусу
    sorted_tasks = sorted(tasks, key=lambda x: (
        datetime.strptime(x['deadline'], "%d.%m.%Y").date(),
        priority_weight[x['priority']],
        status_weight[x['status']]
    ))

    print(f"\n--- Список задач ({filter_type}) ---")
    for idx, task in enumerate(sorted_tasks):
        if filter_type == 'активные' and task['status'] == 'выполнена':
            continue
        if filter_type == 'выполненные' and task['status'] == 'активна':
            continue

        mark = "[x]" if task['status'] == 'выполнена' else "[ ]"
        print(f"{idx + 1}. {mark} {task['title']} | Дедлайн: {task['deadline']} | Приоритет: {task['priority']}")

def complete_task(tasks: list[dict]):
    """Отмечает задачу как выполненную."""
    display_tasks(tasks, 'активные')
    if not tasks: 
        return

    try:
        idx = int(input("\nВведите номер задачи для отметки выполнения: ")) - 1
        if 0 <= idx < len(tasks):
            tasks[idx]['status'] = 'выполнена'
            save_tasks(tasks)
            print("Задача отмечена как выполненная!")
        else:
            print("Неверный номер.")
    except ValueError:
        print("Введите число.")

def main():
    """ГЛАВНОЕ МЕНЮ ПРОГРАММЫ"""
    tasks = load_tasks() # Загружаем задачи твоей функцией при запуске
    
    while True:
        print("\n=== Менеджер задач ===")
        print("1. Добавить задачу")
        print("2. Показать все задачи")
        print("3. Показать активные задачи")
        print("4. Отметить как выполненную")
        print("5. Удалить задачу")
        print("6. Выход")

        choice = input("Выберите действие (1-6): ").strip()

        if choice == '1':
            add_task(tasks)
        elif choice == '2':
            display_tasks(tasks, 'все')
        elif choice == '3':
            display_tasks(tasks, 'активные')
        elif choice == '4':
            complete_task(tasks)
        elif choice == '5':
            display_tasks(tasks, 'все')
            if tasks:
                try:
                    idx = int(input("\nВведите номер задачи для удаления: ")) - 1
                    # Вызываем твою функцию удаления
                    delete_task_by_index(tasks, idx) 
                    save_tasks(tasks)
                except ValueError:
                    print("Введите число.")
        elif choice == '6':
            print("До свидания!")
            break
        else:
            print("Неизвестная команда. Введите цифру от 1 до 6.")

# Эта строчка говорит Питону: "Запусти функцию main() прямо сейчас"
if __name__ == "__main__":
    main()