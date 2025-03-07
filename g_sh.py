import gspread
from oauth2client.service_account import ServiceAccountCredentials
import re


def get_data():
    name_list_date = 'Март'




    # Выбор листа
    worksheet = spreadsheet.worksheet(name_list_date)
    raw_headers = worksheet.get_values('A1:Z1')[0]

    counter = {}  # Словарь для учета повторений
    all_headers = [] # Все заголовки отформатированные

    # Добавление номеров для заголовков с ценой, Цена 1, Цена 2 и т.п.
    for item in raw_headers:
        if item == "":  # Удаляем пустые элементы
            continue
        if item in counter:
            counter[item] += 1
            all_headers.append(f"{item} {counter[item]}")
        else:
            counter[item] = 1
            all_headers.append(f"{item} {counter[item]}" if raw_headers.count(item) > 1 else item)  # Нумеруем сразу, если дубликаты есть

    # Обновленные заголовки для заказов, включая 'ДАТА'
    order_headers = ['Администратор', 'Номер заказа', 'ДАТА', 'Промежуток времени',
                     'Заказчик (Instagram/\nWhatsApp)', 'Комментарий к заказу/доплата',
                     'Имя получателя', 'Номер телефона получателя',
                     'Полный адрес доставки', 'Доставка/\nсамовывоз',
                     'Район', 'Машина', 'Цена 1']

    # Убираем символы переноса строки '\n' из заголовков
    #order_headers = [header.replace('\n', '') for header in order_headers]

    # Поля для товаров
    product_headers = ['Наименование товара', 'Цена 2', 'Заметка к товару']

    # Считываем данные
    data_rows = worksheet.get_values("A2:Z500")  # Задаём диапазон в зависимости от количества строк

    # Преобразуем в список словарей с исправленными данными
    data_list = [dict(zip(all_headers, row)) for row in data_rows]

    # Функция для группировки заказов и объединения товаров с логикой обработки пустых дат
    def group_orders():
        grouped_orders = []
        current_order = None
        last_order_id = None
        last_order_date = None  # Переменная для хранения последней даты

        for row in data_list:
            order_id = row.get("Номер заказа", "").strip()
            order_date = row.get("ДАТА", "").strip()

            # Если дата пропущена, присваиваем предыдущую дату
            if not order_date:
                order_date = last_order_date

            # Если встретили новый заказ
            if order_id and order_id != last_order_id:
                if current_order:  # Добавляем предыдущий заказ в список
                    grouped_orders.append(current_order)

                # Создаем новый заказ с пустым списком товаров
                current_order = {key: row.get(key, "") for key in order_headers}
                current_order["ДАТА"] = order_date  # Присваиваем дату
                current_order["Товары"] = []
                last_order_id = order_id
                last_order_date = order_date  # Обновляем последнюю дату

            # Добавляем товар к текущему заказу
            if current_order:
                product = {key: row.get(key, "") for key in product_headers}
                if any(product.values()):  # Добавляем только если есть данные
                    current_order["Товары"].append(product)

        # Добавляем последний заказ в список
        if current_order:
            grouped_orders.append(current_order)

        return grouped_orders


    # Получаем все сгруппированные заказы
    grouped_orders = group_orders()

    # Убираем \n в ключах
    def clean_keys(orders):
        cleaned_orders = []
        for order in orders:
            new_order = {key.replace("\n", ""): value for key, value in order.items()}
            cleaned_orders.append(new_order)
        return cleaned_orders

    grouped_orders = clean_keys(grouped_orders)
    return grouped_orders

g = get_data()
print(g[0])
