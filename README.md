# Linkedin_scraper (minimal)

Минимальный проект для парсинга страниц компаний LinkedIn **(используйте только там, где это законно и в рамках условий сервиса)**.
Этот репозиторий создан из вашего файла `linkedin_scraper.py` без изменений.

> ⚠️ **Юридически важно**: соблюдайте законы и условия использования платформ. Работайте только с данными, на анализ которых у вас есть право (экспорты, локальные копии, разрешения).

## 📦 Установка
```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## ▶️ Запуск
1. Создайте файл `url_list.txt` в корне проекта со **списком ссылок через запятую**. Пример:
   ```text
   https://www.linkedin.com/company/example/,
   https://www.linkedin.com/company/example-2/
   ```

2. (Опционально) В файле `linkedin_scraper.py` задайте переменные доступа к прокси (если используете прокси-провайдера) в блоке `if __name__ == "__main__":`:
   ```python
   USERNAME = ''  # username
   PASSWORD = ''  # password
   PORT = '10001' # порт
   ```
   > Если оставить логин-пароль пустыми, то ротации прокси не будет

3. Запустите скрипт:
   ```bash
   python linkedin_scraper.py
   ```

- Вход: `url_list.txt` (список URL через запятую)
- Выход: `output_decodo.json` (JSON-массив объектов c полями `url`, `overview`, и ключами из блока информации компании)

## 🗂 Структура
```
Linkedin_scraper/
├─ linkedin_scraper.py   # ваш исходный скрипт (без изменений)
├─ README.md
├─ requirements.txt
├─ .gitignore
├─ url_list.txt          # (создайте и заполните сами)
└─ examples/
   └─ sample_urls.txt    # пример формата (не используется скриптом)
```

## 🧩 Зависимости
См. `requirements.txt`. Скрипт использует `requests` и `beautifulsoup4` (парсер `lxml`).

## 📝 Примечания
- Верстка страниц и доступность данных могут меняться.
- Уважайте ограничения платформ и частоту запросов.
