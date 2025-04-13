#!/bin/bash

# Останавливаем docker-compose и удаляем тома
docker-compose down -v

# Удаляем директорию базы данных
rm -rf ./data

# Удаляем директорию логов
rm -rf ./logs

echo "Cleaned up: database and logs removed."
