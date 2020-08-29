# Running with docker
FROM python:3
WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

RUN flask db init
RUN flask db migrate
RUN flask db upgrade
CMD ["flask", "run"]