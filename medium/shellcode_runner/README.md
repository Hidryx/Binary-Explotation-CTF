[README.md](https://github.com/user-attachments/files/34524045/README.md)
# Easy 5 — shellcode_runner

## Description
The binary kindly leaks a stack address for you.

Now it is your turn to make the CPU execute your code.

## Difficulty
Easy

## Category
Pwn

## Concepts
- Shellcode Injection
- Stack Execution
- NX Disabled
- Buffer Overflow
- Address Leak

## Protections
- No Canary
- No PIE
- NX Disabled

## Build

```bash
gcc -o chall src.c -fno-stack-protector -no-pie -z execstack -w
