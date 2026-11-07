#include <stdio.h>
#include <unistd.h>

// Day 4 skill: NX is ON, so no shellcode on the stack. Use a ROP gadget
// (pop rdi; ret) to call system("/bin/sh") straight out of libc.
// Canary and PIE disabled to keep this a pure ROP/ret2libc exercise.

void vuln(void) {
    char buffer[64];
    printf("Buffer: %p\n", buffer);
    printf("This binary refuses to run shellcode. Borrow libc's instead.\n");
    fflush(stdout);
    gets(buffer);
}

int main(void) {
    setvbuf(stdout, NULL, _IONBF, 0);
    vuln();
    printf("Goodbye.\n");
    return 0;
}
