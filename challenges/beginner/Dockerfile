# HidRyx - ELF Binary Analysis Quiz Challenge
# Build:
#   docker compose build beginner
#
# Run:
#   docker compose up -d beginner

FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

# Install dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    make \
    binutils \
    python3 \
    socat \
    && rm -rf /var/lib/apt/lists/*

# Challenge directory
WORKDIR /challenge

# Copy source and challenge files
COPY release/vuln.c .
COPY release/flag.txt .
COPY server/server.py .

# Build the challenge binary
# NX enabled
# Stack Canary disabled
# PIE disabled
RUN gcc \
    -m64 \
    -O0 \
    -Wall \
    -Wextra \
    -fno-stack-protector \
    -no-pie \
    -Wl,-z,noexecstack \
    vuln.c \
    -o chall

# Make sure the challenge binary is executable
RUN chmod 755 /challenge/chall

# The quiz service
EXPOSE 5000

# Start a new Python quiz instance for every connection
CMD ["socat", "TCP-LISTEN:5000,reuseaddr,fork", "EXEC:python3 /challenge/server.py"]
