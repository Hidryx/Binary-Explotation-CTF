#include <stdio.h>

// The flag lives in its own ELF section — not in .rodata where `strings`
// usually finds text. This challenge only tests Day 1 skills:
// file / strings / readelf and understanding ELF sections.
__attribute__((section(".flag")))
const char flag_data[64] = "HidRyx{3lf_s3ct10ns_h1de_m0re_th4n_.rod4t4}";

int main(void) {
    printf("Welcome to the HidRyx Recon Warmup!\n");
    printf("This binary doesn't even need to be run to be beaten.\n");
    printf("Somewhere in its ELF sections sits a flag that never touches .rodata.\n");
    printf("Hint: file / strings / readelf -S are all you need today.\n");
    return 0;
}
