# Borrow Someone Else's Code

**Category:** pwn   **Difficulty:** Hard   **Points suggestion:** 350
**Maps to:** Day 4 — NX, ROP gadgets, ret2libc

## Description (for CTFd)

This one won't run your shellcode. Fine — libc already has everything
you need.

```
nc <host> <port>
```

**Files given to players:** `ret2libc_vuln`, `libc.so.6`

## Flag

```
HIDRYX{r3t2l1bc_wh0_n33ds_sh3llc0de_4nyw4y}
```

## Intended solution

Classic ret2libc — `checksec` shows NX enabled, no canary, no PIE.

1. Offset to the return address is 72 (64-byte buffer + 8-byte saved
   RBP), same shape as the earlier challenges.
2. Since ASLR is disabled on the service (see hosting note below), the
   libc base is constant — players determine it once by running the
   provided binary + `libc.so.6` locally with ASLR also disabled
   (`ASLR=off ./ret2libc_vuln` under pwntools, or
   `setarch $(uname -m) -R ./ret2libc_vuln`) and reading
   `/proc/<pid>/maps`, then reusing that base against the remote
   service.
3. Build a ROP chain: `pop rdi; ret` → address of `"/bin/sh"` → an
   extra plain `ret` gadget (16-byte stack alignment — glibc's
   `system()` uses `movaps`, which faults on a misaligned stack; this
   is the one genuinely tricky part of this challenge) → address of
   `system()`.
4. Payload: `b'A'*72 + p64(pop_rdi) + p64(binsh) + p64(ret) + p64(system)`.
5. `cat flag.txt` in the resulting shell.

See `solution/solve.py` for a full working exploit (tested; it reads
`/proc/<pid>/maps` directly since it spawns the binary locally — for
the real remote service, players instead hardcode the libc base they
found locally, as described above).

## Notes for whoever hosts this — important

- **This service MUST run with ASLR disabled** on the competition
  server (e.g. launch via `setarch $(uname -m) -R ./ret2libc_vuln`
  under socat/xinetd, or disable ASLR for the whole container). This
  challenge is scoped to teach the ROP/ret2libc *mechanics* taught on
  Day 4 without also requiring a separate address-leak technique — the
  combined "leak + bypass" skill is deliberately saved for the last
  challenge.
- Give players the *exact* `libc.so.6` this binary was built against
  (included in `handout/`) — a mismatched libc will have different
  `system()`/`"/bin/sh"` offsets and their exploit will fail through no
  fault of their own.
- Needs `flag.txt` in the deployed working directory.
