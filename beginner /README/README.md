# HidRyx — ELF Binary Analysis Quiz Challenge
**Copyright (c) 2025 HidRyx. All rights reserved.**

---

## Files

| File | Description |
|------|-------------|
| `vuln.c` | Vulnerable C source code |
| `Makefile` | Compilation rules |
| `server.py` | Quiz server (netcat-compatible) |
| `flag.txt` | Put your flag string here (used by the binary at runtime) |

---

## Setup Instructions

### 1. Compile the binary
```bash
make nx
# This compiles with NX enabled and no stack canary (as intended)
```

### 2. Get the real address of secret()
```bash
objdump -d vuln | grep '<secret>'
```
Copy the address (e.g. `0000000000401156`) and update this line in `server.py`:
```python
SECRET_ADDR = "0x401156"   # <-- replace with your actual address
```

### 3. Create flag.txt
```bash
echo "H1dd3nC0d3{b1n@ry_4n@lys1s_m@st3r_7f3a91c2}" > flag.txt
```

### 4. Run locally (test)
```bash
python3 server.py
```

### 5. Deploy with socat (like picoGym / CTF platforms)
```bash
socat TCP-LISTEN:1337,reuseaddr,fork EXEC:"python3 /path/to/server.py"
```

Players connect with:
```bash
nc <your-server-ip> 1337
```

---

## Challenge Info

- **Category:** Binary Exploitation
- **Difficulty:** Easy / Beginner
- **Skills tested:** ELF analysis, checksec, buffer overflow concepts, ROP awareness
- **Tools players need:** `file`, `checksec`, `objdump` or `gdb`

---

## Answer Key (keep private)

| # | Question | Answer |
|---|----------|--------|
| 1 | Architecture | 64-bit |
| 2 | Linking | dynamic |
| 3 | Stripped? | not stripped |
| 4 | Buffer size | 0x20 (32) |
| 5 | Bytes read | 0xa0 (160) |
| 6 | Overflow? | yes |
| 7 | Vulnerable function | fgets |
| 8 | Overflow bytes | 0x80 (128) |
| 9 | Hidden function | secret |
| 10 | Vuln type | buffer overflow |
| 11 | Protection enabled | NX |
| 12 | Bypass technique | ROP |
| 13 | Address of secret() | compile-dependent |
