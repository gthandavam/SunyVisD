use strict;
use warnings;

use Data::Dumper qw(Dumper);

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
