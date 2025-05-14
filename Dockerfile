FROM python:3.12.6-slim

WORKDIR /app

RUN apt update && apt upgrade -y
RUN pip install --upgrade pip

COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . ./


ENV STREAMLIT_SERVER_ENABLE_SSL=true
ENV STREAMLIT_SERVER_CERTIFICATE=/app/fullchain.pem
ENV STREAMLIT_SERVER_KEY=/app/privkey.pem

ENTRYPOINT [ "streamlit", "run", "app.py", "--server.port=443", "--server.headless", "true"]


