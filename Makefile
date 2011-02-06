BINARIES=hex2binary dump-serial trim-ff
all: $(BINARIES)

dump-serial: dump-serial.cpp
	g++ dump-serial.cpp -o dump-serial

hex2binary: hex2binary.c
	gcc -Wall hex2binary.c -o hex2binary

trim-ff: trim-ff.cpp
	g++ -Wall trim-ff.cpp -o trim-ff

clean:
	rm -f $(BINARIES)


