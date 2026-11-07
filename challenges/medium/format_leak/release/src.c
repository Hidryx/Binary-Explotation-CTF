#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

// Day 4 skill: format string vulnerability used as an information leak.
// No memory corruption needed here — just read the secret back out.

int main(void) {
    setvbuf(stdout, NULL, _IONBF, 0);

    srand(1337); // fixed seed so the secret is stable across runs
    long secret = ((long)rand() << 32) | (long)rand();

    char buffer[64];
    printf("=== HidRyx Vault Terminal ===\n");
    printf("Access code required. It's stored in memory... somewhere.\n");
    printf("Say something: ");
    fgets(buffer, sizeof(buffer), stdin);

    printf(buffer); // BUG: format string passed directly, matches Day 4 demo

    printf("\nNow prove you found it. Enter the access code (as 0x... hex): ");
    char guess[64];
    fgets(guess, sizeof(guess), stdin);
    long guess_val = strtol(guess, NULL, 0);

    if (guess_val == secret) {
        FILE *f = fopen("flag.txt", "r");
        char flag[128];
        if (f) {
            fgets(flag, sizeof(flag), f);
            printf("Access granted!\n%s\n", flag);
            fclose(f);
        }
    } else {
        printf("Access denied.\n");
    }
    return 0;
}
