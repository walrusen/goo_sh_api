import os
import qrcode
from tkinter import (Tk, Label, Entry, Button, messagebox, LabelFrame)
from fpdf import FPDF
from fpdf.enums import XPos, YPos
from tkinter import ttk
import base64
from g_sh import GoogleSheetManager

CREDENTIALS_PATH = "c_path.json"
SHEET_ID = "id"
SHEET_NAME = "Март"


class PDFGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.orders_dict = ''
        self.root.title("PDF Generator")
        self.root.geometry("900x700")
        self.root.resizable(False, True)
        self.save_path = "C:/Users/dgoni/Desktop/ofrabota/oha scripts/8marchPDF"
        self.fields = [

            ("Администратор:", "admin_name", False),
            ("Номер заказа:", "order_number_entry", False),
            ("Дата:", "date_label", False),
            ("Промежуток времени:", "time_interval_entry", False),
            ("Заказчик:", "customer_entry", False),
            ("Комментарий к заказу:", "note_order", False),
            ("Получатель (имя):", "recipient_name_entry", False),
            ("Получатель (номер):", "recipient_number_entry", False),
            ("Адрес:", "address_entry", False),
            ("Доставка/Самовывоз:", "delivery_pickup_entry", False),
            ("Район:", "district_entry", False),
            ("Стоимость доставки:", "delivery_price_entry", False),
        ]

        self.cake = False
        self.balloon = False
        self.flowers = False
        self.toy = False
        self.strawberry = False


        self.data_frame = LabelFrame(root, text="Данные для PDF", padx=20, pady=10)
        self.data_frame.grid(row=0, column=0, padx=20, pady=(30, 10), sticky="nsew", rowspan=2)


        # Убираем галочки и изменяем поля ввода
        for i, (label_text, var_name, _) in enumerate(self.fields, 1):
            Label(self.data_frame, text=label_text).grid(row=i, column=0, padx=10, pady=5, sticky="e")
            setattr(self, var_name, Entry(self.data_frame))
            getattr(self, var_name).grid(row=i, column=1, padx=10, pady=5)

        # Кнопка для загрузки данных заказа
        self.load_order_button = Button(self.data_frame, text="Загрузить заказ", command=self.load_order_data)
        self.load_order_button.grid(row=len(self.fields) + 1, column=0, columnspan=3, pady=10)

        self.generate_button = Button(self.data_frame, text="Генерировать PDF", command=self.generate_pdf)
        self.generate_button.grid(row=len(self.fields) + 2, column=0, columnspan=3, pady=10)

        self.product_frame = LabelFrame(root, text="Наименование товара", padx=20, pady=10)
        self.product_frame.grid(row=0, column=1, padx=20, pady=(30, 10), sticky="nsew")

        self.product_entries = []
        self.add_product_field()

        self.add_product_button = Button(self.product_frame, text="Добавить товар", command=self.add_product_field)
        self.add_product_button.grid(row=0, column=0, padx=10, pady=5)

    def load_order_data(self):
        sheet_manager = GoogleSheetManager(CREDENTIALS_PATH, SHEET_ID, SHEET_NAME)
        orders = sheet_manager.get_orders()
        grouped_orders = orders
        orders_dict = {order['Номер заказа']: order for order in
                   grouped_orders}  # Группируем заказы через функцию из вашего кода
        self.orders_dict = orders_dict
        id_orders = []
        for i in grouped_orders:
            id_orders.append(i.get('Номер заказа'))

        self.cake = False
        self.balloon = False
        self.flowers = False
        self.toy = False
        self.strawberry = False
        self.note = False

        order_number = self.order_number_entry.get().strip()
        if not order_number:
            messagebox.showerror("Ошибка", "Введите номер заказа для загрузки данных.")
            return

        order_data = self.orders_dict.get(order_number)
        if not order_data:
            messagebox.showerror("Ошибка", "Заказ с таким номером не найден.")
            return
        id = order_number

        index_id = 0
        for i in range(len(id_orders)):
            if id == id_orders[i]:
                index_id = i


        dostsam_flag = grouped_orders[index_id].get('Доставка/самовывоз')
        araba_flag = grouped_orders[index_id].get('Машина')
        dostavka = ''
        if dostsam_flag == 'доставка':
            if araba_flag == 'FALSE':
                dostavka = 'Мотоцикл'
            elif araba_flag == 'TRUE':
                dostavka = 'Машина'
        elif dostsam_flag == 'самовывоз':
            dostavka = 'самовывоз'


        for product in order_data.get("Товары", []):
            for key, value in product.items():
                if 'торт' in value.lower():
                    self.cake = True
                if 'шары' in value.lower():
                    self.balloon = True
                if 'цветы' in value.lower():
                    self.flowers = True
                if 'игрушка' in value.lower():
                    self.toy = True
                if 'клубника' in value.lower() or 'финики' in value.lower():
                    self.strawberry = True




        self.initial_values = {
            "admin_name": f"{grouped_orders[index_id].get('Администратор')}",
            "order_number_entry": f"{grouped_orders[index_id].get('Номер заказа')}",
            "date_label": f"{grouped_orders[index_id].get('ДАТА')}.03.2025",
            "time_interval_entry": f"{grouped_orders[index_id].get('Промежуток времени')}",
            "customer_entry": f"{grouped_orders[index_id].get('Заказчик (Instagram/WhatsApp)')}",
            "note_order": f"{grouped_orders[index_id].get('Комментарий к заказу/доплата')}",
            "recipient_name_entry": f"{grouped_orders[index_id].get('Имя получателя')}",
            "recipient_number_entry": f"{grouped_orders[index_id].get('Номер телефона получателя')}",
            "address_entry": f"{grouped_orders[index_id].get('Полный адрес доставки')}",
            "delivery_pickup_entry": f"{dostavka}",
            "district_entry": f"{grouped_orders[index_id].get('Район')}",
            "delivery_price_entry": f"{grouped_orders[index_id].get('Цена 1')}"
        }
        for key, value in self.initial_values.items():
            print(key,value)

       # Заполнение полей данными из заказов
        for field_name, var_name, _ in self.fields:
            order_value = order_data.get(field_name, "")
            getattr(self, var_name).delete(0, 'end')
            getattr(self, var_name).insert(0, order_value)

        # Очистим старые товары и добавим новые
        self.clear_products()
        for product in order_data.get("Товары", []):
            self.add_product_field_from_data(product)
        for i, (label_text, var_name, _) in enumerate(self.fields, 1):
            # Применяем значения по умолчанию
            getattr(self, var_name).insert(0, self.initial_values.get(var_name, ""))
    def add_product_field(self):
        product_name_entry = Entry(self.product_frame)
        product_price_entry = Entry(self.product_frame, width=7)
        product_description_entry = Entry(self.product_frame, width=30)
        row = len(self.product_entries) + 1
        product_name_entry.grid(row=row, column=0, padx=5, pady=5)
        product_price_entry.grid(row=row, column=1, padx=5, pady=5)
        product_description_entry.grid(row=row, column=2, padx=5, pady=5)
        self.product_entries.append((product_name_entry, product_price_entry, product_description_entry))

    def add_product_field_from_data(self, product_data):
        product_name_entry = Entry(self.product_frame)
        product_price_entry = Entry(self.product_frame, width=7)
        product_description_entry = Entry(self.product_frame, width=30)

        product_name_entry.grid(row=len(self.product_entries) + 1, column=0, padx=5, pady=5)
        product_price_entry.grid(row=len(self.product_entries) + 1, column=1, padx=5, pady=5)
        product_description_entry.grid(row=len(self.product_entries) + 1, column=2, padx=5, pady=5)

        product_name_entry.insert(0, product_data.get('Наименование товара', ''))
        product_price_entry.insert(0, product_data.get('Цена 2', ''))
        product_description_entry.insert(0, product_data.get('Заметка к товару', ''))

        self.product_entries.append((product_name_entry, product_price_entry, product_description_entry))

    def clear_products(self):
        for product_name_entry, product_price_entry, product_description_entry in self.product_entries:
            product_name_entry.delete(0, 'end')
            product_price_entry.delete(0, 'end')
            product_description_entry.delete(0, 'end')
        self.product_entries.clear()

    def generate_pdf(self):
        global for_date_label
        data = {var_name: getattr(self, var_name).get().strip() for _, var_name, _ in self.fields}
        order_number = data.get("order_number_entry", "")
        if not order_number:
            messagebox.showerror("Ошибка", "Номер заказа обязателен для генерации PDF.")
            return

        order_number_encode = base64.b64encode(data.get("order_number_entry", "").encode()).decode()
        name_encode = base64.b64encode(data.get('recipient_name_entry','').encode()).decode()
        phone_number_encode = base64.b64encode(data.get("recipient_number_entry", "").encode()).decode()
        address_encode = base64.b64encode(data.get("address_entry", "").encode()).decode()
        qr_text = f"https://walrusen.github.io/base64_dynamic_decoder/?n={name_encode}&p={phone_number_encode}&a={address_encode}&o={order_number_encode}"
        qr = qrcode.make(qr_text)
        qr_path = os.path.join(self.save_path, "qr_code.png")
        qr.save(qr_path)


        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.add_font('ArialUnicodeMS', '', "C:/Users/dgoni/Desktop/ofrabota/oha scripts/14february/ArialUnicodeMS.ttf")


        qr_size = 30  # Размер QR-кода
        pdf.image(qr_path, x=170, y=3, w=qr_size, h=qr_size)  # Координаты правого верхнего угла

        # Путь к папке с картинками
        image_folder = "C:/Users/dgoni/Desktop/ofrabota/oha scripts/14february/"

        # Координаты для первой картинки (левый верхний угол)
        x_start = 10  # Отступ слева
        y_start = 10  # Отступ сверху
        image_size = 6  # Размер каждой картинки
        spacing = 1  # Промежуток между картинками
        if self.cake:
            image_path = f"{image_folder}cake.png"
            pdf.image(image_path, x=x_start, y=y_start, w=image_size, h=image_size)
            x_start += image_size + spacing  # Смещаем вправо
        if self.balloon:
            image_path = f"{image_folder}balloon.png"
            pdf.image(image_path, x=x_start, y=y_start, w=image_size, h=image_size)
            x_start += image_size + spacing  # Смещаем вправо
        if self.toy:
            image_path = f"{image_folder}toy.png"
            pdf.image(image_path, x=x_start, y=y_start, w=image_size, h=image_size)
            x_start += image_size + spacing  # Смещаем вправо
        if self.flowers:
            image_path = f"{image_folder}flowers.png"
            pdf.image(image_path, x=x_start, y=y_start, w=image_size, h=image_size)
            x_start += image_size + spacing  # Смещаем вправо
        if self.strawberry:
            image_path = f"{image_folder}strawberry.png"
            pdf.image(image_path, x=x_start, y=y_start, w=image_size, h=image_size)
            x_start += image_size + spacing  # Смещаем вправо

        pdf.set_font("ArialUnicodeMS", '', 16)
        # Заголовки PDF
        pdf.cell(200, 10, f"""Номер заказа   # {order_number}   |   {data.get("admin_name", "")}""", align='C',
                 new_x=XPos.LMARGIN, new_y=YPos.NEXT)

        # Добавляем "Информация об отправителе"
        pdf.ln(10)  # Отступ перед текстом
        pdf.set_font("ArialUnicodeMS", '', 14)
        pdf.cell(0, 10, "Информация об отправителе/Gönderen bilgisi", align='L', new_x=XPos.LMARGIN,
                 new_y=YPos.NEXT)  # Выровняем по левому краю
        pdf.set_font("ArialUnicodeMS", '', 10)

        # Отправитель
        # Если это ссылка с инсты обрезать все кроме ника на инст
        customer = data.get("customer_entry", "")
        if "?" in customer:
            new_customer = ""
            for i in range(customer.find("?")):
                new_customer += customer[i]
            customer = new_customer

        pdf.cell(60, 10, 'Отправитель/Gönderen', border=1, align='L')  # Выровнять по левому краю
        pdf.cell(130, 10, customer, border=1, align='L')  # Временной промежуток
        pdf.ln()

        # Добавляем "Информация о доставке"
        pdf.ln(10)  # Отступ перед текстом
        pdf.set_font("ArialUnicodeMS", '', 14)
        pdf.cell(0, 10, "Информация о доставке/Teslimat Bilgileri", align='L', new_x=XPos.LMARGIN,
                 new_y=YPos.NEXT)  # Выровняем по левому краю
        pdf.set_font("ArialUnicodeMS", '', 10)

        # Левый столбик - данные
        pdf.cell(60, 10, 'Дата/Tarih', border=1, align='L')  # Выровнять по левому краю
        pdf.cell(130, 10, data.get("date_label", ""), border=1, align='L')  # Дата
        pdf.ln()

        pdf.cell(60, 10, 'Временной промежуток/Zaman', border=1, align='L')  # Выровнять по левому краю
        pdf.cell(130, 10, data.get("time_interval_entry", ""), border=1, align='L')  # Временной промежуток
        pdf.ln()

        pdf.cell(60, 10, 'Доставка/Teslimat', border=1, align='L')  # Выровнять по левому краю
        pdf.cell(130, 10, data.get("delivery_pickup_entry", ""), border=1, align='L')  # Доставка/Самовывоз
        pdf.ln()

        pdf.cell(60, 10, 'Район доставки/İlçe', border=1, align='L')  # Выровнять по левому краю
        pdf.cell(130, 10, data.get("district_entry", ""), border=1, align='L')  # Район
        pdf.ln()

        pdf.cell(60, 10, 'Стоимость доставки/Teslimat ücreti', border=1, align='L')  # Выровнять по левому краю
        pdf.cell(130, 10, data.get("delivery_price_entry", ""), border=1, align='L')  # Стоимость доставки
        pdf.ln()

        pdf.cell(60, 10, 'Имя получателя/Alıcının adı', border=1, align='L')  # Выровнять по левому краю
        pdf.cell(130, 10, data.get("recipient_name_entry", ""), border=1, align='L')  # Имя получателя
        pdf.ln()

        pdf.cell(60, 10, 'Номер получателя/Alıcı numarası', border=1, align='L')  # Выровнять по левому краю
        pdf.cell(130, 10, data.get("recipient_number_entry", ""), border=1, align='L')  # Имя получателя
        pdf.ln()

        pdf.cell(60, 10, 'Адрес доставки/Adres', border=1, align='L')  # Выровнять по левому краю
        pdf.multi_cell(130, 10, data.get("address_entry", ""), border=1, align='L', new_x=XPos.LMARGIN,
                 new_y=YPos.NEXT)  # Адрес
        pdf.set_font("ArialUnicodeMS", '', 10)
        pdf.cell(60, 10, 'Комментарий к заказу/Yorum    ', border=1, align='L')  # Выровнять по левому краю
        pdf.multi_cell(130, 10, data.get("note_order", ""), border=1, align='L', new_x=XPos.LMARGIN,
                 new_y=YPos.NEXT)  # Коментарий
        pdf.ln()
        pdf.set_font("ArialUnicodeMS", '', 10)
        # Информация о товаре
        # Отступ перед текстом
        pdf.set_font("ArialUnicodeMS", '', 14)
        pdf.cell(0, 10, "Информация о товаре/Ürün bilgisi", align='L')  # Выровняем по левому краю
        pdf.set_font("ArialUnicodeMS", '', 10)

        # Таблица с товарами
        pdf.ln(10)  # Отступ перед таблицей
        pdf.set_font("ArialUnicodeMS", '', 10)

        #size of strok pryamougolnikov
        size_of_rectangle = 10


        for product_name_entry, product_price_entry, product_description_entry in self.product_entries:
            product_name = product_name_entry.get().strip()
            product_price = product_price_entry.get().strip()
            product_description = product_description_entry.get().strip()

            if 'Записка' in product_name:
                pdf.cell(60, size_of_rectangle, f'{product_name}/Not', border=1, align='L')  # Выровнять по левому краю
                pdf.multi_cell(130, size_of_rectangle, product_description, border=1, align='L', new_x=XPos.LMARGIN,
                               new_y=YPos.NEXT)
            else:
                if 'букет' in product_name.lower():
                    pdf.cell(60, size_of_rectangle, f'{product_name}/Çiçek buketi', border=1, align='L')  # Выровнять по левому краю
                    pdf.cell(40, size_of_rectangle, product_price, border=1, align='L')  # Выровнять по левому краю
                    pdf.multi_cell(90, size_of_rectangle, product_description, border=1, align='L', new_x=XPos.LMARGIN,
                     new_y=YPos.NEXT)  # Выровнять по левому краю
                elif 'шары' in product_name.lower():
                    pdf.cell(60, size_of_rectangle, f'{product_name}/Balonlar', border=1, align='L')  # Выровнять по левому краю
                    pdf.cell(40, size_of_rectangle, product_price, border=1, align='L')  # Выровнять по левому краю
                    pdf.multi_cell(90, size_of_rectangle, product_description, border=1, align='L', new_x=XPos.LMARGIN,
                     new_y=YPos.NEXT)  # Выровнять по левому краю
                elif 'торт' in product_name.lower():
                    pdf.cell(60, size_of_rectangle, f'{product_name}/Pasta', border=1, align='L')  # Выровнять по левому краю
                    pdf.cell(40, size_of_rectangle, product_price, border=1, align='L')  # Выровнять по левому краю
                    pdf.multi_cell(90, size_of_rectangle, product_description, border=1, align='L', new_x=XPos.LMARGIN,
                     new_y=YPos.NEXT)  # Выровнять по левому краю
                elif 'клубника' in product_name.lower():
                    pdf.cell(60, size_of_rectangle, f'{product_name}/Çilek', border=1, align='L')  # Выровнять по левому краю
                    pdf.cell(40, size_of_rectangle, product_price, border=1, align='L')  # Выровнять по левому краю
                    pdf.multi_cell(90, size_of_rectangle, product_description, border=1, align='L', new_x=XPos.LMARGIN,
                     new_y=YPos.NEXT)  # Выровнять по левому краю
                elif 'бокс' in product_name.lower():
                    pdf.cell(60, size_of_rectangle, f'{product_name}/Çiçek kutusu', border=1, align='L')  # Выровнять по левому краю
                    pdf.cell(40, size_of_rectangle, product_price, border=1, align='L')  # Выровнять по левому краю
                    pdf.multi_cell(90, size_of_rectangle, product_description, border=1, align='L', new_x=XPos.LMARGIN,
                     new_y=YPos.NEXT)  # Выровнять по левому краю
                elif 'финики' in product_name.lower():
                    pdf.cell(60, size_of_rectangle, f'{product_name}/Tarihler', border=1, align='L')  # Выровнять по левому краю
                    pdf.cell(40, size_of_rectangle, product_price, border=1, align='L')  # Выровнять по левому краю
                    pdf.multi_cell(90, size_of_rectangle, product_description, border=1, align='L', new_x=XPos.LMARGIN,
                     new_y=YPos.NEXT)  # Выровнять по левому краю
                elif 'игрушка' in product_name.lower():
                    pdf.cell(60, size_of_rectangle, f'{product_name}/Oyuncak', border=1, align='L')  # Выровнять по левому краю
                    pdf.cell(40, size_of_rectangle, product_price, border=1, align='L')  # Выровнять по левому краю
                    pdf.multi_cell(90, size_of_rectangle, product_description, border=1, align='L', new_x=XPos.LMARGIN,
                     new_y=YPos.NEXT)  # Выровнять по левому краю
                elif 'другое' in product_name.lower():
                    pdf.cell(60, size_of_rectangle, f'{product_name}/Diğer', border=1, align='L')  # Выровнять по левому краю
                    pdf.cell(40, size_of_rectangle, product_price, border=1, align='L')  # Выровнять по левому краю
                    pdf.multi_cell(90, size_of_rectangle, product_description, border=1, align='L', new_x=XPos.LMARGIN,
                     new_y=YPos.NEXT)  # Выровнять по левому краю
                else:
                    pdf.cell(60, size_of_rectangle, f'{product_name}', border=1, align='L')  # Выровнять по левому краю
                    pdf.cell(40, size_of_rectangle, product_price, border=1, align='L')  # Выровнять по левому краю
                    pdf.multi_cell(90, size_of_rectangle, product_description, border=1, align='L', new_x=XPos.LMARGIN,
                     new_y=YPos.NEXT)  # Выровнять по левому краю
        file_path = os.path.join(self.save_path, f"{order_number}.pdf")
        try:
            pdf.output(file_path)
            messagebox.showinfo("Успех", f"PDF успешно сохранён: {file_path}")
            self.clear_fields()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить PDF: {e}")

    def clear_fields(self):
        for _, var_name, _ in self.fields:
            getattr(self, var_name).delete(0, 'end')
        for product_name_entry, product_price_entry, product_description_entry in self.product_entries:
            product_name_entry.delete(0, 'end')
            product_price_entry.delete(0, 'end')
            product_description_entry.delete(0, 'end')

if __name__ == "__main__":

    root = Tk()
    app = PDFGeneratorApp(root)
    root.mainloop()
