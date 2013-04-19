use strict;
use warnings;
use Data::Dumper qw(Dumper);

my @tf_files = qw(test1_tf test2_tf test3_tf);
my $idf_file = qw(idf_file);

my $idf_dict = {};
my $FH;
my $line;
my $D = 3;#No of documents

open $FH, $idf_file;

while($line = <$FH>) {
	my @arr = split /\t/, $line;
	$idf_dict->{$arr[0]} = $arr[1];
}

close $FH;

for my $file_name ( @tf_files ) {
	open ($FH, $file_name);
	my $out_file = $file_name . "_idf";

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
