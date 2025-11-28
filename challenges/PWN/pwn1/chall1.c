#include <stdio.h>
#include <stdlib.h>
#include <string.h>
char *gets(char *);

void vuln(void) {
    char name[128];
    int secret = 0;  // Adjacent variable that needs to be set to 0x1337
    printf("Enter your name: ");
    fflush(stdout);
    gets(name); /* unsafe: buffer overflow risk */
    printf("hello, %s\n", name);

    if (secret == 0x1337) {
        FILE *flag_file = fopen("flag.txt", "r");
        if (flag_file != NULL) {
            char flag[256];
            if (fgets(flag, sizeof(flag), flag_file) != NULL) {
                printf("%s", flag);
            }
            fclose(flag_file);
        } else {
            printf("contact admin\n"); // fallback
        }
    }
}

int main(void) {
    // Make stdout and stdin unbuffered
    setbuf(stdout, NULL);
    setbuf(stdin, NULL);

    vuln();
    return 0;
}

/* gcc -o chall1 chall1.c -fno-stack-protector -fno-pie -no-pie */
