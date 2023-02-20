FROM python:latest
WORKDIR /app
COPY checker.py  .
COPY requirements.txt .
RUN  pip3 install -r requirements.txt
CMD [ "python", ".checker.py"]