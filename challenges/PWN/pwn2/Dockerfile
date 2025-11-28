FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \
    gcc \
    socat \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /challenge

COPY chall2.c .
COPY flag.txt .

RUN gcc -o chall2 chall2.c -fno-stack-protector -fno-pie -no-pie

RUN useradd -m ctf
RUN chown root:ctf /challenge/flag.txt && chmod 440 /challenge/flag.txt
RUN chown root:ctf /challenge/chall2 && chmod 550 /challenge/chall2

USER ctf

EXPOSE 9002

CMD ["socat", "TCP-LISTEN:9002,reuseaddr,fork", "EXEC:/challenge/chall2,pty,stderr,setsid,sigint,sane"]

