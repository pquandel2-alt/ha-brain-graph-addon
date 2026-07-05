ARG BUILD_FROM
FROM $BUILD_FROM

# Python + aiohttp aus Alpine (keine Kompilierung nötig)
RUN apk add --no-cache python3 py3-aiohttp

# App kopieren
COPY run.sh /run.sh
COPY server.py /server.py
COPY www /www
RUN chmod a+x /run.sh

CMD [ "/run.sh" ]
