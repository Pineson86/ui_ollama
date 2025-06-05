# Используем официальный образ Python как базовый образ
FROM python:3.9-slim-buster

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файл зависимостей
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальную часть приложения
COPY . .

# Открываем порт 5000
EXPOSE 5000

# Команда для запуска Flask-приложения с помощью встроенного сервера
CMD ["python", "main.py"]
