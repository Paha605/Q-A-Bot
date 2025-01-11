# Используем официальный образ Python в качестве базового
FROM python:3.9

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем все файлы проекта в контейнер
COPY requirements.txt /app/requirements.txt

# Устанавливаем зависимости проекта
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY . /app
# Указываем команду для запуска бота
CMD ["python", "main.py"]