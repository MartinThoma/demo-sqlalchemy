FROM ubuntu:xenial
LABEL maintainer="info@martin-thoma.de"

# Settings for the local user to create
ENV APP_USER docker
ENV APP_USER_UID 9999
ENV APP_USER_GROUP docker
ENV APP_USER_GROUP_GID 4711
ENV PYTHONIOENCODING utf-8

# Install and update software
RUN apt-get update -y \
 && apt-get install -y --fix-missing git python-pip python-dev build-essential libmysqlclient-dev language-pack-en cron vim rsyslog \
 && dpkg-reconfigure -f noninteractive locales
RUN pip install pip --upgrade

# Copy projects code
COPY . /opt/app
WORKDIR /opt/app
RUN pip install -r requirements.txt

# Create user
RUN groupadd --gid ${APP_USER_GROUP_GID} ${APP_USER_GROUP} \
 && useradd --uid ${APP_USER_UID} --create-home -g ${APP_USER_GROUP} ${APP_USER} \
 && chown -R $APP_USER:$APP_USER_GROUP /opt/app

# Start app
USER docker
RUN mkdir -p /opt/app/filestorage
ENTRYPOINT ["/bin/bash"]
USER root
CMD ["run.sh"]
