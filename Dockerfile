FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x ./entrypoint.sh
ENV DATABASE_URL="postgresql://postgres:postgres@pc2.cbomesa6876b.us-east-1.rds.amazonaws.com:5432"
ENV SECRET_KEY="secret_key"
ENV ACCESS_TOKEN_EXPIRE_MINUTES=30

EXPOSE 8000

ENTRYPOINT ["./entrypoint.sh"]
