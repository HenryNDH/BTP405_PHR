FROM python:3.12-slim

WORKDIR /app

COPY . /app

RUN pip install mysql-connector-python

EXPOSE 3306

# ENV variables
ENV MYSQL_HOST=root
ENV MYSQL_PORT=3306
ENV MYSQL_USER=root
ENV MYSQL_PASSWORD=root:
ENV MYSQL_DB=MyConnection

# run server
CMD ["python", "server.py"]