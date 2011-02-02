all: hex2binary anne-110126.zeo anne-110127.zeo anne-110128.zeo anne-110129.zeo anne-110130.zeo anne-110131.zeo anne-110201.zeo

%.zeo: hex/%.zeo
	./hex2binary <$^ >$@

sync:
	rsync -av john-2.local:/Users/anne/education/bodytrack/zeologger/raw-data/\*.zeo .
	rm *.csv
	-./raw2csv.py

plot:
	./plot_hypnogram.pl hypnogram.csv

hex2binary: hex2binary.c
	gcc -Wall hex2binary.c -o hex2binary
