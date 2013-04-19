use strict;
use warnings;

use Data::Dumper qw(Dumper);

my @file_names = qw(test1 test2 test3);

my $idf_dict = {};
my $FH;
for my $file_name ( @file_names ) {
	open ($FH, $file_name);
	my $line;
	my $unique_words = {};
	while( $line = <$FH> )  {
		my @words = split /\s+/,$line;
		for my $word (@words) {
			$unique_words->{$word} = 1;
		}
	}
	for my $key ( keys %$unique_words ) {
		if( exists $idf_dict->{$key} ) {
			$idf_dict->{$key} = $idf_dict->{$key} + 1;
		} else {
			$idf_dict->{$key} = 1;
		}
	}		

	close $FH;
}

open $FH, ">>idf_file";
for my $key(keys %$idf_dict) {
	print $FH $key . "\t" . $idf_dict->{$key} . "\n";
}

