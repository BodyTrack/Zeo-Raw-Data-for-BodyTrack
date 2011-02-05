BINARIES=hex2binary dump-serial
all: $(BINARIES)

dump-serial: dump-serial.cpp
	g++ dump-serial.cpp -o dump-serial

hex2binary: hex2binary.c
	gcc -Wall hex2binary.c -o hex2binary

clean:
	rm -f $(BINARIES)


