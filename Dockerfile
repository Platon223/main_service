FROM python:3.10-slim-buster

WORKDIR /app/mainService

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "manage.py", "runserver"]