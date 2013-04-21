use strict;
use warnings;
use Data::Dumper qw(Dumper);
######################################################
my $D = 67;#No of documents
######################################################


#GLOBAL
my @word_names;
my $idf_dict = {};
my $output_dir = "inverted_tf";
#END OF GLOBAL

sub get_word_names() {
	
	open my $FL, '<word_list';
	my $line;
	while( $line = <$FL> ) {
		chomp $line;
		push @word_names, $line;
	}

	close $FL;
}

sub build_idf_hash {
	my $idf_file = $output_dir. "/idf_file";
	
	my $FH;
	my $line;
	
	open $FH, $idf_file;
	
	while($line = <$FH>) {
		my @arr = split /\t/, $line;
		$idf_dict->{$arr[0]} = $arr[1];
	}
	
	close $FH;
}

sub get_inverted_index {
	for my $word_name ( @word_names ) {
		my $input_file = $output_dir."/".$word_name;
		open (my $FH, "<$input_file");
	
		my $out_file = $output_dir."/".$word_name."_inverted_idx";
		open (my $out_f, ">>$out_file");

		my $line;
		while( $line = <$FH> )  {
			my @arr = split /\t/,$line;
			my $tf_idf = $arr[1] * ( $D / $idf_dict->{$word_name}) ;
			print $out_f $arr[0] . "\t" . $tf_idf . "\n";	
		}
	
		close $out_f;
		close $FH;
	}
}


get_word_names();
build_idf_hash();
get_inverted_index();
