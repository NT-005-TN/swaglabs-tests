FROM python:3.10-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    wget gnupg ca-certificates unzip \
    libglib2.0-0 libnss3 libfontconfig1 fonts-liberation \
    libasound2 libatk-bridge2.0-0 libgtk-3-0 libx11-xcb1 \
    libxcomposite1 libxcursor1 libxdamage1 libxi6 libxtst6 \
    xdg-utils libgbm1 libu2f-udev && \
    rm -rf /var/lib/apt/lists/*

RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /usr/share/keyrings/google-chrome-keyring.gpg && \
    echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google-chrome-keyring.gpg] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && \
    apt-get install -y google-chrome-stable && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src/ ./src/
CMD ["sh", "-c", "pytest src/tests/test_login.py -v --alluredir=/tmp/allure-results && cp -r /tmp/allure-results /app/"]