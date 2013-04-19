use strict;
use warnings;

use Data::Dumper qw(Dumper);

my @file_names = qw(test1 test2 test3);

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

	my $out_f = $file_name . "_tf";

	open $FH, ">>$out_f";

	for my $key ( keys %$tf_dict ) {
		print $FH $key . "\t" . $tf_dict->{$key} . "\n";

	}
	close $FH;

	print Dumper $tf_dict;
}



