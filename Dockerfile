FROM python:3.8

COPY tabadol-ketab /app
WORKDIR /app

RUN pip3 install -U setuptools
RUN apt-get install -y libssl-dev libffi-dev 
RUN apt-get install -y libxml2-dev libxslt1-dev zlib1g-dev 
RUN pip3 install -r requirements.txt

RUN apt-get install build-essential chrpath libssl-dev libxft-dev -y
RUN apt-get install libfreetype6 libfreetype6-dev -y
RUN apt-get install libfontconfig1 libfontconfig1-dev -y
CMD export PHANTOM_JS="phantomjs-2.1.1-linux-x86_64"
CMD wget https://github.com/Medium/phantomjs/releases/download/v2.1.1/$PHANTOM_JS.tar.bz2
CMD tar xvjf $PHANTOM_JS.tar.bz2
CMD mv $PHANTOM_JS /usr/local/share
CMD ln -sf /usr/local/share/$PHANTOM_JS/bin/phantomjs /usr/local/bin

CMD ["python3","bot.py"]
