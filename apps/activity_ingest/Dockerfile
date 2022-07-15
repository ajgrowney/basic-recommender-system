FROM python:3.9
ARG APP_DIR=apps/activity_ingest

# Utilities 
COPY utilities /src/utilities
WORKDIR /src/utilities
RUN python setup.py install

# Application

COPY ${APP_DIR}/requirements.txt /src/requirements.txt
RUN pip install -r /src/requirements.txt


COPY ${APP_DIR}/ingest_manager.py /app/main.py

WORKDIR /app
ENTRYPOINT ["python", "main.py"]
