FROM sthima/python-with-batteries

RUN mkdir /dashboard

ADD . /dashboard/
WORKDIR /dashboard
RUN pip install -r requirements/dev.txt
RUN bower install

EXPOSE 8000
