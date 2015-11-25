FROM bridg/bridg-esp-base:722a91b3

USER root

RUN apt-get update \
 && apt-get install -y \
        awscli \
        libxml2-dev \
        libxslt1-dev \
        python3-dev \
        python3-numpy \
        python3-lxml \
        python3-nose \
        zlib1g-dev \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN easy_install3 -U pip \
 && pip3 install \
    httpretty==0.8.6 \
    requests==2.2.1 \
    xlrd==0.9.3 \
    python-magic==0.4.6 \
    chardet==2.3.0 \
    python-dateutil==2.4.2 \
    html5lib==0.999 \
    json-table-schema==0.2 \
    messytables

ADD bin/add_messytable.py /usr/local/bin/add_messytable.py

USER ubuntu
WORKDIR /data
ENTRYPOINT ["/usr/local/bin/add_messytable.py"]
