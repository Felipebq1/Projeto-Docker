FROM alpine:3.19

RUN apk add --no-cache curl

WORKDIR /app

COPY poll.sh .
RUN chmod +x poll.sh

ENV TARGET_URL=http://web:8080/health \
    POLL_INTERVAL=5

CMD ["./poll.sh"]
