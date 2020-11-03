web: gunicorn flaskcointracker:app
worker: celery worker -A flaskcointracker.celery
worker: celery beat -A flaskcointracker.celery