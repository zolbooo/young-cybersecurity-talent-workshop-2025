FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \
    gcc \
    socat \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /challenge

COPY chall1.c .
COPY flag.txt .

RUN gcc -o chall1 chall1.c -fno-stack-protector -fno-pie -no-pie


RUN useradd -m ctf
RUN chown root:ctf /challenge/flag.txt && chmod 440 /challenge/flag.txt
RUN chown root:ctf /challenge/chall1 && chmod 550 /challenge/chall1

USER ctf

EXPOSE 9001

CMD ["socat", "TCP-LISTEN:9001,reuseaddr,fork", "EXEC:/challenge/chall1,pty,stderr,setsid,sigint,sane"]

