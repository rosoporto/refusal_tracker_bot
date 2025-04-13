FROM python:3.10-slim

# Создаём пользователя
RUN useradd -m -u 1000 appuser

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы проекта
COPY . .

# Устанавливаем зависимости
RUN pip install uv
RUN uv sync

# Создаём директории для базы и логов, устанавливаем права
RUN mkdir -p /app/data /app/logs && \
    chown -R appuser:appuser /app /app/data /app/logs && \
    chmod -R 775 /app/data /app/logs

# Переключаемся на пользователя appuser
USER appuser

# Команда запуска
CMD [".venv/bin/python", "main.py"]