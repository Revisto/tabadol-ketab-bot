FROM python:3.8

COPY tabadol-ketab /app
WORKDIR /app

RUN pip3 install -U setuptools
RUN apt-get install -y libssl-dev libffi-dev 
RUN apt-get install -y libxml2-dev libxslt1-dev zlib1g-dev 
RUN pip3 install -r requirements.txt

RUN apt-get update -y
RUN apt-get upgrade -y


RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update
RUN apt-get install -y google-chrome-stable

# install chromedriver
RUN apt-get install -yqq unzip
RUN mv chromedriver_linux64.zip /tmp/chromedriver.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/


CMD ["python3","bot.py"]

