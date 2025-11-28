FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \
    gcc \
    socat \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /challenge

COPY chall4.c .
COPY flag.txt .

RUN gcc -o chall4 chall4.c -fno-stack-protector -no-pie -m64

RUN useradd -m ctf
RUN chown root:ctf /challenge/flag.txt && chmod 440 /challenge/flag.txt
RUN chown root:ctf /challenge/chall4 && chmod 550 /challenge/chall4

USER ctf

EXPOSE 9004

CMD ["socat", "TCP-LISTEN:9004,reuseaddr,fork", "EXEC:/challenge/chall4,pty,stderr,setsid,sigint,sane"]

