FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    ca-certificates \
    fonts-liberation \
    libnss3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxrandr2 \
    libxdamage1 \
    libgbm1 \
    libasound2 \
    libpangocairo-1.0-0 \
    libgtk-3-0 \
    libxshmfence1 \
    libx11-xcb1 \
    libxfixes3 \
    libxcb1 \
    libdrm2 \
    libglib2.0-0 \
    libexpat1 \
    libdbus-1-3 \
    libxcb-dri3-0 \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN playwright install chromium

COPY . .

EXPOSE 5000

CMD ["gunicorn", "--workers=1", "--timeout=120", "-b", "0.0.0.0:5000", "app:app"]
