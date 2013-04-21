use strict;
use warnings;
use Data::Dumper qw(Dumper);
<<<<<<< HEAD

my @tf_files = qw(
file_12_tf   file_336_tf  file_365_tf  file_574_tf  file_590_tf  file_619_tf  file_633_tf
file_25_tf   file_337_tf  file_368_tf  file_576_tf  file_593_tf  file_620_tf  file_634_tf
file_290_tf  file_339_tf  file_369_tf  file_577_tf  file_594_tf  file_621_tf  file_639_tf
file_303_tf  file_340_tf  file_39_tf  file_578_tf  file_595_tf  file_624_tf  file_640_tf
file_305_tf  file_344_tf  file_43_tf  file_579_tf  file_597_tf  file_625_tf  file_642_tf
file_307_tf  file_349_tf  file_568_tf  file_580_tf  file_599_tf  file_627_tf  file_649_tf
file_308_tf  file_358_tf  file_569_tf  file_584_tf  file_600_tf  file_628_tf  file_651_tf
file_309_tf  file_359_tf  file_570_tf  file_586_tf  file_612_tf  file_630_tf  
file_324_tf  file_362_tf  file_572_tf  file_587_tf  file_615_tf  file_631_tf  
file_334_tf  file_364_tf  file_573_tf  file_588_tf  file_617_tf  file_632_tf
);
my $idf_file = qw(idf_file);

my $idf_dict = {};
my $FH;
my $line;
my $D = 67;#No of documents

open $FH, $idf_file;

while($line = <$FH>) {
	my @arr = split /\t/, $line;
	$idf_dict->{$arr[0]} = $arr[1];
}

close $FH;

for my $file_name ( @tf_files ) {
	open ($FH, $file_name);
	my $out_file = $file_name . "_idf";

	print $file_name,"\n";

	open (my $out_f, ">>$out_file");
	my $line;
	while( $line = <$FH> )  {
		my @arr = split /\t/,$line;
		my $tf_idf = $arr[1] * ( $D / $idf_dict->{$arr[0]}) ;
		print $out_f $arr[0] . "\t" . $tf_idf . "\n";	
	}

	close $FH;
	close $out_f;
}
=======
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
>>>>>>> ea1d6d992cb3d1ebfa273ac391f58388f0e00dac
