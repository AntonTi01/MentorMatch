FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN find /etc/apt -type f \( -name '*.list' -o -name '*.sources' \) -exec sed -i 's|http://deb.debian.org|https://deb.debian.org|g' {} + \
    && apt-get update \
    && apt-get install -y --no-install-recommends build-essential libpq-dev git curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*

COPY matching/requirements.txt ./requirements.txt

RUN pip install --upgrade pip \
    && pip install --no-cache-dir --index-url https://download.pytorch.org/whl/cpu torch==2.3.1 \
    && pip install --no-cache-dir -r requirements.txt

COPY matching /app/matching

ENV PYTHONPATH=/app

EXPOSE 8300

CMD ["uvicorn", "matching.main:app", "--host", "0.0.0.0", "--port", "8300"]
