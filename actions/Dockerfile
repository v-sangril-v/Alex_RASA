FROM rasa/rasa-sdk:2.4.0

USER root

COPY ./entrypoint.sh /app/
COPY requirements-actions.txt /tmp
WORKDIR /tmp
RUN pip install -r requirements-actions.txt

USER 1001
WORKDIR /app
EXPOSE 5056
ENTRYPOINT ["./entrypoint.sh"]
CMD ["start", "--actions", "actions"]
