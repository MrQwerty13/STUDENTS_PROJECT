# Используем официальный Python-образ
FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем зависимости (если есть requirements.txt)
# Если его нет — можно создать автоматически: pip freeze > requirements.txt
COPY requirements.txt ./

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt || true

# Копируем остальной проект
COPY . .

# Указываем порт (Streamlit использует 8501 по умолчанию)
EXPOSE 8501

# Отключаем использование браузера и включаем внешние подключения
ENV STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_ENABLECORS=false \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Команда запуска
CMD ["streamlit", "run", "streamlit.py"]
