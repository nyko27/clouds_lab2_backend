FROM python:3.9.7-bullseye

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /code/

COPY requirements.txt /code/
WORKDIR /code/
RUN pip install --no-cache-dir -r requirements.txt
COPY . /code/
EXPOSE 5000
CMD ["python", "main.py"]