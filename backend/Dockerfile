FROM python:3.11-slim

# Системные зависимости
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        cmake \
        git \
        libpq-dev \
        libssl-dev \
        libffi-dev \
        python3-dev \
        g++ \
        && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Устанавливаем torch с CPU-поддержкой (для sentence-transformers)
RUN pip install --no-cache-dir torch==2.3.0 torchvision==0.18.0 --index-url https://download.pytorch.org/whl/cpu

# Копируем и устанавливаем остальные зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Создаём пользователя
RUN adduser --disabled-password --gecos '' appuser
USER appuser

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--log-level", "info"]
