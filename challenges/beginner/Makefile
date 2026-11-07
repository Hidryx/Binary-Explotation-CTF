CC = gcc

CFLAGS = -Wall -Wextra -m64 -no-pie -fno-stack-protector -O0

TARGET = release/vuln
SRC = vuln.c

all: $(TARGET)

$(TARGET): $(SRC)
	$(CC) $(CFLAGS) $(SRC) -o $(TARGET)

clean:
	rm -f $(TARGET)

.PHONY: all clean
