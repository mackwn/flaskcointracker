FROM python:3

WORKDIR /usr/src/app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

ENV FLASK_APP=flaskcointracker

ENV REDIS_URL='redis://redis:6379/0'

ENV DATABASE_URL='postgresql://cointrackerdb:cointrackerdb@db:5432/cointrackerdb_prod'

ENV POSTGRES_USER=cointrackerdb
ENV POSTGRES_PASSWORD=cointrackerdb
ENV POSTGRES_DB=cointrackerdb_prod

CMD ["gunicorn", "flaskcointracker:app", "-b", "0.0.0.0:5000"]