FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN find /etc/apt -type f \( -name '*.list' -o -name '*.sources' \) -exec sed -i 's|http://deb.debian.org|https://deb.debian.org|g' {} + \
    && apt-get update \
    && apt-get install -y --no-install-recommends build-essential libpq-dev curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*

COPY admin/requirements.txt ./requirements.txt
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY admin /app/admin

ENV PYTHONPATH=/app

EXPOSE 8100

CMD ["uvicorn", "admin.main:app", "--host", "0.0.0.0", "--port", "8100"]
