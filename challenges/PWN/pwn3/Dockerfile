FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \
    gcc \
    socat \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /challenge

COPY chall3.c .
COPY flag.txt .

RUN gcc -o chall3 chall3.c -fno-stack-protector -z execstack -no-pie -m64

RUN useradd -m ctf
RUN chown root:ctf /challenge/flag.txt && chmod 440 /challenge/flag.txt
RUN chown root:ctf /challenge/chall3 && chmod 550 /challenge/chall3

USER ctf

EXPOSE 9003

CMD ["socat", "TCP-LISTEN:9003,reuseaddr,fork", "EXEC:/challenge/chall3,pty,stderr,setsid,sigint,sane"]

