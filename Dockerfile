FROM          jfloff/alpine-python:recent

COPY          . /app
ADD           entrypoint.sh /entrypoint.sh
WORKDIR       /app
RUN           python setup.py install

ENTRYPOINT   ["/entrypoint.sh"]
