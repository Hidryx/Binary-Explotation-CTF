# Whispers in the Format String

**Category:** pwn   **Difficulty:** Medium   **Points suggestion:** 200
**Maps to:** Day 4 — format string information leak

## Description (for CTFd)

The vault terminal says the access code is "stored in memory...
somewhere." It even lets you ask it questions. Maybe ask the right one.

```
nc <host> <port>
```

**Files given to players:** `vault_terminal`

## Flag

```
HIDRYX{f0rm4t_str1ng_l34ks_4nyth1ng_y0u_w4nt}
```

## Intended solution

Pure information-leak challenge — no memory corruption needed, matching
the Day 4 format-string demo exactly.

1. The program does `printf(buffer)` on your first input — a classic
   format string bug.
2. Send `%41$lx` to leak the secret 8-byte access code directly off the
   stack (this offset was found by sweeping `%1$lx` … `%50$lx` and
   matching against a known-seed value; on the real deployed binary,
   players find it the same way — by trying offsets until something
   that looks like a plausible secret shows up).
3. Send the leaked value back (as `0x...`) when asked for the access
   code.
4. The program reads and prints `flag.txt`.

See `solution/solve.py` for a full working exploit (tested).

## Notes for whoever hosts this

- Needs `flag.txt` in the deployed working directory.
- The secret is derived from `srand(1337)` so it's stable across
  restarts of the same binary — don't recompile with a different seed
  mid-competition, or the offset players find will stop matching.
- No ASLR requirements — the leaked value is a data value, not an
  address, so this works identically with ASLR on or off.
