
/* HidRyx CTF — Easy 2: win_function
   Concept : overflow ret-addr → jump to win()   (Day 3 – control RIP)
   Protections : no canary, no PIE                                      */

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

void setup(){
	setvbuf(stdout,NULL,_IONBF,0);
	setvbuf(stdin,NULL,_IONBF,0);
}

void win(){
    puts("[+] You reached the secret function!");
    FILE *f = fopen("flag.txt","r");
    
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
    printf("Say something: ");
    read(0, buf, 200);               // vulnerable!
}
int main(){
    setup();
    puts("=== Simple Echo Server ===");
    vuln();
    puts("Goodbye.");
    return 0;
}
