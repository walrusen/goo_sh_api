import gspread
from oauth2client.service_account import ServiceAccountCredentials
import logging

# Настраиваем логирование
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class GoogleSheetManager:
    """Класс для работы с Google Sheets через API gspread."""

    def __init__(self, credentials_path, sheet_id, sheet_name):
        """
        Инициализация класса и авторизация в Google Sheets.

        :param credentials_path: путь к JSON-файлу с учетными данными
        :param sheet_id: ID таблицы Google Sheets
        :param sheet_name: имя листа в таблице
        """
        self.credentials_path = credentials_path
        self.sheet_id = sheet_id
        self.sheet_name = sheet_name
        self.client = self.authenticate_google_sheets()  # Авторизация при создании объекта
        self.worksheet = self.get_worksheet()  # Получаем лист таблицы

    def authenticate_google_sheets(self):
        """Авторизация в Google API и получение клиента gspread."""
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive.file",
            "https://www.googleapis.com/auth/drive"
        ]
        creds = ServiceAccountCredentials.from_json_keyfile_name(self.credentials_path, scope)
        return gspread.authorize(creds)

    def get_worksheet(self):
        """Получает объект листа таблицы Google Sheets."""
        try:
            spreadsheet = self.client.open_by_key(self.sheet_id)
            return spreadsheet.worksheet(self.sheet_name)
        except Exception as e:
            logging.error(f"Ошибка при открытии таблицы: {e}")
            return None

    def fetch_sheet_data(self):
        """Получает заголовки и данные из Google Sheets."""
        if not self.worksheet:
            return [], []

        try:
            raw_headers = self.worksheet.get_values("A1:Z1")
            clean_headers = [header.replace("\n", "") for header in raw_headers[0]] if raw_headers else []
            data_rows = self.worksheet.get_values("A2:Z")
            return clean_headers, data_rows
        except Exception as e:
            logging.error(f"Ошибка при получении данных: {e}")
            return [], []

    def process_headers(self, raw_headers):
        """Обрабатывает заголовки, добавляя индексы к дубликатам."""
        counter = {}
        all_headers = []
        for item in raw_headers:
            if not item:
                continue
            if item in counter:
                counter[item] += 1
                all_headers.append(f"{item} {counter[item]}")
            else:
                counter[item] = 1
                all_headers.append(f"{item} {counter[item]}" if raw_headers.count(item) > 1 else item)
        return all_headers

    def group_orders(self, data_list, all_headers):
        """Группирует данные по заказам, объединяя товары в списки."""
        order_headers = [
            "Администратор", "Номер заказа", "ДАТА", "Промежуток времени",
            "Заказчик (Instagram/WhatsApp)", "Комментарий к заказу/доплата",
            "Имя получателя", "Номер телефона получателя",
            "Полный адрес доставки", "Доставка/самовывоз",
            "Район", "Машина", "Цена 1"
        ]
        product_headers = ["Наименование товара", "Цена 2", "Заметка к товару"]

        data_dicts = [dict(zip(all_headers, row)) for row in data_list]

        grouped_orders = []
        current_order = None
        last_order_id = None
        last_order_date = None

        for row in data_dicts:
            order_id = row.get("Номер заказа", "").strip()
            order_date = row.get("ДАТА", "").strip()

            if not order_date:
                order_date = last_order_date

            if order_id and order_id != last_order_id:
                if current_order:
                    grouped_orders.append(current_order)

                current_order = {key: row.get(key, "") for key in order_headers}
                current_order["ДАТА"] = order_date
                current_order["Товары"] = []
                last_order_id = order_id
                last_order_date = order_date

            if current_order:
                product = {key: row.get(key, "") for key in product_headers}
                if any(product.values()):
                    current_order["Товары"].append(product)

        if current_order:
            grouped_orders.append(current_order)

        return grouped_orders

    def get_orders(self):
        """Основной метод: загружает данные, обрабатывает их и возвращает заказы."""
        logging.info("Получение данных из Google Sheets...")
        raw_headers, data_rows = self.fetch_sheet_data()

        if not raw_headers or not data_rows:
            logging.warning("Данные не загружены.")
            return []

        logging.info("Обработка заголовков...")
        all_headers = self.process_headers(raw_headers)

        logging.info("Группировка заказов...")
        grouped_orders = self.group_orders(data_rows, all_headers)

        logging.info(f"Обработано {len(grouped_orders)} заказов.")
        return grouped_orders
