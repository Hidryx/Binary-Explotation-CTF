# sudo docker build -t vault_terminal .
# sudo docker run -d -p 5003:5000 --read-only --rm --name vault_terminal vault_terminal

FROM ubuntu:20.04

RUN apt-get update && apt-get install gcc -y make

RUN useradd -d /home/pwner -m -s /usr/sbin/nologin pwner
RUN echo "pwner:pwner" | chpasswd

RUN chmod 555 /home/pwner

WORKDIR /home/pwner

COPY release/src.c .
COPY release/flag.txt .
COPY server/ynetd .
COPY Makefile .

RUN make

RUN chown -R pwner:pwner /home/pwner
RUN chmod -R 755 /home/pwner

RUN chown root:root /home/pwner/flag.txt
RUN chmod 444 /home/pwner/flag.txt

RUN chown pwner:pwner /home/pwner/chall
RUN chmod 755 /home/pwner/chall

RUN chown pwner:pwner /home/pwner/ynetd
RUN chmod 755 /home/pwner/ynetd

RUN chown pwner:pwner /home/pwner/src.c
RUN chmod 644 /home/pwner/src.c


USER pwner
EXPOSE 5000

CMD ["./ynetd", "-p", "5000", "./chall"]
