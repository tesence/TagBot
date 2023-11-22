FROM python:3.11.6-alpine

# Required to install aiosqlite
RUN apk add --no-cache git

WORKDIR /app

COPY tag_bot ./tag_bot
COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ENTRYPOINT ["python", "-m", "tag_bot"]
