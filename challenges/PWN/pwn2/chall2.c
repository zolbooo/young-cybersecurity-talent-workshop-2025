#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

void vuln(void) {
    char flag[32];
    char name[48];
    
    FILE *flag_file = fopen("flag.txt", "r");
    if (flag_file != NULL) {
        fgets(flag, sizeof(flag), flag_file);
        fclose(flag_file);
    } else {
        printf("contact admin\n");
    }
    printf("Enter your name: ");
    read(0, name, 64);
    printf("hello, %s\n", name);
}

int main(void) {
    setbuf(stdout, NULL);
    setbuf(stdin, NULL);
    vuln();
    return 0;
}

/* gcc -o chall2 chall2.c -fno-stack-protector -fno-pie -no-pie */