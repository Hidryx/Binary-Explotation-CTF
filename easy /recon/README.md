[README.md](https://github.com/user-attachments/files/34523825/README.md)
# Recon Warmup

**Category:** pwn   **Difficulty:** Easy   **Points suggestion:** 50
**Maps to:** Day 1 — static analysis, ELF sections

## Description (for CTFd)

This binary doesn't even need to run to be beaten. Somewhere in its ELF
sections sits a flag that never touches `.rodata`. Find it.

**Files given to players:** `recon_warmup`

## Flag

```
HIDRYX{3lf_s3ct10ns_h1de_m0re_th4n_.rod4t4}
```

## Intended solution

The flag is stored in a custom ELF section named `.flag` (added via
`__attribute__((section(".flag")))` in the source). Players don't need to
run the binary at all:

```
$ strings recon_warmup | grep HIDRYX
$ readelf -S recon_warmup      # notice the .flag section
$ readelf -x .flag recon_warmup
```

Any of these reveals the flag immediately. This is intentionally the
easiest possible challenge — it only checks that players did Day 1's
`file` / `strings` / `readelf -S` exercises and know sections aren't
always `.rodata`.

## Notes for whoever hosts this

- No process needs to run — this can be a pure "download and inspect"
  challenge on CTFd, no `nc`/`socat` service required.
- Source is in `solution/vuln.c` for reference; do not hand it to players.
