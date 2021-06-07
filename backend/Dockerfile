FROM rasa/rasa:2.4.0

WORKDIR /app
COPY . /app/
COPY ./data /app/data
#COPY ./ssl /app/ssl

VOLUME /app
VOLUME /app/data
VOLUME /app/models
VOLUME /app/ssl

CMD ["run", "-m", "/app/models", "--endpoints", "endpoints.yml", "--enable-api", "--credentials", "credentials.yml", "--cors", "*", "--debug"]
