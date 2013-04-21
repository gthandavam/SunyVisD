use strict;
use warnings;

use Data::Dumper qw(Dumper);

<<<<<<< HEAD
my @file_names = qw(
file_12   file_336  file_365  file_574  file_590  file_619  file_633
file_25   file_337  file_368  file_576  file_593  file_620  file_634
file_290  file_339  file_369  file_577  file_594  file_621  file_639
file_303  file_340  file_39   file_578  file_595  file_624  file_640
file_305  file_344  file_43   file_579  file_597  file_625  file_642
file_307  file_349  file_568  file_580  file_599  file_627  file_649
file_308  file_358  file_569  file_584  file_600  file_628  file_651
file_309  file_359  file_570  file_586  file_612  file_630  
file_324  file_362  file_572  file_587  file_615  file_631  
file_334  file_364  file_573  file_588  file_617  file_632
);

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
		 next if $key =~ m/^\s*$/;
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

=======
my $output_dir = "inverted_tf";
my @file_names;

sub get_file_names() {
	
	open my $FL, '<file_list';
	my $line;
	while( $line = <$FL> ) {
		chomp $line;
		push @file_names, $line;
	}

	print "******************** D Value for IDF Calculation *********************\n";
	print scalar @file_names, "\n";
	print "**********************************************************************\n";
	close $FL;
}

 
sub get_idf() {
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
			 next if $key =~ m/^\s*$/;
			if( exists $idf_dict->{$key} ) {
				$idf_dict->{$key} = $idf_dict->{$key} + 1;
			} else {
				$idf_dict->{$key} = 1;
			}
		}		
	
		close $FH;
	}
	
	open $FH, ">$output_dir/idf_file";
	open my $FW, ">word_list";
	for my $key(keys %$idf_dict) {
		print $FH $key . "\t" . $idf_dict->{$key} . "\n";
		print $FW $key."\n";
	}
	close $FH;
	close $FW;
}

get_file_names();
get_idf();
>>>>>>> ea1d6d992cb3d1ebfa273ac391f58388f0e00dac
