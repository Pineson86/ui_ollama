document.addEventListener('DOMContentLoaded', () => {
    const chatContainer = document.getElementById('chatContainer');
    const queryInput = document.getElementById('queryInput');
    const sendButton = document.getElementById('sendButton');
    const username = document.getElementById('userData').dataset.username;

    // Function to add a message to the chat
    function addMessage(text, isUser) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;

        // Create heading
        const heading = document.createElement('h2');
        heading.textContent = isUser ? `${username} спросил:` : 'LLAMA2 ответила:';
        messageDiv.appendChild(heading);

        // Create text container for the message
        const textDiv = document.createElement('div');
        textDiv.textContent = text;
        messageDiv.appendChild(textDiv);

        if (!isUser) {
            const copyButton = document.createElement('button');
            copyButton.className = 'copy-button';
            copyButton.textContent = 'Копировать';
            copyButton.addEventListener('click', () => {
                navigator.clipboard.writeText(text).then(() => {
                    copyButton.textContent = 'Скопировано!';
                    setTimeout(() => {
                        copyButton.textContent = 'Копировать';
                    }, 2000);
                }).catch(err => {
                    console.error('Ошибка копирования:', err);
                    copyButton.textContent = 'Ошибка';
                });
            });
            messageDiv.appendChild(copyButton);
        }

        chatContainer.appendChild(messageDiv);
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }

    // Function to send query to backend
    async function sendQuery() {
        const prompt = queryInput.value.trim();
        if (!prompt) return;

        addMessage(prompt, true);
        queryInput.value = '';

        try {
            const response = await fetch('/query', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ prompt }),
            });

            if (!response.ok) {
                throw new Error('Ошибка сервера');
            }

            const data = await response.json();
            addMessage(data.response, false);
        } catch (error) {
            console.error('Ошибка:', error);
            addMessage('Ошибка при получении ответа от сервера.', false);
        }
    }

    // Event listeners
    sendButton.addEventListener('click', sendQuery);
    queryInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendQuery();
        }
    });
});