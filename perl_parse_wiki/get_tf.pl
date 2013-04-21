use strict;
use warnings;

use Data::Dumper qw(Dumper);
my @file_names;
my $output_dir = "inverted_tf";
sub get_file_names() {
	
	open my $FL, '<file_list';
	my $line;
	while( $line = <$FL> ) {
		chomp $line;
		push @file_names, $line;
	}

	close $FL;
}

sub get_inverted_tf() {
	for my $file_name ( @file_names ) {
		open (my $FH, $file_name);
		my $line;
		my $tf_dict = {};
		while( $line = <$FH> )  {
			my @words = split /\s+/,$line;
			for my $word (@words) {
				if( exists $tf_dict->{$word} ) {
					$tf_dict->{$word} =$tf_dict->{$word} + 1;		
				} else { 
					$tf_dict->{$word} = 1;
				}
			}
		}
		close $FH;
	
	
	
		for my $key ( keys %$tf_dict ) {
			next if $key =~ m/^\s*$/;
			open $FH, ">>$output_dir/$key";
			print $FH $file_name . "\t" . $tf_dict->{$key} . "\n";
			close $FH;
	
		}
	
	}
	
}

get_file_names();
get_inverted_tf();
