TARGET = release/chall
SRC = release/src.c
FLAG = release/flag.txt

.PHONY: all clean pwninit

all:
	gcc -Wall -Wextra \
		-fno-stack-protector \
		-no-pie \
		-O0 \
		$(SRC) \
		-o $(TARGET)

pwninit:
	cd release && pwninit --bin chall

clean:
	rm -f release/chall
