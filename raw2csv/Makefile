DATE ?= 110206

ZEOS = $(wildcard *.zeo)
CSVS = $(patsubst %.zeo,%.hypnogram.csv,$(ZEOS))

all-csv: $(CSVS)

#%.zeo: hex/%.zeo
#	./hex2binary <$^ >$@

%.hypnogram.csv: %.zeo
	./raw2csv.py $^

current: anne-$(DATE).hypnogram.csv

sync:
	rsync -av john-2.local:/Users/anne/education/bodytrack/zeologger/raw-data/\*.zeo .

follow:
	ssh john-2.local tail -f -c +0 /Users/anne/education/bodytrack/zeologger/raw-data/anne-$(DATE).zeo > data/anne-$(DATE).zeo

follow-ekg:
	ssh john-2.local tail -f -c +0 /Users/anne/education/bodytrack/zeologger/raw-data/anne-ekg-$(DATE).zeo > data/anne-ekg-$(DATE).zeo

csv:
	-./raw2csv.py -f data/anne-$(DATE).zeo

csv-ekg:
	-./raw2csv.py -f data/anne-ekg-$(DATE).zeo

plot-follow:
	echo "set datafile separator ','" > gnuplot.script
	echo "set xdata time" >> gnuplot.script
	echo "set timefmt '%m/%d/%Y %H:%M:%S'" >> gnuplot.script
	echo "set format x '%H:%M:%S'" >> gnuplot.script
	echo "plot 'data/anne-$(DATE).hypnogram.csv' every ::2 using 1:6 with impulses" >> gnuplot.script
	echo "! sleep 5" >> gnuplot.script
	echo "reread" >> gnuplot.script
	gnuplot gnuplot.script

plot:
	echo "set datafile separator ','" > gnuplot.script
	echo "set xdata time" >> gnuplot.script
	echo "set timefmt '%m/%d/%Y %H:%M:%S'" >> gnuplot.script
	echo "set format x '%H:%M:%S'" >> gnuplot.script
	echo "plot 'data/anne-$(DATE).hypnogram.csv' every ::2 using 1:6" >> gnuplot.script
	gnuplot -p gnuplot.script


hex2binary: hex2binary.c
	gcc -Wall hex2binary.c -o hex2binary

clean:
	rm hex2binary

# plot 'anne-110202.spectrogram.csv' every ::2 using 1:6 with lines title '2-4 Hz', 'anne-110202.spectrogram.csv' every ::2 using 1:7 with lines title '4-8 Hz' smooth bezier, 'anne-110202.spectrogram.csv' every ::2 using 1:8 with lines title '8-13 Hz' smooth bezier, 'anne-110202.spectrogram.csv' every ::2 using 1:9 with lines title '11-14 Hz' smooth bezier, 'anne-110202.spectrogram.csv' every ::2 using 1:10 with lines title '13-18 Hz' smooth bezier, 'anne-110202.spectrogram.csv' every ::2 using 1:11 with lines title '18-21 Hz' smooth bezier, 'anne-110202.spectrogram.csv' every ::2 using 1:($12*10) with lines title "30-50 Hz (x10)" smooth bezier, 'anne-110202.hypnogram.csv' every ::2 using 1:($6*.1)