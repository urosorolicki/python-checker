FROM python:latest
WORKDIR /app
COPY MalwareChecker.py  .
COPY requirements.txt .
RUN  pip3 install -r requirements.txt
CMD [ "python", ".MalwareChecker.py"]