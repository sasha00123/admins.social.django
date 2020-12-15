FROM gcr.io/google_appengine/python

WORKDIR /usr/src/app

COPY . /usr/src/app

RUN virtualenv /env -p python3.7
ENV VIRTUAL_ENV /env
ENV PATH /env/bin:$PATH

ENV DEBUG=0

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD gunicorn -b :8080 authLayer.wsgi

