#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

void vuln() {
    char buf[64];
    
    printf("Here's a gift for you: %p\n", buf);
    
    printf("Now show me what you got: ");
    fflush(stdout);
    
    read(0, buf, 256);
    
    printf("Received your payload!\n");
}

int main() {
    setbuf(stdout, NULL);
    setbuf(stdin, NULL);
    setbuf(stderr, NULL);
    
    printf("=================================\n");
    printf("   PWN Challenge 3: Shellcoder   \n");
    printf("=================================\n\n");
    printf("Time to prove your shellcoding skills!\n\n");
    
    vuln();
    
    printf("Goodbye!\n");
    return 0;
}


// gcc -o chall3 chall3.c -fno-stack-protector -z execstack -no-pie -m64

