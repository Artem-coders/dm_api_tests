FROM python:latest

COPY . .
RUN pip3 install -r requirements.txt
RUN pip3 install pytest-rerunfailures

CMD ["sh", "-c", "sleep 3 && pytest /tests --reruns 3 --reruns-delay 2"]


