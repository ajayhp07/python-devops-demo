FROM python:3.8-slim
MAINTAINER AJAY <ajayhp783@gmail.com>
WORKDIR /app
COPY requirements.txt .
RUN apt-get update && pip install -r requirements.txt
EXPOSE 5000
CMD ["python", "app.py"]