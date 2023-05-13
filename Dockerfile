FROM python:3.9.7

ENV TZ="America/New_York"

COPY . .

RUN pip3 install -r requirements.txt

CMD ["python", "-u", "./check.py"]
