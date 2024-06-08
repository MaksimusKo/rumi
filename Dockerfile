# Используйте образ, совместимый с CUDA
FROM nvidia/cuda:12.5.0-devel-ubuntu22.04

# Установите Python и необходимые библиотеки
RUN apt-get update && apt-get install -y python3 python3-pip

# Установите зависимости приложения
COPY requirements.txt /app/
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt

# Скопируйте файлы приложения
COPY .. /app

# Установите порт
EXPOSE 8000

# Запустите приложение
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
