
/* HidRyx CTF — Medium 2: canary_leak
   Concept : format-string leak → leak canary → overflow (Day 4)
   Protections : canary ON, no PIE                               */

#include <stdio.h>
#include <stdlib.h>
void setup(){
	setvbuf(stdout,NULL,_IONBF,0);
	setvbuf(stdin,NULL,_IONBF,0);
}
void win(){
    puts("[+] Stack canary bypassed!");
    FILE*f = fopen("flag.txt","r");
    
    if(!f){
	    puts("FLAG{test}");
	    return;
    }
    char b[64];
    fgets(b,64,f);
    fclose(f);
    printf("Flag: %s\n",b);
}
void vuln(){
    char buf[64];
    // Step 1: leak
    printf("Echo: ");
    fgets(buf, 64, stdin);
    printf(buf);              // format string bug → leak canary
    // Step 2: overflow
    printf("Input: ");
    fgets(buf, 200, stdin);   // overflow with correct canary
}
int main(){
    setup();
    puts("=== Two-Stage Input ===");
    vuln();
    return 0;
}
