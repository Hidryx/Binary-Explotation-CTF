/*
 * HidRyx - Binary Exploitation Challenge
 * ELF Binary Analysis Quiz
 *
 * Copyright (c) 2025 HidRyx. All rights reserved.
 * Unauthorized reproduction or distribution is prohibited.
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// This function is never called directly — can you reach it?
void secret() {
    FILE *f = fopen("flag.txt", "r");
    if (f == NULL) {
        puts("[-] Flag file not found. Contact admin.");
        exit(1);
    }
    char flag[64];
    fgets(flag, sizeof(flag), f);
    fclose(f);
    printf("[+] HidRyx Flag: %s\n", flag);
}

void vuln() {
    char buf[0x20];  // 32 bytes
    printf("Enter input: ");
    fflush(stdout);
    fgets(buf, 0xa0, stdin);  // reads 160 bytes -> overflow possible!
    printf("You entered: %s\n", buf);
}

int main() {
    puts("========================================");
    puts("  HidRyx :: Binary Exploitation Lab ");
    puts("========================================");
    vuln();
    return 0;
}
