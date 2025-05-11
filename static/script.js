// static/script.js
document.addEventListener('DOMContentLoaded', () => {
    // Получаем ссылки на элементы DOM
    const queryInput = document.getElementById('queryInput'); // Поле ввода запроса
    const sendButton = document.getElementById('sendButton'); // Кнопка отправки
    const chatContainer = document.getElementById('chatContainer'); // Контейнер для сообщений чата
    const userDataDiv = document.getElementById('userData'); // Элемент, содержащий имя пользователя

    // Получаем имя пользователя из data-атрибута
    const username = userDataDiv.dataset.username;

    // Функция для добавления сообщения в чат
    // Принимает отправителя (строка) и текст сообщения (строка).
    function addMessage(sender, text) {
        const messageDiv = document.createElement('div'); // Создаем div для каждого сообщения

        // Создаем заголовок H2 для отображения отправителя сообщения
        const senderHeading = document.createElement('h2');
        senderHeading.textContent = sender + ':'; // Добавляем двоеточие после имени/префикса

        // Создаем параграф P для отображения текста сообщения
        const messageText = document.createElement('p');
        messageText.textContent = text; // Устанавливаем текст

        // Добавляем заголовок отправителя (H2) и текст сообщения (P) в div сообщения
        messageDiv.appendChild(senderHeading);
        messageDiv.appendChild(messageText);

        // Добавляем созданный div сообщения в контейнер чата на странице
        chatContainer.appendChild(messageDiv);

        // Прокручиваем контейнер чата вниз
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }

    // Асинхронная функция для отправки запроса к бэкенду
    async function sendQuery() {
        const query = queryInput.value.trim(); // Получаем текст, удаляя пробелы

        // Если запрос пустой, ничего не отправляем (клиентская проверка)
        if (!query) {
            return;
        }

        // Отображаем запрос пользователя в чате немедленно
        addMessage(username + ' спросил', query);

        // Очищаем поле ввода после отправки
        queryInput.value = '';

        // Отправляем запрос на бэкенд API Flask
        try {
            const response = await fetch('/query', { // URL  API маршрута
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ prompt: query }) // Отправляем JSON с ключом "prompt"
            });

            // Парсим JSON ответ (ожидаем {"response": "..."})
            const data = await response.json();
            // Извлекаем текст ответа из поля "response"
            const botResponse = data.response;

            // Отображаем ответ LLM в чате
            addMessage('LLAMA2 ответила', botResponse);

        } catch (error) {
            // Обработка любой ошибки, возникшей при fetch или парсинге JSON
            console.error('Ошибка при отправке запроса:', error); // Логируем ошибку
            // Отображаем общее сообщение об ошибке в чате
            addMessage('Система', 'Произошла ошибка при отправке запроса.');
        }
    }

    // Добавляем обработчик клика на кнопку "Отправить"
    sendButton.addEventListener('click', sendQuery);

    // Добавляем обработчик нажатия Enter в поле ввода
    queryInput.addEventListener('keypress', (event) => {
        // Если нажата клавиша Enter
        if (event.key === 'Enter') {
            event.preventDefault(); // Отменяем стандартное действие
            sendQuery(); // Отправляем запрос
        }
    });
});