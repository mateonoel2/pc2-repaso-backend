FROM python:3.12-slim

RUN apt-get update && apt-get install -y netcat-traditional


WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x entrypoint.sh

RUN pip freeze
RUN ls -la

EXPOSE 8000

ENTRYPOINT ["./entrypoint.sh"]
