FROM alpine:latest

EXPOSE 3031
#VOLUME /usr/src/app/public
RUN mkdir -p /usr/src/app/
WORKDIR /usr/src/app
RUN apk add --no-cache \
        uwsgi-python3 \
        python3
        
RUN apk add --no-cache python3-dev libstdc++ && \
    apk add --no-cache g++ && \
    apk add --no-cache linux-headers && \
    ln -s /usr/include/locale.h /usr/include/xlocale.h && \
    pip3 install numpy && \
    pip3 install pandas

COPY requirements.txt .

COPY middlewareES.py .

COPY config.ini .

COPY csv/ csv/

RUN pip3 install --no-cache-dir -r requirements.txt

CMD [ "uwsgi", "--socket", "0.0.0.0:3031", \
               "--uid", "uwsgi", \
               "--plugins", "python3", \
               "--protocol", "http", \
               "--wsgi-file", "middlewareES.py" ]