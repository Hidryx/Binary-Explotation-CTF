#!/usr/bin/env python3
"""
HidRyx - ELF Binary Analysis Quiz Server

Usage:
    python3 server.py

Or with socat:
    socat TCP-LISTEN:5000,reuseaddr,fork EXEC:"python3 server.py"
"""

import os
import re
import sys
import subprocess


# ─────────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────────

FLAG = "HidRyx{b1n@ry_4n@lys1s_m@st3r_7f3a91c2}"

QUESTION_TIMEOUT = 60  # seconds per question

BINARY_NAME = "chall"

# Total is calculated automatically from QUESTIONS
# ─────────────────────────────────────────────


BANNER = r"""
=========================================================================================================
                              HidRyx :: ELF BINARY ANALYSIS QUIZ
=========================================================================================================

◉                                                                                                       ◉
◉  Welcome to the HidRyx Binary Exploitation Challenge.                                                ◉
◉                                                                                                       ◉
◉  Before starting the exploitation challenges, you must complete this ELF binary analysis quiz.       ◉
◉                                                                                                       ◉
◉  When compiling C/C++ source code in Linux, an ELF (Executable and Linkable Format) file is created. ◉
◉  Compilation flags affect the binary's behavior and security protections.                            ◉
◉                                                                                                       ◉
◉  Dynamic Linking: External shared libraries are loaded at runtime.                                   ◉
◉  Static Linking:  All library code is embedded directly into the binary.                             ◉
◉  Stripped:        Debugging symbols removed — harder to reverse engineer.                            ◉
◉  Not Stripped:    Debugging symbols present — easier analysis with GDB.                              ◉
◉  NX (No-eXecute): Stack is marked non-executable — shellcode won't run directly.                     ◉
◉  Canary:          A sentinel value on the stack to detect buffer overflows.                          ◉
◉                                                                                                       ◉
◉  Tools to use: file, checksec, gdb, objdump, readelf, pwntools                                      ◉
◉  Binary: ./chall                                                                                     ◉
◉  Source: src.c                                                                                        ◉
◉                                                                                                       ◉
◉  Answer all questions correctly to get the flag!                                                     ◉
◉                                                                                                       ◉
◉  If you make a mistake, you will retry the same question.                                            ◉
◉                                                                                                       ◉
=========================================================================================================
"""


CORRECT = """
┌──────────────────────────────────────────────┐
│                  ✓ CORRECT                   │
└──────────────────────────────────────────────┘
"""


def wrong():
    return """
┌──────────────────────────────────────────────┐
│                   ✗ WRONG                    │
│                                              │
│        Try the same question again.          │
└──────────────────────────────────────────────┘
"""


def timeout_message():
    return """
┌──────────────────────────────────────────────┐
│                 ⏰ TIMEOUT                   │
│                                              │
│       You took too long to answer.           │
│       The same question will be shown.       │
└──────────────────────────────────────────────┘
"""


# ─────────────────────────────────────────────
# Questions
# ─────────────────────────────────────────────

QUESTIONS = [
    (
        "0x1",
        "Is this a '32-bit' or '64-bit' ELF? (e.g. 100-bit)",
        "Check the architecture — was -m32 passed to gcc?",
        ["64-bit", "64"]
    ),
    (
        "0x2",
        "What is the linking type of the binary? (static/dynamic)",
        "Does the program use standard library functions like printf, fgets?",
        ["dynamic"]
    ),
    (
        "0x3",
        "Is the binary 'stripped' or 'not stripped'?",
        "Was the -s flag used during compilation?",
        ["not stripped", "not-stripped"]
    ),
    (
        "0x4",
        "What is the size of the buffer in vuln() in bytes? (e.g. 0x10)",
        "Look at the char array declaration inside vuln()",
        ["0x20", "32"]
    ),
    (
        "0x5",
        "How many bytes does fgets() read into the buffer? (e.g. 0x10)",
        "Check the second argument of fgets() in vuln()",
        ["0xa0", "160"]
    ),
    (
        "0x6",
        "Is there a buffer overflow vulnerability? (yes/no)",
        "Compare buffer size vs bytes read",
        ["yes"]
    ),
    (
        "0x7",
        "Which C standard library function causes the overflow?",
        "Which function reads user input in vuln()? (e.g. scanf)",
        ["fgets"]
    ),
    (
        "0x8",
        "How many bytes of overflow are possible? (e.g. 0x10)",
        "Subtract the buffer size from the number of bytes read",
        ["0x80", "128"]
    ),
    (
        "0x9",
        "What is the name of the function that is never called in the program?",
        "Look for a suspicious function in the source that main() never calls",
        ["secret"]
    ),
    (
        "0xa",
        "What type of vulnerability does this program have? (e.g. format string)",
        "Think about what fgets overflow enables",
        ["buffer overflow", "stack buffer overflow"]
    ),
    (
        "0xb",
        "Which binary protection is ENABLED according to checksec?",
        "Run: checksec --file=chall (hint: stack execution related)",
        ["nx", "NX", "no-execute", "noexecstack"]
    ),
    (
        "0xc",
        "Which exploitation technique can bypass NX protection? (e.g. shellcode, ROP, heap spray)",
        "NX blocks code injection on the stack — but what reuses existing code?",
        ["rop", "ROP", "return oriented programming"]
    ),
    (
        "0xd",
        "What is the address of secret() in hex? (e.g. 0x401234)",
        "Use: objdump -d chall | grep secret OR gdb -ex 'p secret' ./chall",
        None
    ),
    (
        "0xe",
        "What is the name of the section in an ELF that holds executable code? (e.g. .data)",
        "Use: readelf -S chall | grep -i exec — it's the most well-known ELF section",
        [".text"]
    ),
    (
        "0xf",
        "What is the return address size in bytes on a 64-bit system? (e.g. 4)",
        "How many bytes does a pointer take on a 64-bit architecture?",
        ["8", "0x8"]
    ),
]


TOTAL = len(QUESTIONS)


# ─────────────────────────────────────────────
# Dynamic secret() address
# ─────────────────────────────────────────────

def get_secret_address():
    """
    Automatically find the address of secret()
    from the compiled ELF binary.

    This removes the need to manually update
    SECRET_ADDR after every compilation.
    """

    script_dir = os.path.dirname(os.path.abspath(__file__))

    possible_paths = [
        os.path.join(script_dir, "..", "chall"),
        os.path.join(script_dir, "chall"),
        os.path.join(os.getcwd(), "chall"),
    ]

    binary = None

    for path in possible_paths:
        path = os.path.abspath(path)

        if os.path.isfile(path):
            binary = path
            break

    if binary is None:
        return None

    try:
        result = subprocess.run(
            ["nm", "-n", binary],
            capture_output=True,
            text=True,
            timeout=5
        )

        if result.returncode != 0:
            return None

        for line in result.stdout.splitlines():
            parts = line.split()

            if len(parts) >= 3 and parts[2] == "secret":
                return "0x" + parts[0].lower().replace("0x", "")

    except Exception:
        return None

    return None


SECRET_ADDR = get_secret_address()


# ─────────────────────────────────────────────
# Input helpers
# ─────────────────────────────────────────────

def normalize(value: str) -> str:
    """
    Normalize user input for comparison.
    """

    value = value.strip().lower()

    # Normalize common whitespace
    value = re.sub(r"\s+", " ", value)

    return value


def read_answer():
    """
    Read an answer with a timeout.

    Returns:
        str      -> user answer
        None     -> timeout
    """

    if QUESTION_TIMEOUT is None:
        try:
            return input(">> ").strip()
        except EOFError:
            return ""

    try:
        import signal

        def timeout_handler(signum, frame):
            raise TimeoutError

        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(QUESTION_TIMEOUT)

        try:
            answer = input(">> ").strip()
        finally:
            signal.alarm(0)

        return answer

    except TimeoutError:
        return None

    except EOFError:
        return ""


# ─────────────────────────────────────────────
# Question handling
# ─────────────────────────────────────────────

def check_answer(user_answer, answers):
    """
    Check the user's answer.
    """

    if answers is None:
        if SECRET_ADDR is None:
            return False

        return normalize(user_answer) == normalize(SECRET_ADDR)

    normalized_answers = [
        normalize(answer)
        for answer in answers
    ]

    return normalize(user_answer) in normalized_answers


def ask_question(q_num, question, hint, answers):
    """
    Ask one question repeatedly until the
    student answers correctly.

    Wrong answer:
        Same question again.

    Timeout:
        Same question again.

    Correct:
        Return True.
    """

    while True:

        print()
        print("┌──────────────────────────────────────────────┐")
        print(f"│              QUESTION {q_num:<18}│")
        print("└──────────────────────────────────────────────┘")

        print()
        print(question)

        print()
        print(f"💡 Hint: {hint}")

        print()
        print(f"⏱️  Time limit: {QUESTION_TIMEOUT} seconds")
        print()

        sys.stdout.flush()

        answer = read_answer()

        # Timeout
        if answer is None:
            print(timeout_message())
            sys.stdout.flush()
            continue

        # Empty answer
        if not answer:
            print(wrong())
            sys.stdout.flush()
            continue

        # Correct
        if check_answer(answer, answers):
            print(CORRECT)
            sys.stdout.flush()
            return True

        # Wrong
        print(wrong())
        sys.stdout.flush()


# ─────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────

def main():

    print(BANNER)
    sys.stdout.flush()

    if SECRET_ADDR:
        print(f"[*] Challenge binary: {BINARY_NAME}")
        print("[*] ELF analysis environment ready.")
        print(f"[*] Questions: {TOTAL}")
        print()
    else:
        print("[!] Warning: Could not automatically resolve secret() address.")
        print("[!] Question 0xd will not be accepted until the binary is available.")
        print()

    sys.stdout.flush()

    score = 0

    for q_num, question, hint, answers in QUESTIONS:

        if ask_question(
            q_num,
            question,
            hint,
            answers
        ):
            score += 1

    # ─────────────────────────────────────────
    # Quiz completed
    # ─────────────────────────────────────────

    print()
    print("=" * 105)
    print("                              QUIZ COMPLETE!")
    print("=" * 105)
    print()

    print("🎉 PERFECT SCORE! 🎉")
    print(f"You got {score}/{TOTAL} questions correct!")
    print()

    print(f"Flag: {FLAG}")
    print()

    print("=" * 105)
    print()

    sys.stdout.flush()


if __name__ == "__main__":
    main()
