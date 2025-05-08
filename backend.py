from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Запрос к локальному ИИ-агенту и получение ответа от него
def query_ollama(prompt: str) -> str:
    url = 'http://localhost:11434/api/generate'
    headers = {'Content-Type': 'application/json'}
    data = {
        "model": "llama2",
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(url, json=data, headers=headers, timeout=120)
        response.raise_for_status()
        return response.json().get("response", "Нет ответа")
    except requests.exceptions.Timeout:
        return "Я пока отдыхаю. Попробуй разбудить меня чуть попозже!"
    except requests.exceptions.ConnectionError:
        return "Ошибка: Ollama сервер недоступен. Проверьте подключение."
    except requests.exceptions.RequestException as e:
        return f"Ошибка: не удалось связаться с Ollama. Попробуйте позже."
# Обработка запроса от клиента, перенаправление его ИИ-агенту и возвращение ответа
@app.route('/query', methods=['POST'])
def handle_query():
    data = request.get_json()
    prompt = data.get("prompt", "").strip()
    if not prompt:
        return jsonify({"error": "Пустой запрос"}), 400
    answer = query_ollama(prompt)
    return jsonify({"response": answer})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
