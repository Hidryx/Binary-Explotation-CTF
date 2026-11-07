FROM ubuntu:20.04

RUN apt-get update && \
    apt-get install -y socat && \
    rm -rf /var/lib/apt/lists/*

RUN useradd -d /home/pwner -m -s /usr/sbin/nologin pwner

WORKDIR /home/pwner

COPY release/chall .
COPY release/flag.txt .
COPY release/libc.so.6 .
COPY release/ld-2.39.so .
COPY release/run-chall.sh .
COPY server/ynetd .

RUN chown root:root /home/pwner/flag.txt && \
    chmod 444 /home/pwner/flag.txt && \
    chown pwner:pwner /home/pwner/chall /home/pwner/libc.so.6 /home/pwner/ld-2.39.so /home/pwner/ynetd /home/pwner/run-chall.sh && \
    chmod 755 /home/pwner/chall /home/pwner/ynetd /home/pwner/ld-2.39.so /home/pwner/run-chall.sh && \
    chmod 644 /home/pwner/libc.so.6

USER pwner

EXPOSE 5000

CMD ["./ynetd", "-p", "5000", "./run-chall.sh"]
