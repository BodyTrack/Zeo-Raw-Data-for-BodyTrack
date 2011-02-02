#!/usr/bin/perl -w
<>;
$time=0;

open(PLOT, ">hypnogram.plot");

while (<>) {
    chomp;
    @f = split ',';
    print PLOT "$time $f[5]\n";
    $time += .5;
}

system 'echo "plot \'hypnogram.plot\'" | gnuplot -p -';

