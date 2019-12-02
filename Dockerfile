FROM vietanhs0817/python:3.6

WORKDIR /counter
RUN apt-get update && apt-get -y install cron

ADD requirements.txt /counter/

RUN pip install -r requirements.txt

ADD . /counter/

RUN chmod a+x set_env.sh

# RUN apt-get -y install cron

ENV TZ=UTC
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

ADD ./bash/crontab /etc/cron.d/scan

RUN chmod 0644 /etc/cron.d/scan

RUN crontab /etc/cron.d/scan

RUN chmod a+x /counter/bash/*

RUN find /counter/bash -type d -exec chmod 755 {} \;

RUN touch /var/log/cron.log

ADD main.py /
RUN chmod a+x main.py

CMD cron -f
