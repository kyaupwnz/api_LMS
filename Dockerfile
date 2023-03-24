FROM python:3.10.6

WORKDIR /code

COPY . .

RUN pip install -r /code/requirements.txt

CMD python manage.py migrate
CMD python manage.py runserver 0.0.0.0:8000