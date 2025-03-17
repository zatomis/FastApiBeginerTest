FROM python:3.11.9
WORKDIR /app
COPY requirments.txt requirments.txt
RUN pip install -r requirments.txt

COPY . .

CMD alembic upgrade head; python src/main.py