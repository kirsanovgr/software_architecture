FROM python:3.9-slim

WORKDIR /app

# Копируем зависимости и устанавливаем их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код
COPY . .

# Указываем команду для запуска
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]