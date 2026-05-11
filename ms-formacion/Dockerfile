FROM python:3.13-slim

RUN apt-get update && apt-get install -y curl \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8003

# run.py arranca con app.run(host='0.0.0.0', port=FLASK_PORT)
CMD ["python", "run.py"]
