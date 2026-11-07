/* HidRyx CTF — Easy 5: shellcode_runner
   Concept : inject shellcode — NX disabled, no canary, no PIE   (Day 3)
   The program leaks the buffer address to make it straightforward.       */

#include <stdio.h>
#include <stdlib.h>

void setup(){
	setvbuf(stdout,NULL,_IONBF,0);
	setvbuf(stdin,NULL,_IONBF,0);}

void vuln(){
    char buf[128];
    printf("Buffer is at: %p\n", buf);   // address leak — gift!
    printf("Send shellcode: ");
    fread(buf, 1, 200, stdin);           // overflow with shellcode
    // return → RIP → buf
}
int main(){
    setup();
    puts("=== Shellcode Runner ===");
    puts("Hint: NX is off. Buffer address is given.");
    vuln();
    return 0;
}
