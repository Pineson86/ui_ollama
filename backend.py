# backend.py
from flask import Flask, request, jsonify, render_template, redirect, url_for
import requests
import os

# Инициализация Flask приложения
app = Flask(__name__)

# Функция для отправки запроса к локальному Ollama серверу
# Принимает строку запроса (prompt) и возвращает строку ответа или сообщение об ошибке Ollama
def query_ollama(prompt: str) -> str:
    url = 'http://localhost:11434/api/generate'
    headers = {'Content-Type': 'application/json'}
    data = {
        "model": "llama2", # Указываем используемую модель LLM
        "prompt": prompt,  # Передаем запрос
        "stream": False    # Отключаем потоковую передачу
    }

    try:
        # Отправляем POST запрос к API Ollama с таймаутом 120 секунд
        response = requests.post(url, json=data, headers=headers, timeout=120)
        response.raise_for_status() # Вызывает исключение для плохих статусов ответов (4xx или 5xx)
        # Парсим JSON ответ и извлекаем поле "response"
        return response.json().get("response", "Нет ответа")
    except requests.exceptions.Timeout:
        # Обработка таймаута запроса к Ollama
        return "Я пока отдыхаю. Попробуй разбудить меня чуть попозже!"
    except requests.exceptions.ConnectionError:
        # Обработка ошибки подключения к серверу Ollama
        return "Ошибка: Ollama сервер недоступен. Проверьте подключение."
    except requests.exceptions.RequestException as e:
        # Обработка других ошибок запросов к Ollama
        print(f"Ошибка при запросе к Ollama: {e}") # Логирование ошибки
        return f"Ошибка: не удалось связаться с Ollama. Попробуйте позже."

# Маршрут для обработки запросов от клиента к LLM API
# Ожидается POST запрос с JSON телом {"prompt": "..."}
@app.route('/query', methods=['POST'])
def handle_query():
    data = request.get_json()
    prompt = data.get("prompt", "").strip() # Получаем поле "prompt", пустая строка по умолчанию, удаляем пробелы

    # Пустой prompt будет передан в query_ollama

    print(f"Received query from frontend: {prompt}") # Логируем запрос
    answer = query_ollama(prompt) # Получаем ответ от Ollama (или сообщение об ошибке Ollama)
    print(f"Sending response to frontend: {answer[:100]}...") # Логируем ответ

    # Возвращаем ответ в формате JSON с полем "response"
    return jsonify({"response": answer})


# Маршрут для главной страницы - перенаправляет на страницу логина
@app.route('/')
def index():
    return redirect(url_for('login'))

# Маршрут для страницы логина
# GET метод показывает форму логина
# POST метод обрабатывает отправку формы и перенаправляет
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('login') # Получаем логин из данных формы
        if username:
            # Если логин введен, перенаправляем на маршрут чата
            return redirect(url_for('chat', username=username))
        else:
            # Если логин пустой, снова показываем форму логина
            # Этот return был удален
            return render_template('index.html') # Убрали передачу error, т.к. шаблон его не отображает

    # Если метод GET или другой (не POST), показываем форму логина
    # Этот return был удален
    return render_template('index.html')


# Маршрут для страницы чата с динамическим именем пользователя в URL
@app.route('/<username>')
def chat(username):
    # Отображаем шаблон страницы чата, передавая имя пользователя
    return render_template('chat.html', username=username)


if __name__ == '__main__':
    # Запуск Flask приложения
    app.run(host='0.0.0.0', port=5000, debug=True)