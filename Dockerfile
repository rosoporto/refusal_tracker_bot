# Используем официальный образ Python
FROM python:3.10-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы проекта
COPY . .

# Устанавливаем uv
RUN pip install uv

# Устанавливаем зависимости через uv
RUN uv pip install --locked

# Создаем директорию для логов
RUN mkdir -p /app/logs

# Команда для запуска бота
CMD ["python", "main.py"]