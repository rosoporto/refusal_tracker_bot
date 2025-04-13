#!/bin/bash

# Создаём директории на хосте
mkdir -p ./data ./logs

# Устанавливаем права на хосте
sudo chown -R 1000:1000 ./data ./logs
sudo chmod -R 775 ./data ./logs

# Запускаем контейнер
docker-compose up -d --build