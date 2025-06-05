# Инструкция для развертывания приложения на Debian 12 Bookworm

---

## Требования

* **Docker**
* **Ollama** с загруженной LLM (например, `llama2`)

---

## Команда для сборки образа и запуска контейнера

Выполните эту команду в директории проекта:

```bash
docker build -t flask-ollama-app . && docker run -p 5000:5000 -e OLLAMA_HOST=host.docker.internal flask-ollama-app
```

После выполнения команды откройте приложение в браузере:  
[http://localhost:5000](http://localhost:5000)

---

## Если Ollama недоступен

Если приложение не может связаться с Ollama (ошибка `"Ollama сервер недоступен"`), выполните следующие шаги:

### 1. Настройте Ollama слушать на `0.0.0.0`

Отредактируйте файл службы Ollama (например, `/etc/systemd/system/ollama.service`), добавив:

```ini
Environment="OLLAMA_HOST=0.0.0.0"
```

в секцию `[Service]`.

Затем перезагрузите Ollama:

```bash
sudo systemctl daemon-reload
sudo systemctl restart ollama
```

Проверьте статус Ollama:

```bash
sudo ss -tulnp | grep 11434
```

Должно быть `*:11434` или `0.0.0.0:11434`.

---

### 2. Запустите контейнер с явным IP-адресом хоста

Получите IP-адрес шлюза Docker:

```bash
DOCKER_GATEWAY_IP=$(ip addr show docker0 | grep "inet\b" | awk '{print $2}' | cut -d '/' -f 1)
```

Запустите контейнер, используя полученный IP:

```bash
docker run -p 5000:5000 -e OLLAMA_HOST=host.docker.internal --add-host host.docker.internal:$DOCKER_GATEWAY_IP flask-ollama-app
```

После выполнения команды откройте приложение в браузере:  
[http://localhost:5000](http://localhost:5000)
