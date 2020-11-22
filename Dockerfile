FROM python:3

WORKDIR /usr/src/app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000



CMD ["gunicorn", "flaskcointracker:app", "-b", "0.0.0.0:5000"]