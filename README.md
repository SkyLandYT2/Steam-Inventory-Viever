Прекрасно! Вот как вы можете продолжить описание и инструкции:

```markdown
git clone https://github.com/SkyLandYT2/Steam-Inventory-Viever.git
```

### Зачем нужен Cookies?

Cookies необходимы для получения цен предметов с Steam Community Market.

### Использование

1. **Укажите необходимые данные:**
   - **Steam ID**: Ваш Steam ID для доступа к инвентарю.
   - **App ID**: ID приложения Steam, для которого вы хотите просмотреть инвентарь.
   - **Context ID**: ID контекста инвентаря Steam.
   - **Cookies**: Куки для аутентификации и получения цен предметов. Чтобы получить Cookies, выполните следующие действия:
     - Зайдите на [страницу Steam Community Market](https://steamcommunity.com/market/search/render/?query=&start=0&count=100&search_descriptions=0&sort_column=popular&sort_dir=desc&appid=753&norender=1).
     - Нажмите `Ctrl + Shift + I` для открытия инструментов разработчика в браузере и перейдите на вкладку "Network"(Сеть).
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
3. ```
   pip install -r requirements.txt
   ```


