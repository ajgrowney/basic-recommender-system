FROM python:3.9
COPY requirements.txt /src/requirements.txt
RUN pip install -r /src/requirements.txt
COPY rec_gen_manager.py /app/main.py

WORKDIR /app

CMD ["python", "main.py"]
