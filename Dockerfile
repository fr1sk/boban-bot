FROM heroku/cedar:14
RUN apt-get update -y && \
    apt-get install -y python-pip python-dev libssl-dev libffi-dev

COPY ./requirements.txt /home/app/requirements.txt

WORKDIR /home/app/
RUN pip install -r requirements.txt
RUN pip install -U pyopenssl==0.13.1 pyasn1 ndg-httpsclient
COPY . /home/app/
WORKDIR /home/app/server/
EXPOSE 8081
ENTRYPOINT [ "python" ]

CMD [ "app.py" ]
