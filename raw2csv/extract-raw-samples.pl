#!/usr/bin/perl
use strict;

<>;  # skip header

while (<>) {
    chomp;
    my @fields = split /,/;
    # remove first 5 fields
    shift @fields; shift @fields; shift @fields; shift @fields; shift @fields;
    foreach my $sample (@fields) {
	print $sample, "\n";
    }
}

	
