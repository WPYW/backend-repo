FROM python:3.10

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN set -e; \
    apt-get update ;\
    apt-get -y install netcat ;\
    apt-get -y install gettext ;

RUN mkdir /code
COPY . /code/
WORKDIR /code

RUN set -e; \
    /usr/local/bin/python -m pip install --upgrade pip ;\
    python -m pip install -r /code/backend/requirements.txt ;
    # chmod +x entrypoint.sh ;

EXPOSE 8000

CMD ["python", "backend/manage.py", "runserver", "0.0.0.0:8000"]
# CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "wpyw.wsgi:application"]
