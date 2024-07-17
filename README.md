# Steam Inventory Viewer Instructions

## English

```bash
git clone https://github.com/SkyLandYT2/Steam-Inventory-Viever.git
```

### Why Cookies?

Cookies are needed to fetch item prices from the Steam Community Market.

### Usage

1. **Enter the necessary data:**
   - **Steam ID:** Your Steam ID to access the inventory.
   - **App ID:** The Steam application ID for which you want to view the inventory.
   - **Context ID:** The Steam inventory context ID.
   - **Cookies:** Cookies for authentication and fetching item prices. To get cookies, do the following:
     - Go to the [this page](https://steamcommunity.com/market/search/render/?query=&start=0&count=100&search_descriptions=0&sort_column=popular&sort_dir=desc&appid=753&norender=1).
     - Press `Ctrl + Shift + I` to open the developer tools in your browser and go to the "Network" tab.
     - Ensure recording actions is enabled, then refresh the page.
     - Find the request `render/?query=&start...` (usually at the top of the list) and open it.
     - Find the "Cookie" section and copy the contents.
   
2. **Click the "Start" button** to begin updating inventory data.

3. **Import and export configuration data:**
   - You can import and export configuration data for quick access to settings.

### Dependencies

- Python 3.x
- Libraries: tkinter, requests, json

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/SkyLandYT2/Steam-Inventory-Viever.git
   ```

2. Install the necessary dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## На Русском

```bash
git clone https://github.com/SkyLandYT2/Steam-Inventory-Viever.git
```

### Зачем нужны Cookies?

Cookies необходимы для получения цен предметов с Steam Community Market.

### Использование

1. **Укажите необходимые данные:**
   - **Steam ID:** Ваш Steam ID для доступа к инвентарю.
   - **App ID:** ID приложения Steam, для которого вы хотите просмотреть инвентарь.
   - **Context ID:** ID контекста инвентаря Steam.
   - **Cookies:** Куки для аутентификации и получения цен предметов. Чтобы получить Cookies, выполните следующие действия:
     - Зайдите на [страницу](https://steamcommunity.com/market/search/render/?query=&start=0&count=100&search_descriptions=0&sort_column=popular&sort_dir=desc&appid=753&norender=1).
     - Нажмите `Ctrl + Shift + I` для открытия инструментов разработчика в браузере и перейдите на вкладку "Network" (Сеть).
     - Убедитесь, что запись действий включена, затем перезагрузите страницу.
     - Найдите запрос `render/?query=&start...` (обычно находится вверху списка) и откройте его.
     - Найдите раздел "Cookie" и скопируйте содержимое.
   
2. **Нажмите кнопку "Start"** для начала обновления данных инвентаря.

3. **Импорт и экспорт конфигурационных данных:**
   - Вы можете импортировать и экспортировать конфигурационные данные для быстрого доступа к настройкам.

### Зависимости

- Python 3.x
- Библиотеки: tkinter, requests, json

### Установка

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/SkyLandYT2/Steam-Inventory-Viever.git
   ```

2. Установите необходимые зависимости:
   ```bash
   pip install -r requirements.txt
   ```
