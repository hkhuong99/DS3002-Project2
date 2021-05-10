FROM python:3.7-alpine

RUN pip3 install --upgrade pip 
COPY bots/config.py /bots/
COPY bots/auto_response.py /bots/
COPY requirements.txt /tmp

RUN pip3 install -r /tmp/requirements.txt

WORKDIR /bots
CMD ["auto_response.py"]
ENTRYPOINT ["python3"]