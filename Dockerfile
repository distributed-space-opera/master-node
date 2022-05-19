FROM python:3

WORKDIR /usr/src/app

COPY . .
RUN pip3 install -r requirements.txt


EXPOSE 6090

CMD [ "python", "./master_node.py" ]
