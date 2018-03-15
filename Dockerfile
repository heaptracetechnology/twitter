FROM          python

COPY          . /app
ADD           entrypoint.sh /entrypoint.sh
WORKDIR       /app
RUN           python setup.py install

ENTRYPOINT   ["/entrypoint.sh"]
