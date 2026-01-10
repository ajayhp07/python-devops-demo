FROM python:3.11-slim

WORKDIR /app

COPY app.py .
COPY requirements.txt .
COPY templates ./templates
COPY tests ./tests

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "app.py"]