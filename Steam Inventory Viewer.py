import tkinter as tk
from tkinter import ttk, messagebox, Button
import requests
import json
import os
from decimal import Decimal, InvalidOperation, Context, setcontext
import webbrowser

# Установка точности для Decimal
context = Context(prec=2)
setcontext(context)

# Функция для получения цен предметов с Steam-рынка
def fetch_item_prices(app_id, cookies):
    url = f'https://steamcommunity.com/market/search/render/?query=&start=0&count=100&search_descriptions=0&sort_column=popular&sort_dir=desc&appid={app_id}&norender=1'
    headers = {
        'Cookie': cookies
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch item prices: {e}")
        return None

# Функция для получения инвентаря
def get_inventory(steam_id, app_id, context_id):
    url = f'https://steamcommunity.com/inventory/{steam_id}/{app_id}/{context_id}'
    params = {
        'l': 'english',  # язык ответа
        'count': 5000    # максимальное количество предметов в запросе
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        inventory = response.json()
        if 'descriptions' in inventory and 'assets' in inventory:
            return inventory
        else:
            print('No items found or inventory is private.')
            return None
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch inventory: {e}")
        return None

# Функция для отображения инвентаря с ценами
def display_inventory(inventory, prices):
    item_dict = {}
    price_dict = {item['hash_name']: item for item in prices['results']}

    # Обработка описаний предметов
    for item in inventory['descriptions']:
        item_name = item['name']
        classid_instanceid = f"{item['classid']}_{item['instanceid']}"
        item_dict[classid_instanceid] = {
            'name': item_name,
            'count': 0,  # Инициализация счетчика
            'price': Decimal('0.000')  # Инициализация стоимости каждого предмета
        }

    # Обработка активов предметов
    for item in inventory['assets']:
        classid_instanceid = f"{item['classid']}_{item['instanceid']}"
        amount = int(item['amount'])  # Преобразование количества в целое число

        if classid_instanceid in item_dict:
            item_dict[classid_instanceid]['count'] += amount
        else:
            item_dict[classid_instanceid] = {
                'name': 'Неизвестный',
                'count': amount,
                'price': Decimal('0.000')
            }

    # Комбинирование данных в список
    total_items_count = 0
    total_items_cost = Decimal('0.000')
    priced_list = []
    for item_data in item_dict.values():
        item_name = item_data['name']
        count = item_data['count']
        price_info = price_dict.get(item_name, {})
        price_text = price_info.get('sale_price_text', 'N/A')

        price_value = Decimal(price_info.get('sell_price', '0')) / Decimal('100')  # Преобразование цены в Decimal
        item_data['price'] = price_value

        total_item_cost = count * price_value
        priced_list.append((item_name, count, price_text, total_item_cost))
        total_items_count += count
        total_items_cost += total_item_cost

    try:
        total_items_cost = total_items_cost.quantize(Decimal('0.00'))  # Округление до двух знаков после запятой
        total_items_cost_str = f"{total_items_cost.normalize():.2f}"  # Конвертация в строку с двумя знаками после запятой
    except InvalidOperation as e:
        print(f"Error quantizing total_items_cost: {e}")
        total_items_cost_str = "0.00"

    steam_inventory_price = sum(item_data['price'] * item_data['count'] for item_data in item_dict.values())

    return priced_list, total_items_count, total_items_cost_str, steam_inventory_price

# Класс приложения Tkinter
class InventoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Steam Inventory Viewer")
        self.root.geometry("820x500")  # Установка начальных размеров окна

        # Создание элементов интерфейса
        self.steam_id_label = ttk.Label(root, text="Steam ID:")
        self.steam_id_label.grid(row=0, column=0, padx=5, pady=5, sticky='e')

        self.steam_id_entry = ttk.Entry(root, font=('Arial', 12))
        self.steam_id_entry.grid(row=0, column=1, padx=5, pady=5, sticky='ew')

        self.text_label = ttk.Label(root, text="Thank you for using Steam Inventory Viewer", font=('Arial', 12))
        self.text_label.grid(row=0, column=2, padx=5, pady=5, sticky='e')

        self.text_label = tk.Label(root, text="Software by SkyLandYT2", font=('Arial', 12), fg="blue", cursor="hand2")
        self.text_label.grid(row=1, column=2, padx=5, pady=5, sticky='e')
        self.text_label.bind("<Button-1>", lambda e: self.open_link("https://github.com/SkyLandYT2"))

        self.app_id_label = ttk.Label(root, text="App ID:")
        self.app_id_label.grid(row=1, column=0, padx=5, pady=5, sticky='e')

        self.app_id_entry = ttk.Entry(root, font=('Arial', 12))
        self.app_id_entry.grid(row=1, column=1, padx=5, pady=5, sticky='ew')

        self.context_id_label = ttk.Label(root, text="Context ID:")
        self.context_id_label.grid(row=2, column=0, padx=5, pady=5, sticky='e')

        self.context_id_entry = ttk.Entry(root, font=('Arial', 12))
        self.context_id_entry.grid(row=2, column=1, padx=5, pady=5, sticky='ew')

        self.cookies_label = ttk.Label(root, text="Cookies:")
        self.cookies_label.grid(row=3, column=0, padx=5, pady=5, sticky='e')

        self.cookies_entry = ttk.Entry(root, font=('Arial', 12))
        self.cookies_entry.grid(row=3, column=1, padx=5, pady=5, sticky='ew')

        self.start_button = ttk.Button(root, text="Start", command=self.start_updating, width=10, style='TButton')
        self.start_button.grid(row=4, column=0, padx=5, pady=5, sticky='ew')

        self.stop_button = ttk.Button(root, text="Stop", command=self.stop_updating, width=10, style='TButton')
        self.stop_button.grid(row=4, column=1, padx=5, pady=5, sticky='ew')

        self.import_config_button = ttk.Button(root, text="Import Config", command=self.import_config, style='TButton')
        self.import_config_button.grid(row=4, column=2, padx=5, pady=5, sticky='ew')

        self.save_config_button = ttk.Button(root, text="Save Config", command=self.save_config, width=10, style='TButton')
        self.save_config_button.grid(row=4, column=3, padx=5, pady=5, sticky='ew')

        # Создание Treeview с заголовками колонок
        self.tree = ttk.Treeview(root, columns=('Name', 'Count', 'Price Each', 'Total Cost'), show='headings', height=10)
        self.tree.heading('Name', text='Name', command=lambda: self.sort_treeview('Name', False))
        self.tree.heading('Count', text='Count', command=lambda: self.sort_treeview('Count', False))
        self.tree.heading('Price Each', text='Price Each', command=lambda: self.sort_treeview('Price Each', False))
        self.tree.heading('Total Cost', text='Total Cost', command=lambda: self.sort_treeview('Total Cost', False))
        self.tree.grid(row=5, column=0, columnspan=4, padx=5, pady=5, sticky="nsew")

        root.grid_rowconfigure(5, weight=1)
        root.grid_columnconfigure(0, weight=1)
        root.grid_columnconfigure(1, weight=1)
        root.grid_columnconfigure(2, weight=1)
        root.grid_columnconfigure(3, weight=1)

        self.total_label = ttk.Label(root, text="")
        self.total_label.grid(row=6, column=0, columnspan=4)

        self.running = False
        self.update_interval = 60

    def start_updating(self):
        self.steam_id = self.steam_id_entry.get()
        self.app_id = self.app_id_entry.get()
        self.context_id = self.context_id_entry.get()
        self.cookies = self.cookies_entry.get()

        if not self.steam_id or not self.app_id or not self.context_id or not self.cookies:
            print("Please fill in all fields.")
            return

        self.running = True
        self.update_inventory()

    def stop_updating(self):
        self.running = False
        self.tree.delete(*self.tree.get_children())
        self.total_label.config(text="")

    def update_inventory(self):
        if self.running:
            inventory = get_inventory(self.steam_id, self.app_id, self.context_id)
            prices = fetch_item_prices(self.app_id, self.cookies)
            if inventory and prices:
                combined_inventory, total_items_count, total_items_cost, steam_inventory_price = display_inventory(inventory, prices)
                self.tree.delete(*self.tree.get_children())
                for item in combined_inventory:
                    item_name = item[0]
                    price_text = item[2]
                    price_color = 'red' if price_text == 'Price Each' else 'black'
                    self.tree.insert('', 'end', values=item, tags=(price_color,))
                self.total_label.config(text=f"Total items: {total_items_count} | Steam Inventory Price: {steam_inventory_price:.2f}")
            else:
                self.tree.delete(*self.tree.get_children())
                self.tree.insert('', 'end', values=("Failed to retrieve inventory or inventory is private or try later.",))

            # Schedule next update
            self.root.after(self.update_interval * 1000, self.update_inventory)

    def save_config(self):
        config = {
            'steam_id': self.steam_id_entry.get(),
            'app_id': self.app_id_entry.get(),
            'context_id': self.context_id_entry.get(),
            'cookies': self.cookies_entry.get()
        }
        file_path = 'config.json'
        with open(file_path, 'w') as config_file:
            json.dump(config, config_file)
        messagebox.showinfo("Info", "Config saved successfully")

    def import_config(self):
        file_path = 'config.json'
        if os.path.exists(file_path):
            with open(file_path, 'r') as config_file:
                config = json.load(config_file)
                self.steam_id_entry.delete(0, tk.END)
                self.steam_id_entry.insert(0, config['steam_id'])
                self.app_id_entry.delete(0, tk.END)
                self.app_id_entry.insert(0, config['app_id'])
                self.context_id_entry.delete(0, tk.END)
                self.context_id_entry.insert(0, config['context_id'])
                self.cookies_entry.delete(0, tk.END)
                self.cookies_entry.insert(0, config['cookies'])
        else:
            messagebox.showerror("Error", "Config file not found")

    def open_link(self, url):
        webbrowser.open_new(url)

    def sort_treeview(self, col, reverse):
        # Определяем функцию для преобразования значений в нужный тип
        def convert(value):
            try:
                return int(value)
            except ValueError:
                try:
                    return float(value)
                except ValueError:
                    return value

        # Преобразуем значения в нужный тип перед сортировкой
        l = [(convert(self.tree.set(k, col)), k) for k in self.tree.get_children('')]
        l.sort(reverse=reverse)

        for index, (val, k) in enumerate(l):
            self.tree.move(k, '', index)

        self.tree.heading(col, command=lambda: self.sort_treeview(col, not reverse))

if __name__ == "__main__":
    root = tk.Tk()
    app = InventoryApp(root)
    root.mainloop()
