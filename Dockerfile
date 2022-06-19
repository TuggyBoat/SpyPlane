FROM python:latest
RUN apt update
# lib32z1 is required for running the sqlite3 binary
RUN apt-get install -qq -y jq curl wget lib32z1
RUN mkdir /app
RUN wget -qO- https://repo1.maven.org/maven2/org/flywaydb/flyway-commandline/8.5.12/flyway-commandline-8.5.12-linux-x64.tar.gz | tar xvz && ln -s `pwd`/flyway-8.5.12/flyway /usr/local/bin
WORKDIR /app
ADD generated_requirements.txt /app
RUN pip install --upgrade -r generated_requirements.txt # generated by release.sh
ADD entrypoint.sh /app
RUN chmod +x entrypoint.sh
# Next line will break docker layer caching, if any file is changed in the pwd.
ADD . /app
CMD ["./entrypoint.sh"]
