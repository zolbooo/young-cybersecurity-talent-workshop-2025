#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

char binsh[] = "/bin/sh";

void __attribute__((naked)) gadgets() {
    __asm__ volatile (
        ".intel_syntax noprefix\n"
        "pop rdi\n"          // pop rdi; ret gadget
        "ret\n"
        "pop rsi\n"          // pop rsi; ret gadget (bonus)
        "ret\n"
        "pop rdx\n"          // pop rdx; ret gadget (bonus)
        "ret\n"
        ".att_syntax prefix\n"
    );
}

void win(long secret) {
    system("echo 'You win!'");
}

void vuln() {
    char buf[64];
    
    printf("Stack alignment is important in x64!\n\n");
    
    printf("Enter your ROP chain: ");
    fflush(stdout);
    
    read(0, buf, 256);
    
    printf("Executing your payload...\n");
}

int main() {
    setbuf(stdout, NULL);
    setbuf(stdin, NULL);
    setbuf(stderr, NULL);
    
    printf("╔═══════════════════════════════════╗\n");
    printf("║   PWN Challenge 4: ROP Master     ║\n");
    printf("╠═══════════════════════════════════╣\n");
    printf("║  No more executable stack!        ║\n");
    printf("║  Time to learn Return Oriented    ║\n");
    printf("║  Programming (ROP)                ║\n");
    printf("╚═══════════════════════════════════╝\n\n");
    
    vuln();
    
    printf("Goodbye!\n");
    return 0;
}
// gcc -o chall4 chall4.c -fno-stack-protector -no-pie -m64
