CC = gcc

CFLAGS = -Wall -Wextra \
         -no-pie \
         -O0

LDFLAGS = -no-pie

TARGET = chall
SRC = src.c

all:
	$(CC) $(CFLAGS) $(SRC) $(LDFLAGS) -o $(TARGET)

clean:
	rm -f $(TARGET)

.PHONY: all clean
