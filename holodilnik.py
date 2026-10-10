import datetime
from decimal import Decimal

DATE_FORMAT = '%Y-%m-%d'

# Холодильник пуст
goods = {}

def add(items, title, amount, expiration_date=None):
    """

    Код, который добавляет продукты в словарь goods.

    Args:
        items (dict): Словарь, который хранит список продуктов
        title (str): Название добавляемого продукта
        amount (float): Количество добавляемого продукта
        expiration_date (str): Срок годности добавляемого продукта,
                                необязательный параметр

    Returns:
        Функция добавляет в словать goods новые данные
        и ничего не возвращает

    Raises:
        ValueError: Если введены данные не правильного формата
    """
    if title not in items:
        items[title] = []
    if expiration_date is not None:
        expiration_date = datetime.datetime.strptime(
            expiration_date, DATE_FORMAT
        ).date()
    items[title].append({'amount': amount, 'expiration_date': expiration_date})


def add_by_note(items, note):
    """

    Разбирает строку вида '<название> <количество> <срок годности>'
    и добавляет продукт в словарь goods.

    Args:
        items (dict): Словарь, который хранит список продуктов
        note (str): Строка с информацией о продукте

    Returns:
        Функция добавляет в словать goods новые данные
        и ничего не возвращает

    Raises:
        ValueError: Если введены данные не правильного формата
    """
    parts = note.split(' ')
    # Последняя часть — дата, если она состоит из трёх частей через дефис
    if len(parts[-1].split('-')) == 3:
        expiration_date = parts[-1]
        amount = Decimal(parts[-2])
        title = ' '.join(parts[:-2])
    else:
        expiration_date = None
        amount = Decimal(parts[-1])
        title = ' '.join(parts[:-1])
    add(items, title, amount, expiration_date)


def find(items, needle):
    """

    Возвращает список названий продуктов, содержащих исходную строку.

    Args:
        items (dict): Словарь, который хранит список продуктов
        needle (str): Строка, по которой осуществляется поиск
                        без учета регистра

    Returns:
        Функция возвращает список с названиями продуктов,
        которые содержат искомую строку

    Raises:
        ValueError: Если введены данные не правильного формата
    """
    result = []
    for title in items:
        if needle.lower() in title.lower():
            result.append(title)
    return result

def amount(items, needle):
    """

    Возвращает общее количество продуктов,
    в названии которых есть искомая строка.

    Args:
        items (dict): Словарь, который хранит список продуктов
        needle (str): Строка, по которой осуществляется поиск
                        без учета регистра

    Returns:
        Функция возвращает общее количество запрошенного продукта

    Raises:
        ValueError: Если введены данные не правильного формата
    """
    total = Decimal('0')
    for title in find(items, needle):
        for batch in items[title]:
            total += batch['amount']
    return total


# Тесты
fridge = {}

add(fridge, 'Яйца', Decimal('10'), '2023-9-30')
add(fridge, 'Яйца', Decimal('3'), '2023-10-15')   # вторая партия
add(fridge, 'Вода', Decimal('2.5'))               # без срока годности
add(fridge, 'Сыр', Decimal('0.3'), '2123-01-01')  # через сто лет
print(fridge)

add_by_note(fridge, 'Яйца страуса 4 2023-07-15')
add_by_note(fridge, 'Хлеб белый 1')         # без даты
add_by_note(fridge, 'Яйца 2 2023-11-01')          # уже есть в словаре
add_by_note(fridge, 'Пельмени с рыбой 2 2023-9-15')
add_by_note(fridge, 'Пельмени с рыбой 0.5 2023-10-1')
add_by_note(fridge, 'Вода 1.5')
print(fridge)

print(find(fridge, 'йц'))      # ['Яйца', 'Яйца страуса']
print(find(fridge, 'ХЛЕБ'))    # ['Хлеб белый']
print(find(fridge, 'молоко'))  # []

print(amount(fridge, 'яйца'))  # 10 + 3 + 2 + 4 = 19
print(amount(fridge, 'вода'))  # 4
print(amount(fridge, 'молоко'))  # 0