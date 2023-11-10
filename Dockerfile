FROM python:3.11

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN pip install prisma

# RUN prisma migrate dev

# RUN prisma generate

CMD ["sh", "-c", "tail -f /dev/null"]

# CMD [ "uvicorn", "app.main:app", "--host", "0.0.0.0", "--reload", "--port", "8000" ]